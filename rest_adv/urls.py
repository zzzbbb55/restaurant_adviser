from django.urls import path
from rest_adv import views

app_name = 'rest_adv'

urlpatterns = [
    path('', views.index, name='index'),
    path('restaurant/<slug:restaurant_name_slug>/',
        views.show_restaurant, name='show_restaurant'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('restaurant/<slug:restaurant_name_slug>/add_review/', views.add_review, name='add_review'),
    path('add_restaurant/',views.add_restaurant,name='add_restaurant'),
    path('save_restaurant/',views.save_restaurant,name='save_restaurant'),
    path('search_restaurant',views.search_restaurant,name='search_restaurant'),
    path('update_my_profile',views.update_my_profile,name='update_my_profile'),
    path('my_collections',views.my_collections,name='my_collections'),
    path('my_reviews',views.my_reviews,name='my_reviews'),
    path('login_by_google',views.login_by_google,name='login_by_google'),
    path('category_restaurant/<str:category>/',views.category_restaurant,name='category_restaurant'),
]