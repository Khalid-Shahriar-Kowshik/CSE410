from django.urls import path
from . import views

urlpatterns = [
    path('guides/', views.guide_list, name='guide_list'),
    path('guides/create/', views.guide_create, name='guide_create'),
    path('guides/<int:pk>/update/', views.guide_update, name='guide_update'),
    path('guides/<int:pk>/delete/', views.guide_delete, name='guide_delete'),

]