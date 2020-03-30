import json

from django.contrib.auth.models import User

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_adv.models import Restaurant,Review,UserProfile

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.files import File
from io import BytesIO
from urllib.request import urlopen

from rest_adv.forms import UserForm, UserProfileForm, ReviewForm, RestaurantForm

# Create your views here.
def index(request):
    context_dict = {}
    # get all restaurants
    context_dict['restaurants'] = Restaurant.objects.all().order_by('id')
    # get top 3 rate restaurants
    context_dict['top_restaurants'] = Restaurant.objects.all().order_by('-rate')[:3]

    # get first
    context_dict['first_restaurant'] = context_dict['top_restaurants'][0]
    return render(request,'rest_adv/index.html', context_dict)

def category_restaurant(request, category):
    context_dict={'restaurants':[],'search_text':category}
    try:
        restaurants = Restaurant.objects.filter(category=category)
        context_dict['restaurants'] = restaurants
        context_dict['top_restaurants'] = Restaurant.objects.all().order_by('-rate')[:3]
    except Restaurant.DoesNotExist:
        context_dict['restaurants'] = []
    return render(request, 'rest_adv/search_restaurant.html', context = context_dict)

def search_restaurant(request):
    search_text = request.GET.get('search_text')
    context_dict={'restaurants':[],'search_text':search_text}
    try:
        restaurants = Restaurant.objects.filter(intro__contains=search_text)
        context_dict['restaurants'] = restaurants

        context_dict['top_restaurants'] = Restaurant.objects.all().order_by('-rate')[:3]
    except Restaurant.DoesNotExist:
        context_dict['restaurants'] = []
    return render(request, 'rest_adv/search_restaurant.html', context = context_dict)

@login_required
def my_profile(request):
    context_dict = {}
    try:
        context_dict['user'] = request.user
    except Restaurant.DoesNotExist:
        context_dict['user'] = None
    return render(request, 'rest_adv/my_profile.html', context = context_dict)

@login_required
def update_my_profile(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            website = request.POST.get('website')
            
            # request.user.like_restaurants.add(restaurant_id)
            current_user = request.user

            if current_user.username != username:
                current_user.username = username
                current_user.save()

            if 'picture' in request.FILES:
                current_user.profile.picture = request.FILES['picture']
                current_user.profile.save()
            
            if current_user.profile.website != website:
                current_user.profile.website = website
                current_user.profile.save()
            
    except Restaurant.DoesNotExist:
        pass
    return redirect(reverse('rest_adv:my_profile'))

@login_required
def my_collections(request):
    context_dict = {}
    try:
        context_dict['restaurants'] = request.user.profile.like_restaurants.all()
    except Restaurant.DoesNotExist:
        context_dict['restaurants'] = None
    return render(request, 'rest_adv/my_collections.html', context = context_dict)

@login_required
def my_reviews(request):
    context_dict = {}
    try:
        context_dict['reviews'] = Review.objects.filter(user=request.user)
    except Restaurant.DoesNotExist:
        context_dict['reviews'] = None
    return render(request, 'rest_adv/my_reviews.html', context = context_dict)

def show_restaurant(request, restaurant_name_slug):
    context_dict={}
    try:
        restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
        context_dict['restaurant'] = restaurant
        reviews = Review.objects.filter(restaurant=restaurant)
        context_dict['reviews'] = reviews
    except Restaurant.DoesNotExist:
        context_dict['restaurant'] = None
    return render(request, 'rest_adv/restaurant.html', context = context_dict)

@login_required
def save_restaurant(request):
    try:
        if request.method == 'POST':
            # json_result = json.loads(request.body, strict=False)
            restaurant_id = request.POST.get('id')
            restaurant = Restaurant.objects.get(id=restaurant_id)
            
            # request.user.like_restaurants.add(restaurant_id)
            current_user = UserProfile.objects.get(user_id=request.user.id)

            if current_user.like_restaurants.filter(id=restaurant_id):
                result = {"status":"not post","data":"You have saved it~!"}
            else:
                current_user.like_restaurants.add(restaurant_id)
                result = {"status":"not post","data":"Saved success!"}

            # return success
            return JsonResponse(result,safe=False) 
        else:
            result = {"status":"not post","data":[request.body]}
            return JsonResponse(result,safe=False) 
    except Restaurant.DoesNotExist:
        # return error
        result = {"status":"error","data":""}
        return JsonResponse(result)


def login_by_google(request):
    if request.method == 'POST':
        google_id = request.POST.get('google_id')
        google_email = request.POST.get('google_email')
        google_profile_url = request.POST.get('google_profile_url')
        google_first_name = request.POST.get('google_first_name')
        google_last_name = request.POST.get('google_last_name')

        users = User.objects.filter(email=google_email)
        if users:
            # login with exists account
            login(request, users[0])
            result = {"status":"success","data":"User exists, login success!"}
            return JsonResponse(result,safe=False) 

        user = User()
        user.username = google_email
        user.email = google_email
        user.set_password('123456') # init password is 123456
        user.first_name = google_first_name
        user.last_name = google_last_name
        user.is_active = True
        user.save()

        profile = UserProfile(user=user)

        # get profile from google
        # r = urlopen(google_profile_url)
        # io = BytesIO(r.read())
        # result = profile.picture.save("{}_{}.jpg".format('test',int(time.time())), File(io))
        # profile.picture = google_profile_url
        profile.save()

        login(request, user)

        result = {"status":"success","data":"Login success!"+result}
        return JsonResponse(result,safe=False) 
    else:
        result = {"status":"error","data":"Not Post Method"}
        return JsonResponse(result,safe=False) 


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            #put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                 'rest_adv/register.html',
                 context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})


def user_login(request):
    context_dict = {}
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rest_adv:index'))
            else:
                # An inactive account was used - no logging in!
                context_dict['message'] = "Your Rango account is disabled."
                return render(request, 'rest_adv/login.html', context_dict)
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            context_dict['message'] = "Invalid login details supplied."
            return render(request, 'rest_adv/login.html', context_dict)
            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rest_adv/login.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rest_adv:index'))

@login_required
def add_review(request, restaurant_name_slug):
    try:
        restaurant = Restaurant.objects.get(slug=restaurant_name_slug)
    except Restaurant.DoesNotExist:
        restaurant = None
    if restaurant is None:
        return redirect('rest_adv')

    form = ReviewForm()
    if request.method == 'POST' and restaurant:
        review = Review()
        review.rate = int(request.POST.get('rate'))

        # rate must in 0~5
        if review.rate > 5:
            review.rate = 5
        if review.rate < 0:
            review.rate = 0

        review.message = request.POST.get('message')
        review.restaurant=restaurant
        review.user=request.user
        review.save()

        # update restaurant rate
        calculate_rate(restaurant)

        return redirect(reverse('rest_adv:show_restaurant',
                                        kwargs={'restaurant_name_slug':
                                                restaurant_name_slug}))
    context_dict={'form':form,'restaurant':restaurant}
    return render(request,'rest_adv/add_review.html',context_dict)

def calculate_rate(restaurant):
    """
    Read all rates, calculate the average as new rate.
    """
    new_rate = 0
    all_reviews = restaurant.review_set.all()
    rate_count = len(all_reviews)
    for review in all_reviews:
        new_rate += review.rate
    new_rate = round(new_rate/rate_count,2)
    restaurant.rate = new_rate
    restaurant.save()
    return True

@login_required
def add_restaurant(request):
    form=RestaurantForm()
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.rate = 0
            if 'picture' in request.FILES:
                restaurant.picture = request.FILES['picture']
            restaurant.category = request.POST.get('category')
            restaurant.save()
            return redirect(reverse('rest_adv:show_restaurant',
                                    kwargs={'restaurant_name_slug':
                                                restaurant.slug}))
        else:
            print(form.errors)
    return render(request, 'rest_adv/add_restaurant.html', {'form':form })