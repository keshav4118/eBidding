from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from . import sendEmail
from myadmin import models as myadmin_models
from user import models as user_models 
import time

media_url = settings.MEDIA_URL

# middleware to check session for mainapp routes
def sessioncheck_middleware(get_response):
	def middleware(request):
		if request.path=='' or request.path=='/home/' or request.path=='/about/' or request.path=='/contact/' or request.path=='/login/' or request.path=='/service/' or request.path=='/register/':
			request.session['sunm']=None
			request.session['srole']=None
			response = get_response(request)

		else:
			response = get_response(request)
		return response
	return middleware


def index(request):
    clist = myadmin_models.Category.objects.all()
    return render(request, 'index.html', {'clist': clist, "media_url": media_url})


def viewsubcategory(request):
    catnm = request.GET.get("catnm")
    clist = myadmin_models.Category.objects.all()
    sclist = myadmin_models.SubCategory.objects.filter(catnm=catnm)
    return render(request, "viewsubcategory.html", {"catnm": catnm, "clist": clist, "sclist": sclist, "media_url": media_url})


def viewproduct(request):
    catnm = request.GET.get("catnm")
    clist = myadmin_models.Category.objects.all()
    sclist = myadmin_models.SubCategory.objects.filter(catnm=catnm)
    uplist = user_models.Product.objects.filter(catnm=catnm)
    return render(request, "viewproduct.html", {"catnm": catnm, "clist": clist, "sclist": sclist, 'uplist':uplist,"media_url": media_url})

def about(request):
    return render(request, 'about.html')


def register(request):
    if request.method == "GET":
        return render(request, 'register.html', {"output": " "})

    else:
        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        gender = request.POST.get("gender")
        info = time.asctime()

        sendEmail.mymail(username, password)

        p = models.Register(name=name, username=username, password=password, mobile=mobile,
                            address=address, city=city, gender=gender, role='user', status=0, info=info)
        p.save()
        return render(request, "register.html", {"output": "form submitted"})


def verifyuser(request):
    email = request.GET.get("email")
    models.Register.objects.filter(username=email).update(status=1)
    return redirect("/login/")


def login(request):
    if request.method == "GET":
        return render(request, "login.html", {"output": ""})
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        userDetails = models.Register.objects.filter(
            username=username, password=password, status=1)

        if len(userDetails) > 0:
            # To store details in session
            request.session["sunm"] = userDetails[0].username
            request.session["srole"] = userDetails[0].role

            if userDetails[0].role == "admin":
                return redirect("/myadmin/")
            else:
                return redirect("/user/")
        else:
            return render(request, "login.html", {"output": "Invalid user , please check authentication..."})


def services(request):
    return render(request, "services.html")


def contact(request):
    return render(request, 'contact.html')
