from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from . import models
from ebidding import models as e_models


# middleware to check session for admin routes
def sessioncheckmyadmin_middleware(get_response):
    def middleware(request):
        if request.path == '/myadmin/' or request.path == '/myadmin/manageusers/' or request.path == '/myadmin/manageuserstatus/' or request.path == '/myadmin/addcategory/' or request.path == '/myadmin/addsubcategory/':
            if request.session['sunm'] == None or request.session['srole'] != "admin":
                response = redirect('/login/')
            else:
                response = get_response(request)
        else:
            response = get_response(request)
        return response
    return middleware


# Create your views here.

def adminhome(request):
    return render(request, 'adminhome.html', {"sunm": request.session["sunm"]})


def manageuser(request):
    userDetails = e_models.Register.objects.filter(role='user')
    return render(request, "manageuser.html", {"userDetails": userDetails, "sunm": request.session["sunm"]})


def manageuserstatus(request):
    regid = request.GET.get("regid")
    s = request.GET.get("s")

    if s == "block":
        e_models.Register.objects.filter(regid=int(regid)).update(status=0)
    elif s == "verify":
        e_models.Register.objects.filter(regid=int(regid)).update(status=1)
    else:
        e_models.Register.objects.filter(regid=int(regid)).delete()

    return redirect("/myadmin/manageuser/")


def addcategory(request):
    if request.method == 'GET':
        return render(request, 'addcategory.html', {'output': '', "sunm": request.session["sunm"]})
    else:
        catnm = request.POST.get('catnm')
        caticonnm = request.FILES['caticonnm']
        fs = FileSystemStorage()
        filename = fs.save(caticonnm.name, caticonnm)
        p = models.Category(catnm=catnm, caticonnm=filename)
        p.save()
        return render(request, 'addcategory.html', {'output': 'Category added Successfully', "sunm": request.session["sunm"]})


def addsubcategory(request):
    clist = models.Category.objects.all()
    if request.method == 'GET':
        return render(request, 'addsubcategory.html', {'output': '', 'clist': clist, "sunm": request.session["sunm"]})
    else:
        catnm = request.POST.get('catnm')
        subcatnm = request.POST.get('subcatnm')
        subcaticonnm = request.FILES['subcaticonnm']
        fs = FileSystemStorage()
        filename = fs.save(subcaticonnm.name, subcaticonnm)
        p = models.SubCategory(
            catnm=catnm, subcatnm=subcatnm, subcaticonnm=filename)
        p.save()
        return render(request, 'addsubcategory.html', {'output': "Sub Category added Successfully", 'clist': clist, "sunm": request.session["sunm"]})


def changepws(request):
    if request.method == "GET":
        return render(request,"changepws.html",{"sunm": request.session["sunm"]})
    else:
        opass = request.POST.get("opass")
        npass = request.POST.get("npass")
        cnpass = request.POST.get("cnpass")
        res= e_models.Register.objects.filter(username=request.session["sunm"],password=opass).exists()
        if res:
            if npass==cnpass:
                e_models.Register.objects.filter(username=request.session["sunm"],password=opass).update(password=cnpass)
                return render(request,"changepws.html",{"sunm":request.session["sunm"],"output":"password changed successfully , please login again"})
            else:
                return render(request,"changepws.html",{"sunm":request.session["sunm"],"output":"New & Confirm new password mismatch , try again"})    
        else:  
            return render(request,"changepws.html",{"sunm":request.session["sunm"],"output":"Invalid old password , please try again"})

