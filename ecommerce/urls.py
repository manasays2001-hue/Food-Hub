"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from restuarent import views

    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_home', views.admin_home , name='admin_home'),
    path('', views.index, name='index'),
    path('entry/', views.entry, name='entry'),
    path('product/', views.product, name='product'),
    path('edit/<int:product_id>/', views.edit, name='edit_product'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment_page, name='payment_page'),
    path('update_quantity/<int:cart_id>/', views.update_quantity, name='update_quantity'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('add-address/', views.add_address, name='add_address'),
    path('edit-address/<int:id>/', views.edit_address, name='edit_address'),
    path("update-address/", views.update_address, name="update_address"),
    path('place_order/', views.place_order, name='place_order'),
    path("orders/", views.my_orders, name="orders"),
    path("profile/", views.profile_dashboard, name="profile_dashboard"),
    path("orders/<int:order_id>/", views.order_details, name="order_details"),
    path("orders/cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('order_dashboard', views.order_dashboard, name='order_dashboard'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('users', views.users, name='users'),
    path('order_detail', views.order_detail, name='order_detail'),

]
