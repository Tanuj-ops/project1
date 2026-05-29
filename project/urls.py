from os import name

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='reg'),
    path('check_user/',views.check_user,name="check_user"),
    path('login/', views.user_login,name='user_login'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('artist_dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('edit_artist_profile/', views.edit_artist_profile, name='edit_artist_profile'),
    path('edit_user_profile/', views.edit_user_profile, name='edit_user_profile'),
    path('add_product/', views.add_product_view, name='add_product'),
    path('my_products/', views.my_product, name='my_product'),
    path('single_product/', views.single_product, name='single_product'),
    path('update_product/', views.update_product, name='edit_product'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('all_product/', views.all_product, name='all_product'),
    path('buy/', views.buy_product, name='buy_now'),
    path('cart/', views.add_to_cart, name='cart'),
    path('get_cart_data/', views.get_cart_data, name='get_cart_data'),
    path('change_quan/', views.change_quan, name='change_quan'),
    # path('payment/', views.payment_page, name='payment_page'),
    
    path('precess_payment/', views.precess_payment, name='precess_payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('A_change_password/', views.A_change_pass, name='A_change_password'),
    path('U_change_password/', views.U_change_pass, name='U_change_password'),
]
