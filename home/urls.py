from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.next, name='about'),
    path("info", views.log_in, name='info'),
    path("checkout", views.checkout, name='checkout'),
    path("profile", views.user_profile, name='profile'),
    path("vivek", views.user, name='vivek'),
    path("products/<int:my_id>/", views.vishal,name="ProductView" ),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'), 
]