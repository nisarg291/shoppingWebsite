from django.shortcuts import render,redirect, get_object_or_404,HttpResponse
import numpy as np
import pandas as pd
import json
import csv
import re
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from selenium import webdriver
import json
p_sitename=[];
p_name=[];
p_image=[];
p_price=[];
p_type=[];
manufacture1=[];
isAvailable1=[];
label1=[];
site1=[];
pr_sitename=[];
pr_name=[];
pr_image=[];
pr_price=[];
pr_type=[];
manufacture2=[];
isAvailable2=[];
label2=[];
site2=[]
from shop.models import Product,Cart,UserAddress1,CheckOut
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings

from shop import Checksum


from shop.models import CheckOut,PaytmHistory
# Create your views here.
usr=""
def payment(request):
    global usr;
    usr=request.user;
    print(usr)
    MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
    MERCHANT_ID = settings.PAYTM_MERCHANT_ID
    get_lang = "/" + get_language() if get_language() else ''
    CALLBACK_URL = settings.HOST_URL + get_lang + settings.PAYTM_CALLBACK_URL
    # Generating unique temporary ids
    order_id = 104

    bill_amount = 100
    if bill_amount:
        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(order_id)),
            ('CUST_ID', str(request.user.email)),
            #('TXNID',str(100)),
            #('BANKTXNID',str(1000)),
            ('TXN_AMOUNT', str(bill_amount)),
            
           # ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            # ('EMAIL', request.user.email),
            # ('MOBILE_N0', '9911223388'),
            ('INDUSTRY_TYPE_ID',"Retail"),
            ('CALLBACK_URL', "http://127.0.0.1:8000/response/"),
            # ('PAYMENT_MODE_ONLY', 'NO'),
        )

        paytm_params = dict(params)
        paytm_params['CHECKSUMHASH'] = Checksum.generateSignature(paytm_params, settings.PAYTM_MERCHANT_KEY)
        print(paytm_params['CHECKSUMHASH'])
        return render(request,"payment.html",{'paytmdict':paytm_params})
    return HttpResponse("Bill Amount Could not find. ?bill_amount=10")


@csrf_exempt
def response(request):
    global usr;
    if request.method == "POST":
        MERCHANT_KEY = settings.PAYTM_MERCHANT_KEY
        data_dict = {}
        for key in request.POST:
            
                data_dict[key] = request.POST[key]
        print(data_dict['CHECKSUMHASH'])
        verify = Checksum.verifySignature(data_dict, MERCHANT_KEY, data_dict['CHECKSUMHASH'])
        if verify:
            print("user",request.user)
            print(usr)
            print(data_dict)
           # data_dict['BANKTXNID']=str(1000);
            #data_dict['quantity']="3";
            #data_dict['TXNID']=str(100);
            PaytmHistory.objects.create(user=usr, **data_dict)
            return render(request,"response.html",{"paytm":data_dict})
        else:
            return HttpResponse("checksum verify failed")
    return HttpResponse(status=200)

def home(request):
    global usr;
    usr=request.user;
    cart=Cart.objects.filter(user_email=request.user)
    count=Cart.objects.filter(user_email=request.user).count()
    products=Product.objects.all();
    print(count)
    print(cart)
    productNames=[]
    productPrices=[]
    quantity=[]
    productId=[]
    productImages=[]
    for ct in cart:
        prod=ct.product_id.product_name.split(' ');
        name=""
        for p in prod:
            name+=p+'_';
            
        productNames.append(name)
        productImages.append(ct.product_id.product_image);
        
        productPrices.append(ct.product_id.product_price)
        quantity.append(ct.quantity);
        productId.append(ct.product_id.id)
    print(quantity)
    print(productNames)
    print(productPrices)
    return render(request,"home.html",{'products':products,'cart':cart,'count':count,'prodnames':productNames,'prodid':productId,'prodprices':productPrices,'prodimages':productImages,'quantity':quantity})

def addToCart(request,id):
    if request.method=="POST":
        quant=request.GET.get('quant');   
        product=Product.objects.get(id=id);
        usr=request.user.id;
        print(usr)
        #driver=webdriver.chrome();
        #quantity=driver.exexute_script("window.localStorage.getItem('Cart');");
        #cart.save();
        ct=Cart.objects.all();
        return render(request,'CartList.html',{'cart':ct});
    return render(request,'cartlist.html');
def cart(request):
    user=request.user;
    cart=Cart.objects.filter(user_email=user);
    count=Cart.objects.filter(user_email=user).count();
    return render(request,"cart.html",{'cart':cart,'count':count})

def address(request):
    if request.method=='POST':
        usr=request.user;
        address=request.POST.get('address');
        add=UserAddress1(user=usr,address=address);
        add.save();
        cart=Cart.objects.filter(user_email=request.user);
        prodID="";
        quant="";
        for c in cart:
            prodID+=str(c.product_id)+',';
            quant+=str(c.quantity)+',';
        checkout=CheckOut(user_email=request.user,product_id=prodID,address=add.address,quantity=quant,status=True)
        checkout.save();
        checkouts=CheckOut.objects.get(user_email=request.user)
        prids=checkouts.product_id.split(',');
        products=[];
        quantity=[];
        for prid in prids:
            products.append(Product.objects.get(id=prid));
            quantity.append(Product.objects.get(id=prid));
        print(checkouts)
        print(products)
        return render(request,"goforcheckout.html",{'checkouts':checkouts,'products':products,'quantity':quantity})
    return render(request,"address.html")

def updateCart(request):
    print("hi");
    usr=request.user;
    id=request.GET.get('id');
    quant=request.GET.get("quant");
    #id=data['id'];
    print(id,quant);
    prd=Product.objects.get(id=id);
    #quant=data['quant'];
    cart=Cart.objects.get(product_id=prd,user_email=request.user);
    cart.quantity=int(quant);
    cart.save();
    print(cart);
    ct=Cart.objects.filter(user_email=request.user).count();
    print(ct);
    price=int(cart.quantity)*float(cart.product_id.product_price) ;
    return HttpResponse(str(price));

def addCart(request):
    usr=request.user;
    id=request.GET.get('id');
    quant=request.GET.get("quant");
    #id=data['id'];
    print(id,quant)
    prd=Product.objects.get(id=id);
    #quant=data['quant'];
    cart=Cart(user_email=usr,product_id=prd,quantity=quant);
    cart.save()
    ct=Cart.objects.filter(user_email=request.user).count();
    print(ct);
    return HttpResponse(str(ct));

def productview(request,id):
    prd=Product.objects.get(id=int(id))
    product={
        'id':prd.id,
        'product_name':prd.product_name,
        'product_image':prd.product_image,
        'product_type':prd.product_type,
        'product_manufacture':prd.product_manufacture,
        'product_price':prd.product_price,
        'count':Cart.objects.filter(user_email=request.user).count(),
        }
    print(product)
    return render(request,"productview.html",product)
def index(request):
    global pr_sitename,pr_name, pr_image, pr_price, pr_type, manufacture2, isAvailable2, label2, site2
    if "a"<"b":
        print("b")
    if "a"<"c":
        print("c")
    if "a"<"z":
        print("z")
    else:
        print("a")
    pharmeasy=pd.read_csv('PharmEasyProducts.csv');
    pharmeasy.sort_values(['product_name'],axis=0,ascending=True,inplace=True)
    pharmeasyrows=len(pharmeasy)
    pharmeasy.to_json('pharmeasyproduct.json');
    with open('pharmeasyproduct.json') as myfile:
        data=myfile.read()
    pharmeasy = json.loads(data)
    medlife=pd.read_csv('MedLifeProducts.csv');
    # medlife.sort_values(['product_name'],axis=0,ascending=True,inplace=True)
    medliferows=len(pharmeasy)
    medlife.to_json('medlifeproduct.json');
    with open('medlifeproduct.json') as myfile:
        data=myfile.read()
    medlife = json.loads(data)
    netmeds=pd.read_csv('netmedsproduct.csv');
    # netmeds.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    netmedsrows=len(netmeds)
    netmeds.to_json('netmedsproduct.json');
    with open('netmedsproduct.json') as myfile:
        data = myfile.read()
    netmeds = json.loads(data)
    onemg = pd.read_csv('onemgproduct.csv');
    onemgrows=len(onemg)
    # onemg.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    onemg.to_json('onemgproduct.json');
    with open('onemgproduct.json') as myfile:
        data = myfile.read()
    onemg = json.loads(data)
    product_sitename=[]
    product_name=[]
    product_price=[]
    product_image=[]
    product_type=[]
    manufacture=[]
    isAvailable=[]
    site=[]
    for i in range(0,onemgrows):
        if i < pharmeasyrows:
            product_sitename.append('PharmEasy');
            product_name.append(pharmeasy['product_name'][str(i)]);
            product_price.append(pharmeasy['product_price'][str(i)]);
            product_image.append(pharmeasy['product_image'][str(i)]);
            product_type.append(pharmeasy['product_type'][str(i)])
            manufacture.append('no one');
            isAvailable.append(pharmeasy['isAvailable'][str(i)]);
            site.append(str('https://pharmeasy.in/search/all?name='+pharmeasy['product_name'][str(i)]));
        if i < medliferows:
            product_sitename.append('MedLife');
            product_name.append(medlife['product_name'][str(i)]);
            product_price.append(medlife['product_price'][str(i)]);
            product_image.append(medlife['product_image'][str(i)]);
            product_type.append(medlife['product_type'][str(i)])
            manufacture.append(medlife['manufacture'][str(i)]);
            isAvailable.append(medlife['isAvailable'][str(i)]);
            site.append(str('https://www.medlife.com/'+medlife['product_name'][str(i)]+'/otc/'+medlife['product_id'][str(i)]+'?fcId=DEFAULT'));
        if i < netmedsrows:
            product_sitename.append('NetMeds');
            product_name.append(netmeds['product_name'][str(i)]);
            product_price.append(netmeds['product_price'][str(i)][4:]);
            product_image.append(netmeds['product_image'][str(i)]);
            product_type.append(netmeds['product_type'][str(i)])
            manufacture.append(netmeds['manufacture'][str(i)]);
            isAvailable.append('available');
            site.append(str('https://www.netmeds.com/catalogsearch/result?q='+netmeds['product_name'][str(i)]))
        if i<= onemgrows:
            product_sitename.append('1Mg');
            product_name.append(onemg['product_name'][str(i)]);
            product_price.append(onemg['product_price'][str(i)]);
            product_image.append(onemg['product_image'][str(i)]);
            product_type.append(onemg['product_type'][str(i)])
            manufacture.append(onemg['manufacture'][str(i)]);
            isAvailable.append(onemg['isAvailable'][str(i)]);
            site.append(str('https://www.1mg.com/search/all?name='+onemg['product_name'][str(i)]));
    pr_sitename=product_sitename;
    pr_name = product_name;
    pr_type = product_type;
    pr_image = product_image;
    pr_price = product_price;
    manufacture2 = manufacture;
    site2 = site;
    isAvailable2 = isAvailable;
    myProducts={
        'product_sitename':product_sitename[0:10],
        'product_name':product_name[0:10],
        'product_price':product_price[0:10],
        'product_image':product_image[0:10],
        'manufacture':manufacture[0:10],
        'product_type':product_type[0:10],
        'isAvailable':isAvailable[0:10],
        'site':site[0:10],
        'nextPage':1,
        'lastPage':int(len(product_name)/10),
        'start':0,
        'end':9,
    }
    return render(request,'index.html',myProducts)
def next(request,id):
    global pr_name, pr_image, pr_price, pr_type, manufacture2, isAvailable2, label2, site2
    if int(len(pr_name))>((int(id)*10)+10):
        myProducts={
            'product_sitename':pr_sitename[(int(id)*10):((int(id)*10)+10)],
            'product_name':pr_name[(int(id)*10):((int(id)*10)+10)],
            'product_price':pr_price[(int(id)*10):((int(id)*10)+10)],
            'product_image':pr_image[(int(id)*10):((int(id)*10)+10)],
            'manufacture':manufacture2[(int(id)*10):((int(id)*10)+10)],
            'product_type':pr_type[(int(id)*10):((int(id)*10)+10)],
            'isAvailable': isAvailable2[(int(id)*10):((int(id)*10)+10)],
            'site':site2[(int(id)*10):((int(id)*10)+10)],
            'start': 0,
            'end': 9,
            'lastPage':int(len(pr_name)/10),
            'nextPage':id+1,
        }
    else:
        if id>int(len(p_name)/10):
            id=int(len(p_name)/10)
        myProducts={
        'product_sitename':pr_sitename[(int(id)*10):int(len(pr_name))],
        'product_name':pr_name[(int(id)*10):int(len(pr_name))],
        'product_price':pr_price[(int(id)*10):int(len(pr_name))],
        'product_image':pr_image[(int(id)*10):int(len(pr_name))],
        'manufacture':manufacture2[(int(id)*10):int(len(pr_name))],
        'product_type':pr_type[(int(id)*10):int(len(pr_name))],
        'isAvailable': isAvailable2[(int(id)*10):int(len(pr_name))],
        'site':site2[(int(id)*10):int(len(pr_name))],
        'start': 0,
        'end': 9,
        'lastPage':int(id),
        'nextPage':id,
    }

    return render(request,'index.html',myProducts)

class ProductListView(ListView):
    netmeds = pd.read_csv('netmedsproduct.csv');

    myProducts = {
        'product_name': netmeds['product_name'],
        'product_price': netmeds['product_price'],
        'product_image': netmeds['product_image'],
        'manufacture': netmeds['manufacture'],
        'product_type': netmeds['product_type'],
        'length':20537
    }
    template_name = 'blog/home.html'
    context_object_name = myProducts # it used to pass all posts as key and value pair of dictionary so we can use in home.html page
    ordering = ['product_name']
    paginate_by = 4

def search(request):
    searchValue=request.GET.get('search');
    # pr_name=product_name;
    # print(product_name)
    global p_sitename,p_name, p_image, p_price, p_type, manufacture1, isAvailable1, label1, site1
    # global product_name1,product_image,product_price,product_type,manufacture,isAvailable,label,site
    product_sitename=[]
    product_name=[]
    product_price=[]
    product_image=[]
    product_type=[]
    manufacture=[]
    isAvailable=[]
    label=[]
    site=[]
    netmeds = pd.read_csv('netmedsproduct.csv');
    netmeds['site'] = str('https://www.netmeds.com/catalogsearch/result?q=')
    netmeds['product_name'].fillna(' ');
    netmeds['product_type'].fillna(' ');
    netmeds['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    netmeds['isAvailable']='available';
    netmeds['manufacture'].fillna('no one');
    netmedsrows = len(netmeds)
    # netmeds.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    netmeds.to_json('netmedsproduct.json');
    with open('netmedsproduct.json') as myfile:
        data = myfile.read()
    netmeds = json.loads(data)
    onemg = pd.read_csv('onemgproduct.csv');
    onemg['site'] = str('https://www.1mg.com/search/all?name=')
    onemg['product_name'].fillna(' ');
    onemg['product_type'].fillna(' ');
    onemg['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    onemg['isAvailable'].fillna('not available');
    onemg['manufacture'].fillna('no one');
    onemgrows = len(onemg)
    # onemg.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    # onemg.to_csv('onemgproduct.csv');
    # onemg = pd.read_csv('onemgproduct.csv');
    # onemg.set_index('product_name', inplace=True)
    onemg.to_json('onemgproduct.json');
    with open('onemgproduct.json') as myfile:
        data = myfile.read()
    onemg = json.loads(data)
    #onemg.to_json('onemgproduct.json');
    pharmeasy = pd.read_csv('PharmEasyProducts.csv');
    pharmeasyrows = len(pharmeasy);
    pharmeasy['site']=str('https://pharmeasy.in/search/all?name=')
    pharmeasy['product_name'].fillna(' ');
    pharmeasy['product_type'].fillna(' ');
    pharmeasy['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    pharmeasy['isAvailable'].fillna('not available');
    pharmeasy['manufacture']='no one';
    # pharmeasy.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    pharmeasy.to_json('pharmeasyproduct.json');
    with open('pharmeasyproduct.json') as myfile:
        data = myfile.read()
    pharmeasy = json.loads(data)
    medlife = pd.read_csv('MedLifeProducts.csv');
    medliferows = len(medlife);
    medlife['site']='https://medlife.com/'
    medlife['product_name'].fillna(' ');
    medlife['product_type'].fillna(' ');
    medlife['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    medlife['isAvailable'].fillna('not available');
    medlife['manufacture'].fillna('no one');
    # medlife.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    medlife.to_json('medlifeproduct.json');
    with open('medlifeproduct.json') as myfile:
        data = myfile.read()
    medlife = json.loads(data)
    low=0;
    high=onemgrows
    demostr="2345.60"
    print(float(demostr))
    # while low<=high:
    #     mid=low+mid//2;
    #     if str(searchValue).lower() in str(pharmeasy['product_name'][str(mid)]).lower():
    #         print("got it")
    #         product_name.append(pharmeasy['product_name'][str(mid)]);
    #         product_price.append(pharmeasy['product_price'][str(mid)]);
    #         if pharmeasy['product_image'][str(mid)]!=None:
    #             product_image.append(pharmeasy['product_image'][str(mid)]);
    #         else:
    #             product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    #         product_type.append(pharmeasy['product_type'][str(mid)])
    #         manufacture.append('no one');
    #         isAvailable.append(pharmeasy['isAvailable'][str(mid)]);
    #         site.append(str('https://pharmeasy.in/search/all?name='+pharmeasy['product_name'][str(mid)]));
    #         product_sitename.append('PharmEasy');
            
    #     elif str(searchValue)[0]<str(pharmeasy['product_name'][str(mid)][0]):
    #         high=mid-1;
    #     else:
    #         low=mid+1;
        
    for i in range(0,onemgrows):
        if i < pharmeasyrows:
            print(pharmeasy['product_name'][str(i)])
            if str(searchValue).lower() in str(pharmeasy['product_name'][str(i)]).lower():
                product_name.append(pharmeasy['product_name'][str(i)]);
                product_price.append(float(pharmeasy['product_price'][str(i)]));
                if pharmeasy['product_image'][str(i)]!=None:
                    product_image.append(pharmeasy['product_image'][str(i)]);
                else:
                    product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
                product_type.append(pharmeasy['product_type'][str(i)])
                manufacture.append('no one');
                isAvailable.append(pharmeasy['isAvailable'][str(i)]);
                site.append(str('https://pharmeasy.in/search/all?name='+pharmeasy['product_name'][str(i)]));
                product_sitename.append('PharmEasy');
            if str(searchValue).lower() in str(pharmeasy['product_type'][str(i)]).lower():
                product_name.append(pharmeasy['product_name'][str(i)]);
                product_price.append(float(pharmeasy['product_price'][str(i)]));
                if pharmeasy['product_image'][str(i)]!=None:
                    product_image.append(pharmeasy['product_image'][str(i)]);
                else:
                    product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
                product_type.append(pharmeasy['product_type'][str(i)])
                manufacture.append('no one');
                isAvailable.append(pharmeasy['isAvailable'][str(i)]);
                site.append(str('https://pharmeasy.in/search/all?name='+pharmeasy['product_name'][str(i)]));
                product_sitename.append('PharmEasy');
        if i < medliferows:
            print(medlife['product_name'][str(i)])
            if str(searchValue).lower() in str(medlife['product_name'][str(i)]).lower():
                product_name.append(medlife['product_name'][str(i)]);
                product_price.append(float(medlife['product_price'][str(i)]));
                if medlife['product_image'][str(i)]!=None:
                    product_image.append(medlife['product_image'][str(i)]);
                else:
                    product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
                product_type.append(medlife['product_type'][str(i)])
                manufacture.append('no one');
                isAvailable.append(medlife['isAvailable'][str(i)]);
                site.append(str('https://www.medlife.com/'+medlife['product_name'][str(i)]+'/otc/'+medlife['product_id'][str(i)]+'?fcId=DEFAULT'));
                product_sitename.append('MedLife');
            if str(searchValue).lower() in str(medlife['product_type'][str(i)]).lower():
                product_name.append(medlife['product_name'][str(i)]);
                product_price.append(float(medlife['product_price'][str(i)]));
                if medlife['product_image'][str(i)] != None:
                    product_image.append(medlife['product_image'][str(i)]);
                else:
                    product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
                product_type.append(medlife['product_type'][str(i)])
                manufacture.append(medlife['manufacture'][str(i)]);
                isAvailable.append(medlife['isAvailable'][str(i)]);
                site.append(str('https://www.medlife.com/'+medlife['product_name'][str(i)]+'/otc/'+medlife['product_id'][str(i)]+'?fcId=DEFAULT'));
                product_sitename.append('MedLife');
        if i < netmedsrows:
            if str(searchValue).lower() in str(netmeds['product_name'][str(i)]).lower():
                product_name.append(netmeds['product_name'][str(i)]);
                price=str(netmeds['product_price'][str(i)][4:])
                # price.pop(',');
                price=str(price)
                product_price.append(str(price));
                if netmeds['product_image'][str(i)] != None:
                    product_image.append(netmeds['product_image'][str(i)]);
                else:
                    product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
                # product_image.append(netmeds['product_image'][str(i)]);
                product_type.append(netmeds['product_type'][str(i)])
                manufacture.append(str(netmeds['manufacture'][str(i)][4:]));
                isAvailable.append('available');
                site.append(str('https://www.netmeds.com/catalogsearch/result?q='+netmeds['product_name'][str(i)]));
                product_sitename.append('NetMeds');
            if str(searchValue).lower() in str(netmeds['product_type'][str(i)]).lower():
                product_name.append(netmeds['product_name'][str(i)]);
                price=str(netmeds['product_price'][str(i)][4:])
                # price.pop(',');
                price=str(price)
                product_price.append(str(price));
                if netmeds['product_image'][str(i)] != None:
                    product_image.append(netmeds['product_image'][str(i)]);
                else:
                    product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
                # product_image.append(netmeds['product_image'][str(i)]);
                product_type.append(netmeds['product_type'][str(i)])
                manufacture.append(netmeds['manufacture'][str(i)][4:]);
                isAvailable.append('available');
                site.append(str('https://www.netmeds.com/catalogsearch/result?q='+netmeds['product_name'][str(i)]));
                product_sitename.append('NetMeds');
        if i<= onemgrows:
            if str(searchValue).lower() in str(onemg['product_name'][str(i)]).lower():
                product_name.append(onemg['product_name'][str(i)]);
                product_price.append(float(onemg['product_price'][str(i)]));
                if onemg['product_image'][str(i)] != None:
                    product_image.append(onemg['product_image'][str(i)]);
                else:
                    product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
                # product_image.append(onemg['product_image'][str(i)]);
                product_type.append(onemg['product_type'][str(i)])
                manufacture.append(onemg['manufacture'][str(i)]);
                isAvailable.append(onemg['isAvailable'][str(i)]);
                site.append(str('https://www.1mg.com/search/all?name='+onemg['product_name'][str(i)]))
                product_sitename.append('1Mg');
            if str(searchValue).lower() in str(onemg['product_type'][str(i)]).lower():
                product_name.append(onemg['product_name'][str(i)]);
                product_price.append(float(onemg['product_price'][str(i)]));
                product_image.append(onemg['product_image'][str(i)]);
                product_type.append(onemg['product_type'][str(i)])
                manufacture.append(onemg['manufacture'][str(i)]);
                isAvailable.append(onemg['isAvailable'][str(i)]);
                site.append(str('https://www.1mg.com/search/all?name='+onemg['product_name'][str(i)]))
                product_sitename.append('1Mg');
    for i in range(len(product_name)):
        label.append('no');

    # for best price label logic
    id=0
    while id<=(len(product_name)-1):
        allWords=product_name[id].split(' ');
        firstWord=allWords[0]
        for i in range(1,int(len(product_name))):  
            if product_name[id][0:len(firstWord)] in product_name[i]:
                prod_price=str(product_price[id]);
                comaIndex=prod_price.find(',');
                if comaIndex!=-1:
                    product_price[id]=str(prod_price[0:int(comaIndex)])+str(prod_price[int(comaIndex+1):])
                prod_price=str(product_price[i]);
                comaIndex=prod_price.find(',');
                if comaIndex!=-1:
                    product_price[i]=str(prod_price[0:int(comaIndex)])+str(prod_price[int(comaIndex+1):])
                if float(product_price[id])<float(product_price[i]) and id!=i:
                    label[i]="no";
                    label[id]="Best Price";
                if re.findall('[0-9]+m',product_name[id])==re.findall('[0-9]+m',product_name[i]):
                    prod_price=str(product_price[id]);
                    comaIndex=prod_price.find(',');
                    if comaIndex!=-1:
                        product_price[id]=str(prod_price[0:int(comaIndex)])+str(prod_price[int(comaIndex+1):])
                    prod_price=str(product_price[i]);
                    comaIndex=prod_price.find(',');
                    if comaIndex!=-1:
                        product_price[i]=str(prod_price[0:int(comaIndex)])+str(prod_price[int(comaIndex+1):])
                    if float(product_price[id])<float(product_price[i]) and id!=i:
                        label[i]="no";
                        label[id]="Best Price";
            # elif product_name[id][0:len(firstWord)] in product_name[i] and re.findall('[0-9]+ml',product_name[id])==re.findall('[0-9]+ml',product_name[i]):
            #     if int(product_price[id])<int(product_price[i]) and id!=i:
            #         label[i]="no";
            #         label[id]="Best Price";
            #     if int(product_price[id])>int(product_price[i]):
                    # label[id]="not";
                    # label[i]="Best Price";
        id = id + 1;
    
    print(label)
    p_sitename=product_sitename;
    p_name=product_name;
    p_type=product_type;
    p_image=product_image;
    p_price=product_price;
    manufacture1=manufacture;
    site1=site;
    isAvailable1=isAvailable;
    label1=label;
    flag=False
    nextPage=1;

    end=len(product_name);
    if len(product_name)>10:
        myProducts = {
            'product_sitename':product_sitename[0:10],
            'product_name': product_name[0:10],
            'product_price': product_price[0:10],
            'product_image': product_image[0:10],
            'manufacture': manufacture[0:10],
            'product_type': product_type[0:10],
            'isAvailable':isAvailable[0:10],
            'label':label[0:10],
            'site':site[0:10],
            'nextPage': nextPage,
            'start': 0,
            'end':10,
            'lastPage':int(len(product_name)/10),
        }
    else:
        myProducts = {
            'product_sitename':product_sitename[0:len(product_name)],
            'product_name': product_name[0:len(product_name)],
            'product_price': product_price[0:len(product_name)],
            'product_image': product_image[0:len(product_name)],
            'manufacture': manufacture[0:len(product_name)],
            'product_type': product_type[0:len(product_name)],
            'isAvailable': isAvailable[0:len(product_name)],
            'label': label[0:len(product_name)],
            'site': site[0:len(product_name)],
            'nextPage':-1,
            'start': 0,
            'end': int(len(product_name)),
            'lastPage':0,
        }
    return render(request, 'search.html', myProducts)

#
def search1(request,id):
    # global pr_name
    global p_sitename,p_name,p_image,p_price,p_type,manufacture1,isAvailable1,label1,site1
    flag = False
    nextPage = id;

    myProducts={}
    pr_len=len(p_name)
    if (len(p_name)>=((int(id)*10)+10)):
        flag=True;
    if id>int(len(p_name)/10):
        id=int(len(p_name)/10)
    if flag==True:
        myProducts = {
        'product_sitename':p_sitename[(int(id)*10):((int(id)*10)+10)],
        'product_name': p_name[(int(id)*10):((int(id)*10)+10)],
        'product_price': p_price[(int(id)*10):((int(id)*10)+10)],
        'product_image': p_image[(int(id)*10):((int(id)*10)+10)],
        'manufacture': manufacture1[(int(id)*10):((int(id)*10)+10)],
        'product_type': p_type[(int(id)*10):((int(id)*10)+10)],
        'isAvailable': isAvailable1[(int(id)*10):((int(id)*10)+10)],
        'label': label1[(int(id)*10):((int(id)*10)+10)],
        'site': site1[(int(id)*10):((int(id)*10)+10)],
        'nextPage': int(id)+1,
        'start': (10*int(id)),
        'end': 10*int(id)+10,
        'lastPage':int(len(p_name)/10)
        }
    else:
        myProducts = {
            'product_sitename': p_sitename[(int(id)*10):pr_len],
            'product_name': p_name[(int(id) * 10):pr_len],
            'product_price': p_price[(int(id) * 10):pr_len],
            'product_image': p_image[(int(id) * 10):pr_len],
            'manufacture': manufacture1[(int(id) * 10):pr_len],
            'product_type': p_type[(int(id) * 10):pr_len],
            'isAvailable': isAvailable1[(int(id) * 10):pr_len],
            'label': label1[(int(id) * 10):pr_len],
            'site': site1[(int(id) * 10):pr_len],
            'nextPage':int(id)+1,
            'start': (10 * int(id)),
            'end': ((10 *int(id)) + 10),
            'lastPage':int(id)
        }
    return render(request, 'search.html', myProducts)

