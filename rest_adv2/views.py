from django.shortcuts import render
from django.http import HttpResponse
from rest_adv.models import Restaurant,Review

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_adv.forms import UserForm, UserProfileForm, ReviewForm, RestaurantForm

# Create your views here.
def index(request):

    return render(request,'rest_adv/index.html')

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
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
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
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            if restaurant:
                review = form.save(commit=False)
                review.restaurant=restaurant
                review.user=request.user
                review.save()
                return redirect(reverse('rest_adv:show_restaurant',
                                        kwargs={'restaurant_name_slug':
                                                restaurant_name_slug}))
        else:
            print(form.errors)
    context_dict={'form':form,'restaurant':restaurant}
    return render(request,'rest_adv/add_review.html',context_dict)

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
            restaurant.save()
            return redirect(reverse('rest_adv:show_restaurant',
                                    kwargs={'restaurant_name_slug':
                                                restaurant.slug}))
        else:
            print(form.errors)
    return render(request, 'rest_adv/add_restaurant.html', {'form':form })