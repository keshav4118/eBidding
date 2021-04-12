from django.urls import path

from . import views 

urlpatterns = [
     path('',views.adminhome),
     path('addcategory/',views.addcategory),
     path('manageuser/',views.manageuser),
     path('editadmin/',views.editadmin),
     path('manageuserstatus/',views.manageuserstatus),
     path('addsubcategory/',views.addsubcategory),
     path('changepws/',views.changepws),
     
]