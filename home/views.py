from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from datetime import datetime
from home.models import Contact , Product, Order
from django.contrib import messages
from home.forms import Signup_form,EditUserProfileForm,EditAdminProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    product = Product.objects.all()
    allProds=[]
    catprods= Product.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n = len(prod)
        allProds.append([prod, range(1,n)])
        

    params={'allProds':allProds }
    
    return render(request, 'index.html',params)

def next(request):
    if request.method == 'POST':
        fm = Signup_form(request.POST)
        if fm.is_valid():
            fm.save()       
            messages.success(request,'Account Created Successfully')
    else:
        fm=Signup_form()
    return render(request, 'about.html', {'form':fm})

def log_in(request):
    if request.method =='POST':
        fm=AuthenticationForm(request=request ,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            user= authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
            return HttpResponseRedirect('/vivek')
    else:
        fm=AuthenticationForm()
    return render(request,'login.html', {'form':fm})    

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(request.POST, instance=request.user)
                users = User.objects.all()
            else:
                 fm = EditUserProfileForm(instance=request.user)
                 users = None
            if fm.is_valid():
                messages.success(request,'Profile updated succesfully')
                fm.save()
        else:
            if request.user.is_superuser == True:
                fm = EditAdminProfileForm(instance=request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfileForm(instance=request.user)
                users = None
            return render(request,'profile.html', {'name':request.user, 'form':fm, 'users':users} )
    else:
        return HttpResponseRedirect('/login/')    



def services(request):
    return render(request, 'services.html')
 

def contact(request):
   if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        contact = Contact(name = name, email = email, phone = phone, desc = desc)
        contact.save()
        messages.success(request, 'Your message has been sent!')
   return render(request, 'contact.html')
 
def user(request):
    return render(request, 'boot.html')

def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
        state=state, zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        id = order.order_id
        return render(request, 'checkout.html', {'thank':thank, 'id': id})
    return render(request, 'checkout.html')    


def vishal(request, my_id):
    # Fetch the product using the id
    product = Product.objects.filter(id = my_id)
    

    return render(request, 'prodView.html', {'product':product[0]})    