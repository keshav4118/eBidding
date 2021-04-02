from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from myadmin import models as myadmin_models
from . import models

import time

#middleware to check session for admin routes
def sessioncheckuser_middleware(get_response):
	def middleware(request):
		if request.path=='/user/' or request.path=='/user/addproduct/':
			if request.session['sunm']==None or request.session['srole']!="user":
				response = redirect('/login/')
			else:
				response = get_response(request)
		else:
			response = get_response(request)		
		return response	
	return middleware


# Create your views here.

def userhome(request):
 return render(request,"userhome.html",{"sunm":request.session["sunm"]})

def addproduct(request):
 clist=myadmin_models.Category.objects.all()
 if request.method=="GET":
  return render(request,"addproduct.html",{"output":"","clist":clist,"sunm":request.session["sunm"]}) 
 else:
  title=request.POST.get('title')
  category=request.POST.get('cat')	
  subcategory=request.POST.get('subcat')
  description=request.POST.get('description')
  bprice=request.POST.get('bprice')

  file1=request.FILES['file1']
  fs = FileSystemStorage()
  file1name = fs.save(file1.name,file1)

  if request.POST.get('file2')=="":
   file2name="logo.jpeg"
  else:
   file2=request.FILES['file2']
   fs = FileSystemStorage()
   file2name = fs.save(file2.name,file2)

  if request.POST.get('file3')=="":
   file3name="logo.jpeg"
  else:
   file3=request.FILES['file3']
   fs = FileSystemStorage()
   file3name = fs.save(file3.name,file3)

  if request.POST.get('file4')=="":
   file4name="logo.jpeg"
  else:
   file4=request.FILES['file4']
   fs = FileSystemStorage()
   file4name = fs.save(file4.name,file4)		

  p=models.Product(title=title,category=category,subcategory=subcategory,description=description,bprice=bprice,file1=file1name,file2=file2name,file3=file3name,file4=file4name,status=0,uid=request.session['sunm'],info=time.time())
  p.save()	 
  return render(request,"addproduct.html",{"output":"Product added successfully....","clist":clist,"sunm":request.session["sunm"]})	 


def fetchSubCategoryAJAX(request):
 cnm=request.GET.get("cnm")   
 sclist=myadmin_models.SubCategory.objects.filter(catnm=cnm) 
 sclist_options="<option>Select sub category</option>"
 for row in sclist:
     sclist_options+=("<option>"+row.subcatnm+"</option>")
 return HttpResponse(sclist_options)


def viewproductuser(request):
 plist=models.Product.objects.filter(uid=request.session["sunm"])
 return render(request,"viewproductuser.html",{"plist":plist,"sunm":request.session["sunm"]}) 