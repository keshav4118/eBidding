from django.urls import path

from . import views 

urlpatterns = [
     path('',views.userhome),
     path('addproduct/',views.addproduct),
     path('fetchSubCategoryAJAX/',views.fetchSubCategoryAJAX),
     path('viewproductuser/',views.viewproductuser),
     path('payment/',views.payment),
     path('edituser/',views.edituser),
     path('success/',views.success),
     path('cancel/',views.cancel),
     path('bidproduct/',views.bidproduct),
     path('bidproductview/',views.bidproductview),
     path('mybid/',views.mybid),
     path('userchangepws/',views.userchangepws),
     path("bidhistory/",views.bidhistory),

]
