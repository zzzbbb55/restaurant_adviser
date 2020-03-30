from django.urls import path
from rest_adv import views

app_name = 'rest_adv'

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurant/<slug:restaurant_name_slug>/',
        views.show_restaurant, name='show_restaurant'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('restaurant/<slug:restaurant_name_slug>/add_review/',
         views.add_review, name='add_review'),
    path('add_restaurant/',views.add_restaurant,name='add_restaurant'),
]