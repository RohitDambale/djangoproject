from django.shortcuts import render,HttpResponse,redirect
from messageapp.models import Msg
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from messageapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay

# Create your views here.
def create(request):
    print("request is:",request.method)
    if request.method=="GET":
        return render(request,'create.html')
    else:
        n=request.POST['uname']
        p=request.POST['uemail']
        q=request.POST['umob']
        s=request.POST['msg']
        # /print('name is',n)
        # print('email is',p)
        # print('mobno is',q)
        # print('msg is:',s)

        m= Msg.objects.create(name=n,email=p,mobile=q,msg=s)
        m.save()
        return redirect('/dashboard')
        #return HttpResponse("Insert form data into db")
    
def dashboard(request):
    m=Msg.objects.all()
    #print(m)
    context={}
    context['data']=m
    return render(request,'dashboard.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u[0])
        p=Product.objects.filter(id=pid)
        print(p[0])
        c=Cart.objects.create(uid=u[0],pid=p[0])
        c.save()
        #print(userid)
        #print(pid)
        return HttpResponse("Product is successfully added to cart")
    else:
        return redirect("/user_login")
def delete(request,rid):
    #print("id to be deleted is :",rid)
    m=Msg.objects.filter(id=rid)
    print(m)
    m.delete()
    #return HttpResponse("id to be deleted is :"+rid)
    return redirect('/dashboard')

def edit(request,rid):
    #print("id to be edited",rid)
    #return HttpResponse("id to be edited is:"+rid)
    if request.method=="GET":
        m=Msg.objects.filter(id=rid)
        print(m)
        context={}
        context['data']=m
        return render(request,'edit.html',context)
    
    else:
        un=request.POST['uname']
        uemail=request.POST['uemail']
        umob=request.POST['umob']
        umsg=request.POST['msg']
        #print(un)
        m=Msg.objects.filter(id=rid)
        m.update(name=un,email=uemail,mobile=umob,msg=umsg)
        return redirect('/dashboard')
    
def home(request):
    #userid=request.user.id
    #print(userid)
    #print("result",request.user.is_authenticated)
    context={}
    p=Product.objects.filter(is_activate=True)
    print(p)
    
    context['Products']=p
    return render(request,'index.html',context)

def catfilter(request,cv):
    q1=Q(is_activate=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1 & q2)
    print(p)
    context={}
    context['Products']=p
    return render(request,'index.html',context)


def prodet(request,pid):
    context={}
    context['Products']=Product.objects.filter(id=pid)
  
    return render(request,'product_details.html',context)

def about(request):
    return render(request,'about.html')

def cart(request):
    return render(request,'cart.html')

def contact(request):
    return render(request,'contact.html')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print('orderid',oid)
    #print(c)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    for x in c:
        s=s+x.pid.price * x.qty
    context={}

    context['n']=np
    context['Product']=c
    context['total']=s
    return render(request,'placeorder.html',context)

def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        upassword=request.POST['upassword']
        if uname =="" or upass=="" or upassword=="":
            context['errormsg']="Field cannot be empty" 
            return render(request,'register.html',context)
        elif upass!=upassword:
            context['errormsg']="password and confirm password did not match" 
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(upassword)
                u.save()
                context['success']="user created succesffully please login"
                return render(request,'register.html',context)
            except Exception:
                context['errormsg']="username already exist" 
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np=len(c)
    context={}
    for x in c:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.qty
       
        context['n']=np
        context['Products']=c
        context['Total']=s
    return render(request,'cart.html',context)

    

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=="1":
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    #print(c)
    #print(c[0])
    #print(c[0].qty)
    return redirect ('/viewcart')


def user_logout(request):
    logout(request)
    return redirect('/home')

def user_login(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        #print(uname)
        #print(upass)
        if uname =="" or upass=="":
            context['errormsg']="Field cannot be empty" 
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errormsg']="Invalid username and pass"
                return render(request,"login.html",context)
            #print(u)
            #return HttpResponse("Data is fetch")
    else:   
        return render(request,'login.html')
    

def sort(request,sv):
    if sv=="0":
        col='price'
    else:
        col='-price'

    p=Product.objects.filter(is_activate=True).order_by(col)
    print(p)
    context={}
    context['Products']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['umin']
    max=request.GET['umax']
    #print(min)
    #print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_activate=True)
    p=Product.objects.filter(q1 & q2 & q3)
    context={}
    context['Products']=p
    return render(request,'index.html',context)

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0

    for x in orders:
        #print(x)
        #print(x.pid.price)
        s=s+x.pid.price * x.qty
        oid=x.order_id

    client = razorpay.Client(auth=("rzp_test_zyMr545mMqCvJ5", "xbRsMvRRs6hIXrvD7HW2Huai"))

    data = { "amount": s*100, "currency": "INR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    
    return render(request,'pay.html',context)
       
