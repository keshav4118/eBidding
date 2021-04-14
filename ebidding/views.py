from django.shortcuts import render, redirect
from django.conf import settings
from . import models
from . import sendEmail
from . import sentEmailforget
from django.http import HttpResponse

from myadmin import models as myadmin_models
from user import models as user_models
import time
from . import encryption_api
from . import decryption_api

media_url = settings.MEDIA_URL

# middleware to check session for mainapp routes


def sessioncheck_middleware(get_response):
    def middleware(request):
        if request.path == '' or request.path == '/home/' or request.path == '/about/' or request.path == '/contact/' or request.path == '/login/' or request.path == '/service/' or request.path == '/register/':
            request.session['sunm'] = None
            request.session['srole'] = None
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
    subcatnm = request.GET.get("subcatnm")
    clist = myadmin_models.Category.objects.all()
    uplist = user_models.Product.objects.filter(subcategory=subcatnm)
    return render(request, "viewproduct.html", {'uplist': uplist, "clist": clist, "media_url": media_url})


def about(request):
    # response = render(request, 'about.html')

    # response.set_cookie("cunm","Hy i am Here ",3600*24)
    # response.set_cookie("cpass","hello Every one ",3600*24)
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
    cunm = ""
    cpass = ""
    if request.COOKIES.get("cunm") != None:
        cunm = request.COOKIES.get('cunm')
        cpassword = request.COOKIES.get('cpass')
        l = list(cpassword)
        l.pop(0)
        l.pop(0)
        l.pop(len(l)-1)
        s = ""
        for x in l :
            s += x
        cpassword_byte = bytes(s, 'utf-8')
        cpass = decryption_api.decrypt_message(cpassword_byte)


    if request.method == "GET":
        return render(request, "login.html", {"output": "","cunm":cunm,"cpass":cpass})
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
                response = redirect("/myadmin/")

            else:
                response = redirect("/user/")
                
            # To Store Details in Cookies
            if request.POST.get("chk") == "remember":
                encrypted_message=encryption_api.encrypt_message(userDetails[0].password)
                response.set_cookie("cunm", userDetails[0].username, 3600*24)
                response.set_cookie("cpass", encrypted_message, 3600*24)
            return response

        else:
            return render(request, "login.html", {"output": "Invalid user , please check authentication...","cunm":cunm,"cpass":cpass})


def forgetpws(request):
    if request.method == "GET":
        return render(request, "forget.html", {"output": ""})
    else:
        username = request.POST.get("username")
        print("username:",username)
        passwordDetails = models.Register.objects.filter(username=username)
        password = passwordDetails[0].password
        print(password)
        sentEmailforget.mymail(username,password)
        return render(request, "forget.html", {})

def services(request):
    return render(request, "services.html")


def contact(request):
    return render(request, 'contact.html')
