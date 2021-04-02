from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('viewsubcategory/',views.viewsubcategory),
    path('viewproduct/',views.viewproduct),
    path('about/', views.about),
    path('register/', views.register),
    path('login/', views.login),
    path('services/', views.services),
    path('contact/', views.contact),
    path('myadmin/', include('myadmin.urls')),
    path('user/', include('user.urls')),
    path('verifyuser/',views.verifyuser),
    
] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)