from django.contrib import admin
from django.urls import path,include
from django.contrib.auth.views import LoginView
from .import views

urlpatterns = [
path('cpu/', views.cpu, name='cpu'),
path('mobo/', views.mobo, name='mobo'),
path('cpucooler/', views.cpucooler, name='cpucooler'),
path('ram/', views.ram, name='ram'),
path('storage/', views.storage, name='storage'),
path('gpu/', views.gpu, name='gpu'),
path('psu/', views.psu, name='psu'),
path('case/', views.case, name='case'),
path('cpu/<int:cpu_id>/', views.cpu_detail, name='cpu_detail'),
path('mobo/<int:mobo_id>/', views.mobo_detail, name='mobo_detail'),
path('cpu-cooler/<int:cooler_id>/', views.cpu_cooler_detail, name='cpu_cooler_detail'),
path('ram/<int:ram_id>/', views.ram_detail, name='ram_detail'),
path('storage/<int:storage_id>/', views.storage_detail, name='storage_detail'),
path('gpu/<int:gpu_id>/', views.gpu_detail, name='gpu_detail'),
path('psu/<int:psu_id>/', views.psu_detail, name='psu_detail'),
path('case/<int:case_id>/', views.case_detail, name='case_detail'),

# Product search and autocomplete
path('search/', views.product_search, name='product_search'),
path('autocomplete/', views.product_autocomplete, name='product_autocomplete'),

path("cart/", views.view_cart, name="cart_view"),
path("cart/add/<str:product_type>/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
path("cart/remove/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),
path("order/place/", views.place_order, name="place_order"),
path("order/<int:order_id>/", views.order_details, name="order_details"),
path('orders/', views.order_list, name='order_list'),
path('order/delete/<int:order_id>/', views.delete_order, name='delete_order'),
]