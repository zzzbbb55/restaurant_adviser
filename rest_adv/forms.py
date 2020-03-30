from django import forms
from django.contrib.auth.models import User
from rest_adv.models import UserProfile,Review,Restaurant

class ReviewForm(forms.ModelForm):
    # <input id="input-1" name="input-1" class="rating rating-loading" data-min="0" data-max="5" data-step="1">

    rate = forms.CharField(
        max_length=5,
        min_length=1,
        widget=forms.TextInput(attrs={
            'class':'rating rating-loading',
            'data-min':0,
            'data-max':5,
            'data-step':1,
            'type':'number'
        }))


    message = forms.CharField()
    class Meta:
        model = Review
        fields = ('rate', 'message',)

class RestaurantForm(forms.ModelForm):
    name = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    # rate = forms.FloatField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    intro = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
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