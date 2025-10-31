from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView
from .import views
from django.conf import settings
from django.conf.urls.static import static
from .admin import my_admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve

urlpatterns = [
    path('', views.home, name='home'),
    path('base', views.base, name='base'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/',views.register,name='register'),
    path('login/',views.LOGIN,name='login'),
    path('logout/', views.LOGOUT, name='logout'),
    path('builder/', views.builder, name='builder'),
    path('products/', include('products.urls')),

    path('buildhub/', include('buildhub.urls')),

    path('userprofile/', include('userprofile.urls')),
    path('guides/', include('guides.urls')),

    path('admin/', my_admin.urls),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
