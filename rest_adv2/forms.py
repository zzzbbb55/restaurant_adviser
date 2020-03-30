from django import forms
from django.contrib.auth.models import User
from rest_adv.models import UserProfile,Review,Restaurant

class ReviewForm(forms.ModelForm):
    rate = forms.IntegerField()
    message = forms.CharField()
    class Meta:
        model = Review
        fields = ('rate', 'message',)

class RestaurantForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    rate = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    intro = forms.CharField()
    class Meta:
        model = Restaurant
        fields = ('name','picture','intro')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)