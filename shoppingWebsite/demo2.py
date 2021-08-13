from django.shortcuts import render,redirect, get_object_or_404
import numpy as np
import pandas as pd
import json
import csv
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
p_name=[];
p_image=[];
p_price=[];
p_type=[];
manufacture1=[];
isAvailable1=[];
label1=[];
site1=[]
pr_name=[];
pr_image=[];
pr_price=[];
pr_type=[];
manufacture2=[];
isAvailable2=[];
label2=[];
site2=[]
def index(request):
    global pr_name, pr_image, pr_price, pr_type, manufacture2, isAvailable2, label2, site2
    pharmeasy=pd.read_csv('PharmEasyProducts.csv');
    pharmeasy.sort_values(['product_name'],axis=0,ascending=True,inplace=True)
    pharmeasyrows=len(pharmeasy)
    pharmeasy.to_json('pharmeasyproduct.json');
    with open('pharmeasyproduct.json') as myfile:
        data=myfile.read()
    pharmeasy = json.loads(data)
    netmeds=pd.read_csv('netmedsproduct.csv');
    netmeds.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    netmedsrows=len(netmeds)
    netmeds.to_json('netmedsproduct.json');
    with open('netmedsproduct.json') as myfile:
        data = myfile.read()
    netmeds = json.loads(data)
    onemg = pd.read_csv('onemgproduct.csv');
    onemgrows=len(onemg)
    onemg.sort_values(['product_name'], axis=0, ascending=True, inplace=True)
    onemg.to_json('onemgproduct.json');
    with open('onemgproduct.json') as myfile:
        data = myfile.read()
    onemg = json.loads(data)
    product_name=[]
    product_price=[]
    product_image=[]
    product_type=[]
    manufacture=[]
    isAvailable=[]
    site=[]
    for i in range(0,onemgrows):
        if i < pharmeasyrows:
            product_name.append(pharmeasy['product_name'][str(i)]);
            product_price.append(pharmeasy['product_price'][str(i)]);
            product_image.append(pharmeasy['product_image'][str(i)]);
            product_type.append(pharmeasy['product_type'][str(i)])
            manufacture.append('no one');
            isAvailable.append(pharmeasy['isAvailable'][str(i)]);
            site.append('https://pharmeasy.in/search/all?name=');
        if i < netmedsrows:
            product_name.append(netmeds['product_name'][str(i)]);
            product_price.append(netmeds['product_price'][str(i)][4:]);
            product_image.append(netmeds['product_image'][str(i)]);
            product_type.append(netmeds['product_type'][str(i)])
            manufacture.append(netmeds['manufacture'][str(i)]);
            isAvailable.append('available');
            site.append('https://www.netmeds.com/catalogsearch/result?q=')
        if i<= onemgrows:
            product_name.append(onemg['product_name'][str(i)]);
            product_price.append(onemg['product_price'][str(i)]);
            product_image.append(onemg['product_image'][str(i)]);
            product_type.append(onemg['product_type'][str(i)])
            manufacture.append(onemg['manufacture'][str(i)]);
            isAvailable.append(onemg['isAvailable'][str(i)]);
            site.append('https://www.1mg.com/search/all?name=')
    pr_name = product_name;
    pr_type = product_type;
    pr_image = product_image;
    pr_price = product_price;
    manufacture2 = manufacture;
    site2 = site;
    isAvailable2 = isAvailable;
    # try:
    #     for item in pharmeasy['product_name'].items():
    #         product_name.append(item);
    #     for item in pharmeasy['product_price'].items():
    #         product_price.append(item);
    #     for item in pharmeasy['product_image'].items():
    #         product_image.append(item);
    #     for item in pharmeasy['product_type'].items():
    #         product_type.append(item);
    #     for item in pharmeasy['product_name'].items():
    #         manufacture.append('no one');
    #     for item in pharmeasy['isAvailable'].items():
    #         isAvailable.append(item);
    # except:
    #     pass
    myProducts={
        'product_name':product_name[0:20],
        'product_price':product_price[0:20],
        'product_image':product_image[0:20],
        'manufacture':manufacture[0:20],
        'product_type':product_type[0:20],
        'isAvailable':isAvailable[0:20],
        'site':site[0:20],
        'nextPage':1,
        'start':0,
        'end':19,
    }
    return render(request,'index.html',myProducts)
def next(request,id):
    global pr_name, pr_image, pr_price, pr_type, manufacture2, isAvailable2, label2, site2
    # netmeds = pd.read_csv('PharmEasyProducts.csv');
    # netmeds.to_json('pharmeasyproduct.json');
    # with  open('pharmeasyproduct.json') as myfile:
    #     data = myfile.read()
    # netmeds=json.loads(data)
    # product_name=[]
    # product_price=[]
    # product_image=[]
    # product_type=[]
    # manufacture=[]
    # isAvailable=[]
    # try:
    #     for item in netmeds['isAvailable'].items():
    #         if str(item) != 'undefined' or str(item) != 'nan' or str(item)!='':
    #             isAvailable.append(item);
    #         else:
    #             isAvailable.append('False');
    #     for item in netmeds['product_name'].items():
    #         if str(item) != 'undefined' or str(item) != 'nan' or str(item)!='':
    #             product_name.append(item);
    #         else:
    #             product_name.append('no item');
    #     for item in netmeds['product_price'].items():
    #         if str(item) != 'undefined' or str(item) != 'nan' or str(item)!='':
    #             product_price.append(item);
    #         else:
    #             product_price.append('no item');
    #     for item in netmeds['product_image'].items():
    #         if str(item) != 'undefined' or str(item) != 'nan' or str(item)!='':
    #             product_image.append(item);
    #         else:
    #             product_image.append('no item');
    #     for item in netmeds['product_type'].items():
    #         if str(item) != 'undefined' or str(item) != 'nan' or str(item)!='':
    #             product_type.append(item);
    #         else:
    #             product_type.append('no item');
    #
    #     for item in netmeds['product_name'].items():
    #         if str(item) != 'undefined' or str(item) != 'nan' or str(item)!='':
    #             manufacture.append('no one')
    #         else:
    #             manufacture.append('no item');
    # except:
    #     pass
    myProducts={
        'product_name':pr_name[(int(id)*20):((int(id)*20)+20)],
        'product_price':pr_price[(int(id)*20):((int(id)*20)+20)],
        'product_image':pr_image[(int(id)*20):((int(id)*20)+20)],
        'manufacture':manufacture2[(int(id)*20):((int(id)*20)+20)],
        'product_type':pr_type[(int(id)*20):((int(id)*20)+20)],
        'isAvailable': isAvailable2[(int(id)*20):((int(id)*20)+20)],
        'site':site2[(int(id)*20):((int(id)*20)+20)],
        'start': 0,
        'end': 19,
        'nextPage':id+1,
    }
    return render(request,'index.html',myProducts)

# def home(request):
#     try:
#         Friends = []
#         if str(Cuser.profile.friends) != "-":
#             Fri = literal_eval(Cuser.profile.friends)
#             print(type(Fri))
#             for item in Fri.items():
#                 Friends.append(item)
#         else:
#             Fri = {}
#         context = {
#             'posts': Post.objects.all(),
#             'Friends':Friends
#         }
#         paginate_by = 4
#         return render(request, 'blog/home.html', context)
#     except:
#         context = {
#             'posts': Post.objects.all(),
#             'Friends':'null'
#         }
#         return render(request, 'blog/home.html', context)

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
    product_name=request.GET.get('search');
    # pr_name=product_name;
    # print(product_name)
    global p_name, p_image, p_price, p_type, manufacture1, isAvailable1, label1, site1
    # global product_name1,product_image,product_price,product_type,manufacture,isAvailable,label,site
    product_name1=[]
    product_price=[]
    product_image=[]
    product_type=[]
    manufacture=[]
    isAvailable=[]
    label=[]
    site=[]
    netmeds1 = pd.read_csv('netmedsproduct.csv');
    netmeds1['site'] = 'https://www.netmeds.com/catalogsearch/result?q='
    netmeds1['product_name'].fillna(' ');
    netmeds1['product_type'].fillna(' ');
    netmeds1['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    netmeds1['isAvailable']='available';
    netmeds1['manufacture'].fillna('no one');
    # netmeds.set_index('product_name',inplace=True)
    # netmeds.to_json('netmedsproduct.json');
    #netmeds.to_json('netmedsproduct.json');
    onemg = pd.read_csv('onemgproduct.csv');
    onemg['site'] = 'https://www.1mg.com/search/all?name='
    onemg['product_name'].fillna(' ');
    onemg['product_type'].fillna(' ');
    onemg['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    onemg['isAvailable'].fillna('not available');
    onemg['manufacture'].fillna('no one');
    # onemg.to_csv('onemgproduct.csv');
    # onemg = pd.read_csv('onemgproduct.csv');
    # onemg.set_index('product_name', inplace=True)
    # onemg.to_json('onemgproduct.json');
    #onemg.to_json('onemgproduct.json');
    pharmeasy = pd.read_csv('PharmEasyProducts.csv');
    pharmeasy['site']='https://pharmeasy.in/search/all?name='
    pharmeasy['product_name'].fillna(' ');
    pharmeasy['product_type'].fillna(' ');
    pharmeasy['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    pharmeasy['isAvailable'].fillna('not available');
    pharmeasy['manufacture']='no one';
    # pharmeasy.to_csv('PharmEasyProducts.csv');
    # type=False;
    # name=False;
    # pharmeasy.to_csv('PharmEasyProducts.csv');
    # pharmeasy = pd.read_csv('PharmEasyProducts.csv');
    # pharmeasy.set_index('product_name', inplace=True)
    # pharmeasy.to_json('pharmeasyproduct.json');
    #pharmeasy.to_json('PharmEasyProducts.json');
    netmeds1['product_name']=netmeds1['product_name'].str.lower();
    netmedsProducts_name= (netmeds1['product_name'].str.contains(product_name.lower()));
    print("netmeds",netmedsProducts_name)
    onemg['product_name'] = onemg['product_name'].str.lower();
    onemgProducts_name= (onemg['product_name'].str.contains(product_name.lower()));
    print("one",onemgProducts_name)
    pharmeasy['product_name'] = pharmeasy['product_name'].str.lower();
    pharmeasyProducts_name=(pharmeasy['product_name'].str.contains(product_name.lower()));
    print("pharm", pharmeasyProducts_name)

    pharmeasy['product_type'] = pharmeasy['product_type'].str.lower();
    onemg['product_type'] = onemg['product_type'].str.lower();
    netmeds1['product_type'] = netmeds1['product_type'].str.lower();
    netmedsProducts_type = (netmeds1['product_type'].str.contains(product_name.lower()));
    print(netmedsProducts_type)
    onemgProducts_type = (onemg['product_type'].str.contains(product_name.lower()));
    print(onemgProducts_type)
    pharmeasyProducts_type = (pharmeasy['product_type'].str.contains(product_name.lower()));
    print(pharmeasyProducts_type)
    df=pd.DataFrame();
    try:
        # print('netmeds',netmeds1.loc[netmedsProducts_name,'product_name'].values)
        for item in netmeds1.loc[netmedsProducts_name,'product_name'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_name1.append(str(item))
            # print("net",netmeds1.loc[netmedsProducts_name,"product_name"].values)
        for item in netmeds1.loc[netmedsProducts_name,'product_price'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_price.append(str(item[4:]))
        print('netmeds images', netmeds1.loc[netmedsProducts_name,'product_image'].values)
        for item in netmeds1.loc[netmedsProducts_name,'product_image'].values:
            # print(item)
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_image.append(str(item))
            elif str(item) == '':
                product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
        for item in netmeds1.loc[netmedsProducts_name,'product_type'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_type.append(str(item))
        for item in netmeds1.loc[netmedsProducts_name,'isAvailable'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                isAvailable.append(str(item));
        for item in netmeds1.loc[netmedsProducts_name, 'manufacture'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                manufacture.append(str(item))
        for item in netmeds1.loc[netmedsProducts_name, 'product_name'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                site.append('https://www.netmeds.com/catalogsearch/result?q=');
    except:
        pass
    try:
        # print('pharmeasy',pharmeasy.loc[pharmeasyProducts_name,'product_name'].values)
        for item in pharmeasy.loc[pharmeasyProducts_name, 'product_name'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_name1.append(str(item))
        # print("pharm",pharmeasy.loc[pharmeasyProducts_name, 'product_name'].values)
        for item in pharmeasy.loc[pharmeasyProducts_name, 'product_price'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_price.append(str(item))
        print('phameasy images',pharmeasy.loc[pharmeasyProducts_name,'product_image'].values)
        for item in pharmeasy.loc[pharmeasyProducts_name,'product_image'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_image.append(str(item))
        for item in pharmeasy.loc[pharmeasyProducts_name, 'isAvailable'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                isAvailable.append(str(item))
        for item in pharmeasy.loc[pharmeasyProducts_name, 'product_type'].values:
            if str(item) != 'nan' and str(item) != 'undefined' and str(item)!='':
                product_type.append(str(item))
        for item in pharmeasy.loc[pharmeasyProducts_name, 'manufacture'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                manufacture.append(str(item));
        for item in pharmeasy.loc[pharmeasyProducts_name, 'site'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                site.append(str(item));
    except:
        pass
    try:
        # print('onemg',onemg.loc[onemgProducts_name, 'product_name'].values)
        for item in onemg.loc[onemgProducts_name, 'product_name'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_name1.append(str(item))
        # print("onemg",onemg.loc[onemgProducts_name, 'product_name'].values)
        for item in onemg.loc[onemgProducts_name, 'product_price'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_price.append(str(item))
        print('onemg images',onemg.loc[onemgProducts_name, 'product_image'].values)
        for item in onemg.loc[onemgProducts_name, 'product_image'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
                product_image.append(str(item))
            elif str(item) == '':
                product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
        for item in onemg.loc[onemgProducts_name, 'isAvailable'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                isAvailable.append(str(item))
        for item in onemg.loc[onemgProducts_name, 'product_type'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_type.append(str(item))
        for item in onemg.loc[onemgProducts_name, 'manufacture'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                manufacture.append(str(item))
        for item in onemg.loc[onemgProducts_name, 'site'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                site.append(str(item))
    except:
        pass;
    try:
        for item in netmeds1.loc[netmedsProducts_type,'product_name'].values:
            if str(item) != 'undefined' and str(item)!='nan' and str(item)!='':
                product_name1.append(str(item))
        # print("netmeds product",netmeds1.loc[netmedsProducts_type,'product_name'].values)
        for item in netmeds1.loc[netmedsProducts_type,'product_price'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_price.append(str(item[4:]))
        # print("netmeds product image", netmeds1.loc[netmedsProducts_type, 'product_image'].values);
        for item in netmeds1.loc[netmedsProducts_type,'product_image'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_image.append(str(item))
            elif str(item)=='':
                product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
        for item in netmeds1.loc[netmedsProducts_type,'product_type'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_type.append(str(item))
        for item in netmeds1.loc[netmedsProducts_type,'isAvailable'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                isAvailable.append(str(item))
        for item in netmeds1.loc[netmedsProducts_type,'manufacture'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                manufacture.append(str(item))
        for item in netmeds1.loc[netmedsProducts_type,'product_type'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                site.append('https://www.netmeds.com/catalogsearch/result?q=');
    except:
        pass
    try:
        for item in pharmeasy.loc[pharmeasyProducts_type,'product_name'].values:
            if str(item) != 'undefined' and str(item)!='nan' and str(item)!='':
                product_name1.append(str(item))
        print("pharmeasy productname",pharmeasy.loc[pharmeasyProducts_name,'product_name'].values)
        for item in pharmeasy.loc[pharmeasyProducts_type,'product_price'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_price.append(str(item))
        for item in pharmeasy.loc[pharmeasyProducts_type,'product_image'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_image.append(str(item))
            elif str(item)=='':
                product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
        for item in pharmeasy.loc[pharmeasyProducts_type,'isAvailable'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                isAvailable.append(str(item))
        for item in pharmeasy.loc[pharmeasyProducts_type,'product_type'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_type.append(str(item))
        for item in pharmeasy.loc[pharmeasyProducts_type,'manufacture'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                manufacture.append(str(item))
        for item in pharmeasy.loc[pharmeasyProducts_type,'site'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                site.append(str(item));
    except:
        pass;
    try:
        for item in onemg.loc[onemgProducts_type,'product_name'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_name1.append(str(item))
        print("onemg product name of type",onemg.loc[onemgProducts_name,'product_name'].values)
        for item in onemg.loc[onemgProducts_type,'product_price'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_price.append(int(item))
        for item in onemg.loc[onemgProducts_type,'product_image'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_image.append(str(item))
            elif str(item)=='':
                product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
        for item in onemg.loc[onemgProducts_type,'isAvailable'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                isAvailable.append(str(item))
        for item in onemg.loc[onemgProducts_type,'product_type'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                product_type.append(str(item))
        for item in onemg.loc[onemgProducts_type,'manufacture'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                manufacture.append(str(item))
        for item in onemg.loc[onemgProducts_type,'site'].values:
            if str(item) != 'undefined' and str(item) != 'nan' and str(item)!='':
                site.append(item)
    except:
        pass;
    for i in range(len(product_name1)):
        label.append('no');
    id=0
    # for i in range(1,len(product_name1)):
    #     index=product_name1[id].find('mg');
    #     print(product_name1[id][0:int(index)])
    #     if product_name1[id][0:int(len(product_name1[id])/2)] in product_name1[i]:
    #         if int(product_price[id])<int(product_price[i]):
    #             label[i]="not";
    #             label[id]="Best Price";
    #             id = id + 1;
    #             i = 1;
    #         if int(product_price[id])>int(product_price[i]):
    #             label[id]="not";
    #             label[i]="Best Price";

    print(label)
    p_name=product_name1;
    p_type=product_type;
    p_image=product_image;
    p_price=product_price;
    manufacture1=manufacture;
    site1=site;
    isAvailable1=isAvailable;
    label1=label;
    flag=False
    nextPage=1;
    end=len(product_name1);
    if len(product_name1)>20:
        end=20;
    if end<20:
        nextPage=-1;
    # print('product_name',product_name1)
    # print('P_name',p_name)
    myProducts = {
        'product_name': product_name1[0:20],
        'product_price': product_price[0:20],
        'product_image': product_image[0:20],
        'manufacture': manufacture[0:20],
        'product_type': product_type[0:20],
        'isAvailable':isAvailable[0:20],
        'label':label[0:20],
        'site':site[0:20],
        'nextPage': nextPage,
        'start': 0,
        'end':end,
    }
    return render(request, 'search.html', myProducts)

#
def search1(request,id):
    # global pr_name
    global p_name,p_image,p_price,p_type,manufacture1,isAvailable1,label1,site1
    # global product_name1, product_image, product_price, product_type, manufacture, isAvailable, label, site
    # product_name = pr_name;
    # print(product_name)
    # netmeds = pd.read_csv('netmedsproduct.csv');
    # netmeds['site'] = 'https://www.netmeds.com/catalogsearch/result?q='
    # netmeds['product_name'].fillna(' ');
    # netmeds['product_type'].fillna(' ');
    # netmeds['product_image'].fillna(
    #     'https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    # # netmeds['isAvailable'].fillna('not available');
    # netmeds['manufacture'].fillna('no one');
    # # print(netmeds)
    # # netmeds.set_index('product_name',inplace=True)
    # # netmeds.to_json('netmedsproduct.json');
    # # netmeds.to_json('netmedsproduct.json');
    # onemg = pd.read_csv('onemgproduct.csv');
    # onemg['site'] = 'https://www.1mg.com/search/all?name='
    # onemg['product_name'].fillna(' ');
    # onemg['product_type'].fillna(' ');
    # onemg['product_image'].fillna(
    #     'https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    # onemg['isAvailable'].fillna('not available');
    # onemg['manufacture'].fillna('no one');
    # # onemg.to_csv('onemgproduct.csv');
    # # onemg = pd.read_csv('onemgproduct.csv');
    # # onemg.set_index('product_name', inplace=True)
    # # print(onemg)
    # # onemg.to_json('onemgproduct.json');
    # # onemg.to_json('onemgproduct.json');
    # pharmeasy = pd.read_csv('PharmEasyProducts.csv');
    # pharmeasy['site'] = 'https://pharmeasy.in/search/all?name='
    # pharmeasy['product_name'].fillna(' ');
    # pharmeasy['product_type'].fillna(' ');
    # pharmeasy['product_image'].fillna('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png');
    # pharmeasy['isAvailable'].fillna('not available');
    # # pharmeasy['manufacture'].fillna('no one');
    # # pharmeasy.to_csv('PharmEasyProducts.csv');
    # # print(pharmeasy)
    # type = False;
    # name = False;
    # # pharmeasy.to_csv('PharmEasyProducts.csv');
    # # pharmeasy = pd.read_csv('PharmEasyProducts.csv');
    # # pharmeasy.set_index('product_name', inplace=True)
    # # pharmeasy.to_json('pharmeasyproduct.json');
    # # pharmeasy.to_json('PharmEasyProducts.json');
    # netmeds['product_name'] = netmeds['product_name'].str.lower();
    # netmedsProducts_name = (netmeds['product_name'].str.contains(product_name.lower()));
    # print("netmeds", netmedsProducts_name)
    # onemg['product_name'] = onemg['product_name'].str.lower();
    # onemgProducts_name = (onemg['product_name'].str.contains(product_name.lower()));
    # print("one", onemgProducts_name)
    # pharmeasy['product_name'] = pharmeasy['product_name'].str.lower();
    # pharmeasyProducts_name = (pharmeasy['product_name'].str.contains(product_name.lower()));
    # print("pharm", pharmeasyProducts_name)
    #
    # pharmeasy['product_type'] = pharmeasy['product_type'].str.lower();
    # onemg['product_type'] = onemg['product_type'].str.lower();
    # netmeds['product_type'] = netmeds['product_type'].str.lower();
    # netmedsProduct_type = (netmeds['product_type'].str.contains(product_name.lower()));
    # onemgProducts_type = (onemg['product_type'].str.contains(product_name.lower()));
    # pharmeasyProducts_type = (pharmeasy['product_type'].str.contains(product_name.lower()));
    # df = pd.DataFrame();
    # try:
    #     print('netmeds', netmeds.loc[netmedsProducts_name, 'product_name'].values)
    #     for item in netmeds.loc[netmedsProducts_name, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_name1.append(str(item))
    #         # print("net",netmeds.loc[netmedsProducts_name,"product_name"].values)
    #     for item in netmeds.loc[netmedsProducts_name, 'product_price'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_price.append(int(item[4:]))
    #     print('netmeds images', netmeds.loc[netmedsProducts_name, 'product_image'].values)
    #     for item in netmeds.loc[netmedsProducts_name, 'product_image'].values:
    #         print(item)
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_image.append(str(item))
    #         elif str(item) == '':
    #             product_image.append(
    #                 'https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
    #     for item in netmeds.loc[netmedsProducts_name, 'product_type'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_type.append(str(item))
    #     for item in netmeds.loc[netmedsProducts_name, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             isAvailable.append('True');
    #     for item in netmeds.loc[netmedsProducts_name, 'manufacture'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             manufacture.append(str(item))
    #     for item in netmeds.loc[netmedsProducts_name, 'site'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             site.append(str(item))
    # except:
    #     pass
    # try:
    #     print('pharmeasy', pharmeasy.loc[pharmeasyProducts_name, 'product_name'].values)
    #     for item in pharmeasy.loc[pharmeasyProducts_name, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_name1.append(str(item))
    #     # print("pharm",pharmeasy.loc[pharmeasyProducts_name, 'product_name'].values)
    #     for item in pharmeasy.loc[pharmeasyProducts_name, 'product_price'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_price.append(int(item))
    #     print('phameasy images', pharmeasy.loc[pharmeasyProducts_name, 'product_image'].values)
    #     for item in pharmeasy.loc[pharmeasyProducts_name, 'product_image'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_image.append(str(item))
    #     for item in pharmeasy.loc[pharmeasyProducts_name, 'isAvailable'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             isAvailable.append(str(item))
    #     for item in pharmeasy.loc[pharmeasyProducts_name, 'product_type'].values:
    #         if str(item) != 'not available' and str(item) != 'nan' and str(item) != 'undefined':
    #             product_type.append(str(item))
    #     for item in pharmeasy.loc[pharmeasyProducts_name, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             manufacture.append('not given')
    #     for item in pharmeasy.loc[pharmeasyProducts_name, 'site'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             site.append(str(item));
    # except:
    #     pass
    # try:
    #     print('onemg', onemg.loc[onemgProducts_name, 'product_name'].values)
    #     for item in onemg.loc[onemgProducts_name, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             product_name1.append(str(item))
    #     # print("onemg",onemg.loc[onemgProducts_name, 'product_name'].values)
    #     for item in onemg.loc[onemgProducts_name, 'product_price'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             product_price.append(int(item))
    #     print('onemg images', onemg.loc[onemgProducts_name, 'product_image'].values)
    #     for item in onemg.loc[onemgProducts_name, 'product_image'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_image.append(str(item))
    #         elif str(item) == '':
    #             product_image.append(
    #                 'https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
    #     for item in onemg.loc[onemgProducts_name, 'isAvailable'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             isAvailable.append(str(item))
    #     for item in onemg.loc[onemgProducts_name, 'product_type'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             product_type.append(str(item))
    #     for item in onemg.loc[onemgProducts_name, 'manufacture'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             manufacture.append(str(item))
    #     for item in onemg.loc[onemgProducts_name, 'site'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             site.append(str(item))
    # except:
    #     pass
    # try:
    #     for item in netmeds.loc[netmedsProduct_type, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             product_name1.append(str(item))
    #     print("netmeds product", netmeds.loc[netmedsProducts_name, 'product_name'].values)
    #     for item in netmeds.loc[netmedsProduct_type, 'product_price'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan':
    #             product_price.append(int(item))
    #     print("netmeds product image", netmeds.loc[netmedsProducts_name, 'product_image'].values);
    #     for item in netmeds.loc[netmedsProduct_type, 'product_image'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_image.append(str(item))
    #     for item in netmeds.loc[netmedsProduct_type, 'product_type'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_type.append(str(item))
    #     for item in netmeds.loc[netmedsProduct_type, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             isAvailable.append('')
    #     for item in netmeds.loc[netmedsProduct_type, 'manufacture'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             manufacture.append(str(item))
    #     for item in netmeds.loc[netmedsProduct_type, 'site'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             site.append(item)
    # except:
    #     pass
    # try:
    #     for item in pharmeasy.loc[pharmeasyProducts_type, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_name1.append(str(item))
    #     print("pharmeasy productname", pharmeasy.loc[pharmeasyProducts_name, 'product_name'].values)
    #     for item in pharmeasy.loc[pharmeasyProducts_type, 'product_price'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_price.append(int(item))
    #     for item in pharmeasy.loc[pharmeasyProducts_type, 'product_image'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_image.append(str(item))
    #     for item in pharmeasy.loc[pharmeasyProducts_type, 'isAvailable'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             isAvailable.append(str(item))
    #     for item in pharmeasy.loc[pharmeasyProducts_type, 'product_type'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_type.append(str(item))
    #     for item in pharmeasy.loc[pharmeasyProducts_type, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             manufacture.append('no one')
    #     for item in pharmeasy.loc[pharmeasyProducts_type, 'site'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             site.append(item);
    # except:
    #     pass
    # try:
    #     for item in onemg.loc[onemgProducts_type, 'product_name'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_name1.append(str(item))
    #     print("onemg product name of type", onemg.loc[onemgProducts_name, 'product_name'].values)
    #     for item in onemg.loc[onemgProducts_type, 'product_price'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_price.append(int(item))
    #     for item in onemg.loc[onemgProducts_type, 'product_image'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_image.append(str(item))
    #         elif str(item) == '':
    #             product_image.append('https://res.cloudinary.com/du8msdgbj/image/upload/a_ignore,w_380,h_380,c_fit,q_auto,f_auto/v1479378261/blank_otc_uobogo.png')
    #     for item in onemg.loc[onemgProducts_type, 'isAvailable'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             isAvailable.append(str(item))
    #     for item in onemg.loc[onemgProducts_type, 'product_type'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             product_type.append(str(item))
    #     for item in onemg.loc[onemgProducts_type, 'manufacture'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             manufacture.append(str(item))
    #     for item in onemg.loc[onemgProducts_type, 'site'].values:
    #         if str(item) != 'undefined' and str(item) != 'nan' and str(item) != '':
    #             site.append(item)
    # except:
    #     pass;
    # label = []
    # for i in range(len(product_name1)):
    #     label.append('no');
    # j = 0
    # # for i in range(1, len(product_name1) - 1):
    #     index = product_name1[j].find('mg');
    #     print(index)
    #     if product_name1[j][0:15] in product_name1[i]:
    #         if product_price[j] < product_price[i]:
    #             # label[i]="no";
    #             label[j] = "Best Price";
    #         if product_price[j] > product_price[i]:
    #             # label[id]="no";
    #             label[i] = "Best Price";
    #         j = j + 1;
    #         i = j + 1;
    # # print(label)
    flag = False
    nextPage = id;
    myProducts={}
    pr_len=len(p_name)
    if (len(p_name)>=((int(id)*20)+20)):
        flag=True;
    if flag==True:
        myProducts = {
        'product_name': p_name[(int(id)*20):((int(id)*20)+20)],
        'product_price': p_price[(int(id)*20):((int(id)*20)+20)],
        'product_image': p_image[(int(id)*20):((int(id)*20)+20)],
        'manufacture': manufacture1[(int(id)*20):((int(id)*20)+20)],
        'product_type': p_type[(int(id)*20):((int(id)*20)+20)],
        'isAvailable': isAvailable1[(int(id)*20):((int(id)*20)+20)],
        'label': label1[(int(id)*20):((int(id)*20)+20)],
        'site': site1[(int(id)*20):((int(id)*20)+20)],
        'nextPage': int(id)+1,
        'start': (20*int(id)),
        'end': 20*int(id)+20,
        }
    else:
        myProducts = {
            'product_name': p_name[(int(id) * 20):pr_len],
            'product_price': p_price[(int(id) * 20):pr_len],
            'product_image': p_image[(int(id) * 20):pr_len],
            'manufacture': manufacture1[(int(id) * 20):pr_len],
            'product_type': p_type[(int(id) * 20):pr_len],
            'isAvailable': isAvailable1[(int(id) * 20):pr_len],
            'label': label1[(int(id) * 20):pr_len],
            'site': site1[(int(id) * 20):pr_len],
            'nextPage':-1,
            'start': (20 * int(id)),
            'end': ((20 *int(id)) + 20),
        }
    # if flag==True:
    #     myProducts = {
    #     'product_name': product_name1[(int(id)*20):((int(id)*20)+20)],
    #     'product_price': product_price[(int(id)*20):((int(id)*20)+20)],
    #     'product_image': product_image[(int(id)*20):((int(id)*20)+20)],
    #     'manufacture': manufacture[(int(id)*20):((int(id)*20)+20)],
    #     'product_type': product_type[(int(id)*20):((int(id)*20)+20)],
    #     'isAvailable': isAvailable[(int(id)*20):((int(id)*20)+20)],
    #     'label': label[(int(id)*20):((int(id)*20)+20)],
    #     'site': site[(int(id)*20):((int(id)*20)+20)],
    #     'nextPage': int(id)+1,
    #     'start': (20*int(id)),
    #     'end': 20*int(id)+20,
    #     }
    # else:
    #     myProducts = {
    #         'product_name': product_name1[(int(id) * 20):pr_len],
    #         'product_price': product_price[(int(id) * 20):pr_len],
    #         'product_image': product_image[(int(id) * 20):pr_len],
    #         'manufacture': manufacture[(int(id) * 20):pr_len],
    #         'product_type': product_type[(int(id) * 20):pr_len],
    #         'isAvailable': isAvailable[(int(id) * 20):pr_len],
    #         'label': label[(int(id) * 20):pr_len],
    #         'site': site[(int(id) * 20):pr_len],
    #         'nextPage':-1,
    #         'start': (20 * int(id)),
    #         'end': ((20 *int(id)) + 20),
    #     }
    return render(request, 'search.html', myProducts)

