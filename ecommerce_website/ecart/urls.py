from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.login_page, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit_user_details/', views.edit_user_details, name='edit_user_details'),
    path('logout/', views.logout, name='logout'),
    path('forgot-password/', views.forgot_pwd, name='forgotpwd'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
     path('cart/', views.cart, name='cart'),
    path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_quantity/<int:cart_id>/', views.update_cart_quantity, name='update_cart_quantity'),

    path('payment/', views.payment, name='payment'),
]
