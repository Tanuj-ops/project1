from multiprocessing import context
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from project.models import category,register_table, add_product, cart ,order,feature_product
from urllib import request 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from project.forms import add_product_form
from django.db.models import Q
from django.http import JsonResponse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings


def center_text(text, width=80):
    if text is None:
        text = ""
    return str(text).center(width)


def home(request):
    cats = category.objects.all()
    feature = feature_product.objects.all()
    return render(request, 'home.html', {"category": cats, "feature_p":feature})


def register(request):
    if request.method == "POST":
        fname = request.POST.get("first")
        lname = request.POST.get("last")
        un = request.POST.get("uname")
        em = request.POST.get("email")
        con= request.POST.get("contact")
        tp = request.POST.get("utype")
        pwd = request.POST.get("password")

        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = lname
        if tp == "artist":
            usr.is_staff = True
        usr.save()

        reg = register_table(user=usr, contact_number=con)
        reg.save()
        return render(request, "register.html", {"status": "Mr./Mrs. {} Your Account created successfully!".format(fname)})

    return render(request, 'register.html')

def check_user(request):
    if request.method == "GET":
        Un= request.GET.get("usern")
        check = User.objects.filter(username=Un)
        if len(check) == 1:
            return HttpResponse("exist")
        else:
            return HttpResponse("not exist")
      
def user_login(request):
    if request.method == "POST":
        un = request.POST.get("username")
        pwd = request.POST.get("password")
        user = authenticate(request, username=un, password=pwd)
        if user:
            login(request, user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            if user.is_staff:
                return HttpResponseRedirect("/project")
            if user.is_active:
                return HttpResponseRedirect("/project")
        else:
            return render(request, "login.html", {"status": "Invalid username or password"})
        
    return render(request, "login.html") 

@login_required
def user_dashboard(request):
    return render(request, "user_dashboard.html")

@login_required
def artist_dashboard(request):
    return render(request, "artist_dashboard.html") 

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/project")


def edit_artist_profile(request):
    context = {}
    data= register_table.objects.get(user__id=request.user.id)
    context['data'] = data
    if request.method == "POST":
        fn = request.POST.get("fname")
        ln = request.POST.get("lname")
        em = request.POST.get("email")
        co= request.POST.get("contact")
        age = request.POST.get("age")
        gen= request.POST.get("gender")
        ad= request.POST.get("address")
        bio= request.POST.get("bio")
        uid= request.POST.get("upi_id")
        upn= request.POST.get("upi_number")
        ex= request.POST.get("experience")

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        
        data.contact_number=co
        data.age = age
        data.gender = gen
        data.address = ad
        data.bio = bio
        data.upi_id = uid
        data.upi_number = upn
        data.experience = ex    
        data.save()
        
        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_image = img
            data.save()
        context['status'] = "Profile updated successfully!"
    return render(request, "edit_artist_profile.html", context)

def edit_user_profile(request):
    context = {}
    data= register_table.objects.get(user__id=request.user.id)
    context['data'] = data
    if request.method == "POST":
        fn = request.POST.get("fname")
        ln = request.POST.get("lname")
        em = request.POST.get("email")
        co= request.POST.get("contact")
        age = request.POST.get("age")
        gen= request.POST.get("gender")
        ad= request.POST.get("address")
        bio= request.POST.get("bio")
        uid= request.POST.get("upi_id")
        upn= request.POST.get("upi_number")

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fn
        usr.last_name = ln
        usr.email = em
        usr.save()

        
        data.contact_number=co
        data.age = age
        data.gender = gen
        data.address = ad
        data.bio = bio
        data.upi_id = uid
        data.upi_number = upn    
        data.save()
        
        if "image" in request.FILES:
            img = request.FILES["image"]
            data.profile_image = img
            data.save()

        context['status'] = "Profile updated successfully!"
    return render(request, "edit_user_profile.html", context)


def add_product_view(request):
    context = {}
    ch= register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
    form =add_product_form()
    if request.method == "POST":
        form = add_product_form(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            login_user = User.objects.get(username=request.user.username)
            data.Artist = login_user
            data.save()
            context['status'] = "{} added successfully!".format(data.product_name)
    context['form'] = form
    return render(request, "add_product.html", context)


def my_product(request):
    context = {}
    ch= register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context['data'] = data
        
    all= add_product.objects.filter(Artist__id=request.user.id).order_by("-id")
    context['products'] = all
    return render(request, "my_product.html", context)


def single_product(request):
    context = {}
    id = request.GET.get("pid")
    obj = add_product.objects.get(id=id)
    context["product"] = obj
    return render(request, "single_product.html", context)


def update_product(request):
    context ={}
    cat = category.objects.all().order_by("cat_name")
    context["cats"] = cat

    pid = request.GET["pid"]
    product = add_product.objects.get(id=pid)
    context["product"] = product

    if request.method=="POST":
        pn = request.POST["pname"]
        ct_id = request.POST["pcat"]
        pr = request.POST["pp"]
        sz = request.POST["psize"]
        dis = request.POST["dp"]

        cat_obj = category.objects.get(id=ct_id)

        product.product_name = pn
        product.product_category = cat_obj
        product.price = pr
        product.size = sz
        product.description = dis
        if "pimg" in request.FILES:
            img = request.FILES["pimg"]
            product.product_image = img
        product.save()
        context["status"] = "Changes Saved Successfully"
        context["id"] = pid
    return render(request, "edit_product.html",context)


def delete_product(request):
    context = {}
    if "pid" in request.GET:
        pid = request.GET["pid"]
        prd = get_object_or_404(add_product, id=pid)
        context["product"] = prd

        if "action" in request.GET:
            prd.delete()
            context["status"] = str(prd.product_name)+"Deleted Successfully!!"
    return render(request, "delete_product.html", context)


def all_product(request):
    context = {}
    all_product = add_product.objects.all().order_by("product_name")
    context['products'] = all_product 

    if "qry" in request.GET:
        q = request.GET["qry"]
        prd = add_product.objects.filter(Q(product_name__icontains=q)|Q(product_category__cat_name__contains=q))
        context["products"] = prd

    if "cat" in request.GET:
        cid = request.GET["cat"]
        prd = add_product.objects.filter(product_category__id=cid)
        context["products"] = prd

    return render(request, "all_product.html", context)

def buy_product(request):
    context = {}
    id = request.GET.get("pid")
    obj = add_product.objects.get(id=id)
    context["product"] = obj

    return render(request, "buy_now.html", context)

def add_to_cart(request):
    context = {}
    items = cart.objects.filter(user__id=request.user.id,status=False)
    context["items"] = items
    if request.user.is_authenticated:
        if request.method=="POST":
            pid = request.POST["pid"]
            qty = request.POST["qty"]
            is_exist = cart.objects.filter(product__id=pid,user__id=request.user.id,status=False)
            if len(is_exist)>0:
                context["msz"] = "Item Already Exist In Your Cart"
                context["cls"] = "alert alert-warning"
            else:
                product = get_object_or_404(add_product,id=pid)
                usr = get_object_or_404(User,id=request.user.id)
                c = cart(user=usr,product=product,quantity=qty)
                c.save()
                context["msz"] = "{} Added in Your Cart".format(product.product_name)
                context["cls"] = "alert alert-success"
    
    else:
        context["status"] = "Please Login First To View Your Cart"
        context["cls"] = "alert alert-success"
    return render(request, "cart.html", context) 



def get_cart_data(request):
    items = cart.objects.filter(user__id=request.user.id, status=False)
    total,quantity = 0,0
    for i in items:
        total += i.product.price
        quantity += i.quantity

    res = {
        "total":total, "quan":quantity
    }
    return JsonResponse(res)


def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = int(request.GET["quantity"])
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)
    
    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponse(1)


# def payment_page(requqst):
#     return render(request, "payment.html")

def precess_payment(request):
    items = cart.objects.filter(user_id__id=request.user.id,status=False)

    products = ""
    amt = 0
    inv = "INV-"
    cart_ids = ""
    p_ids = ""
    for j in items:
        products += str(j.product.product_name)+"\n"
        p_ids += str(j.product.id)+","
        amt += float(j.product.price)
        inv += str(j.id)
        cart_ids += str(j.id)+","

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': products,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),
    }
    usr = User.objects.get(username=request.user.username)
    ord = order(cust_id=usr,cart_id=cart_ids,product_ids=p_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session["order_id"] = ord.id

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment.html', {'form': form})
    

def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(order,id=order_id)
        ord_obj.status = True
        ord_obj.save()

        for i in ord_obj.cart_id.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status = True
            cart_object.save()
            
    return render(request, 'payment_done.html')
    # return render(request, 'payment_failed.html')


def payment_cancelled(request):
    return render(request, 'payment_failed.html')

def A_change_pass(request):
    context = {}
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request, 'A_change_password.html', context)


def U_change_pass(request):
    context = {}
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]

        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"
    return render(request, 'U_change_password.html', context)