from django.urls import path

from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='product_list'),
    path('category/<slug:slug>/', ProductListByCategory.as_view(), name='category_list'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('login_registration', login_registration, name='login_registration'),
    path('login', user_login, name='login'),
    path('logout', user_logout, name='logout'),
    path('register', register, name='register'),
    path('save_review/<slug:product_slug>/', safe_review, name='save_review'),
    path('reviews', ReviewsList.as_view(), name='reviews'),
    path('contact/', contact, name='contact'),
    path('search/', SearchResult.as_view(), name='search'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('clear_cart/', clear_cart, name='clear_cart')
]