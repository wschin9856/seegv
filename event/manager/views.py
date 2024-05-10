from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse,JsonResponse
from SEEGV.models import GiftconCategory,Members,MemberType,MemberInfo,StoreCategory,StoreProductState,StoreProduct,PackageProduct,Giftcon,GiftconState
import os 
from django.conf import settings


from django.core.paginator import Paginator 

# Create your views here.
def index(request:HttpRequest) :
    login = request.session.get("login")

    context = {
        'login' : login,

    }
    return render(request,'manager.html',context)

def members(request:HttpRequest) :
    login = request.session.get("login")
    type =  request.GET.get('type')
    if type == None :
        int_type = None
    else :
        int_type = int(type) 


    members = Members.objects.order_by('-member_no')

    if type == None :
        members = Members.objects.order_by('-member_no')
    else :
        members = Members.objects.order_by('-member_no').filter(memberType_no_id=type)

    memberType = MemberType.objects.all()
    


    #페이지 네비게이션
    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 10   # 한 페이지당 띄울 글의 개수 

    paginator = Paginator(members,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 

    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지






    context = {
        'login' : login,

        'members' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,

        "type" : type,
        'int_type' : int_type,
        "memberType" : memberType,


    }
    return render(request,'manager_members.html',context)



def members_detail(request:HttpRequest) :
    login = request.session.get("login")

    no = request.GET.get("no")

    member = Members.objects.get(member_no = no)
    memberType = MemberType.objects.all()
    memberInfo = MemberInfo.objects.all()


    context = {
        'login' : login,

        'member' : member,

        "memberType" : memberType,
        "memberInfo" : memberInfo,


    }
    return render(request,'manager_members_detail.html',context)

def members_detail_change(request:HttpRequest) :
    login = request.session.get("login")

    member_no = request.POST.get("member_no")
    type = request.POST.get("type")
    info = request.POST.get("info")

    member = Members.objects.get(member_no = member_no)

    try :
        member.memberType_no_id = type
        member.memberInfo_no_id = info
        member.save()
    except Exception as e:
        print(e)
        text = "변경에 실패했습니다"
    else :
        text = "변경이 완료되었습니다"

    url = "/manager/members/detail?no=" + member_no
        


    context = {
        'login' : login,
        'member' : member,
        'url' : url,
        'text' : text,



    }
    return render(request,'manager_result.html',context)


def members_detail_remove(request:HttpRequest) :
    login = request.session.get("login")

    member_no = request.POST.get("member_no")
    type = request.POST.get("type")
    info = request.POST.get("info")

    member = Members.objects.get(member_no = member_no)

    try :
        member.delete()
    except Exception as e:
        print(e)
        text = "삭제를 실패했습니다"
    else :
        text = "삭제가 완료되었습니다"

    url = "/manager/members"
        


    context = {
        'login' : login,
        'member' : member,
        'url' : url,
        'text' : text,



    }
    return render(request,'manager_result.html',context)


def product(request:HttpRequest) :
    login = request.session.get("login")

    category = int(request.GET.get("category",'0'))
    state = int(request.GET.get("state",'0'))

    

    storecategory = StoreCategory.objects.all()
    storeproductstate = StoreProductState.objects.all()

    if category == 0 and state == 0 :
        store = StoreProduct.objects.all()
    elif category == 0 :
        store = StoreProduct.objects.filter(sps_no_id=state)
    elif state == 0 :
        store = StoreProduct.objects.filter(sc_no_id=category)
    else :
        store = StoreProduct.objects.filter(sc_no_id=category,sps_no_id=state)




    #페이지 네비게이션
    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 5   # 한 페이지당 띄울 글의 개수 

    paginator = Paginator(store,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 

    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지




    context = {
        'login' : login,
        'store' : store,
        'storecategory' : storecategory,
        'storeproductstate' : storeproductstate,
        'category' :category,
        'state' : state,


        'store' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,



    }
    return render(request,'manager_product.html',context)



def product(request:HttpRequest) :
    login = request.session.get("login")

    category = int(request.GET.get("category",'0'))
    state = int(request.GET.get("state",'0'))

    

    storecategory = StoreCategory.objects.all()
    storeproductstate = StoreProductState.objects.all()

    if category == 0 and state == 0 :
        store = StoreProduct.objects.all()
    elif category == 0 :
        store = StoreProduct.objects.filter(sps_no_id=state)
    elif state == 0 :
        store = StoreProduct.objects.filter(sc_no_id=category)
    else :
        store = StoreProduct.objects.filter(sc_no_id=category,sps_no_id=state)




    #페이지 네비게이션
    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 5   # 한 페이지당 띄울 글의 개수 

    paginator = Paginator(store,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 

    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지




    context = {
        'login' : login,
        'store' : store,
        'storecategory' : storecategory,
        'storeproductstate' : storeproductstate,
        'category' :category,
        'state' : state,


        'store' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,



    }
    return render(request,'manager_product.html',context)


def product_detail(request:HttpRequest) :
    login = request.session.get("login")

    sp_no = request.GET.get("no")

    storeProduct = StoreProduct.objects.order_by("-sp_no").get(sp_no = sp_no)



    context = {
        'login' : login,

        'storeProduct' : storeProduct,

    }
    return render(request,'manager_product_detail.html',context)



def product_add(request:HttpRequest) :
    login = request.session.get("login")

    try : 
        category = int(request.POST.get("category"))
    except :
        category = None
        sc = None
    else :
        sc = StoreCategory.objects.get(sc_no=category)



    storecategory = StoreCategory.objects.all()
    storeproductstate = StoreProductState.objects.all()
    



    context = {
        'login' : login,

        'storecategory' : storecategory,
        'storeproductstate' : storeproductstate,


        'category' : category,
        'sc' : sc,
       

    }
    return render(request,'manager_product_add.html',context)


def product_add_result(request:HttpRequest) :
    login = request.session.get("login")

    sc_no = request.POST.get("sc_no")
    sp_name = request.POST.get("sp_name")
    sp_price = request.POST.get("sp_price")
    sp_discount = request.POST.get("sp_discount")
    sp_items = request.POST.get("sp_items")
    sp_period = request.POST.get("sp_period")
    sp_periodNumber = request.POST.get("sp_periodNumber")
    sp_origin = request.POST.get("sp_origin",'null')
    sp_txt = request.POST.get("sp_txt","null")
    sps_no = request.POST.get("sps_no")
    file = request.FILES.get('file')

    pp_name1 = request.POST.get("pp_name1")
    pp_price1 = request.POST.get("pp_price1")
    pp_count1 = request.POST.get("pp_count1")
    pp_periodNumber1 = request.POST.get("pp_periodNumber1")
    pp_origin1 = request.POST.get("pp_origin1",None)
    pp_name2 = request.POST.get("pp_name2")
    pp_price2 = request.POST.get("pp_price2")
    pp_count2 = request.POST.get("pp_count2")
    pp_periodNumber2 = request.POST.get("pp_periodNumber2")
    pp_origin2 = request.POST.get("pp_origin2",None)

    gg_category1 = request.POST.get("gg_category1")
    gg_category2 = request.POST.get("gg_category2")
    if gg_category1 == '1' :
        gg_name1 = "매점상품권"
    elif gg_category1 == '2' :
        gg_name1 = "영화관람권"

    if gg_category2 == '1' :
        gg_name2 = "매점상품권"
    elif gg_category2 == '2' :
        gg_name2 = "영화관람권"



    if sc_no == "1" :   # 패키지상품
        try :
            sp =  StoreProduct.objects.create(sc_no_id=sc_no,sp_name=sp_name,sp_price=sp_price,sp_discount=sp_discount,sp_items=sp_items,sp_period=sp_period,sp_periodNumber=sp_periodNumber,sp_origin=sp_origin,sp_txt=sp_txt,sps_no_id=sps_no,sp_image=file)
        except Exception as e :
            print(e)
            text = "실패"
        else : 
            try :
                pp1 = PackageProduct.objects.create(pp_name= pp_name1,pp_price= pp_price1,pp_count= pp_count1,pp_periodNumber= pp_periodNumber1,pp_origin= pp_origin1,sp_no_id = sp.sp_no)
                pp2 = PackageProduct.objects.create(pp_name= pp_name2,pp_price= pp_price2,pp_count= pp_count2,pp_periodNumber= pp_periodNumber2,pp_origin= pp_origin2,sp_no_id = sp.sp_no)
                gg1 = GiftconCategory.objects.create(gc_category=gg_name1,gc_categoryNo=gg_category1,pp_no_id=pp1.pp_no)
                gg2 = GiftconCategory.objects.create(gc_category=gg_name2,gc_categoryNo=gg_category2,pp_no_id=pp2.pp_no)
            except Exception as e :
                print(e)
                text = "실패"
            else :
                text = "성공"

    elif sc_no == "3" :     # 기프트카드
        
            try :
                sp =  StoreProduct.objects.create(sc_no_id=sc_no,sp_name=sp_name,sp_items=sp_items,sp_period=sp_period,sp_periodNumber=sp_periodNumber,sp_txt=sp_txt,sps_no_id=sps_no,sp_image=file)
            except Exception as e :
                print(e)
                text = "실패"
            else : 
                text = "성공"        

    else :      # 일반상품
            
        if sp_discount == "":

            try :
                sp =  StoreProduct.objects.create(sc_no_id=sc_no,sp_name=sp_name,sp_price=sp_price,sp_items=sp_items,sp_period=sp_period,sp_periodNumber=sp_periodNumber,sp_origin=sp_origin,sp_txt=sp_txt,sps_no_id=sps_no,sp_image=file)
            except Exception as e :
                print(e)
                text = "실패"
            else : 
                text = "성공"
        else :
            try :
                sp =  StoreProduct.objects.create(sc_no_id=sc_no,sp_name=sp_name,sp_price=sp_price,sp_discount=sp_discount,sp_items=sp_items,sp_period=sp_period,sp_periodNumber=sp_periodNumber,sp_origin=sp_origin,sp_txt=sp_txt,sps_no_id=sps_no,sp_image=file)
            except Exception as e :
                print(e)
                text = "실패"
            else : 
                text = "성공"

    url = "/manager/product"




    context = {
        'login' : login,
        'text' :text,
        "url" : url,


    }
    return render(request,'manager_result.html',context)

def product_change(request:HttpRequest) :
    login = request.session.get("login")
    sp_no = request.POST.get("sp_no")

    ## 패키지상품
    sp = StoreProduct.objects.get(sp_no=sp_no)
    category = sp.sc_no_id
    storeproductstate = StoreProductState.objects.all()
    packageProduct = PackageProduct.objects.filter(sp_no_id=sp_no)

    giftconCategory = GiftconCategory.objects.all()

    if category == 1 :
        pp1 = packageProduct[0]
        pp2 = packageProduct[1]
    else :
        pp1 = None
        pp2 = None       



    context = {
        'login' : login,
        'sp' : sp ,
        'category' : category,
        'storeproductstate' : storeproductstate,
        'packageProduct' :  packageProduct,
        'giftconCategory' :giftconCategory,
        'pp1' : pp1,
        'pp2' : pp2,
        
    }
    return render(request,'manager_product_change.html',context)







def product_change_result(request:HttpRequest) :
    login = request.session.get("login")
    sp_no = request.POST.get("sp_no")

    sc_no = request.POST.get("sc_no")
    sp_name = request.POST.get("sp_name")
    sp_price = request.POST.get("sp_price")
    sp_discount = request.POST.get("sp_discount")
    sp_items = request.POST.get("sp_items")
    sp_period = request.POST.get("sp_period")
    sp_periodNumber = request.POST.get("sp_periodNumber")
    sp_origin = request.POST.get("sp_origin",'null')
    sp_txt = request.POST.get("sp_txt","null")
    sps_no = request.POST.get("sps_no")
    file = request.FILES.get('file')

    pp_no1 = request.POST.get("pp_no1")
    pp_name1 = request.POST.get("pp_name1")
    pp_price1 = request.POST.get("pp_price1")
    pp_count1 = request.POST.get("pp_count1")
    pp_periodNumber1 = request.POST.get("pp_periodNumber1")
    pp_origin1 = request.POST.get("pp_origin1",None)
    pp_no2 = request.POST.get("pp_no2")
    pp_name2 = request.POST.get("pp_name2")
    pp_price2 = request.POST.get("pp_price2")
    pp_count2 = request.POST.get("pp_count2")
    pp_periodNumber2 = request.POST.get("pp_periodNumber2")
    pp_origin2 = request.POST.get("pp_origin2",None)

    gg_category1 = request.POST.get("gg_category1")
    gg_category2 = request.POST.get("gg_category2")

    if gg_category1 == '1' :
        gg_name1 = "매점상품권"
    elif gg_category1 == '2' :
        gg_name1 = "영화관람권"

    if gg_category2 == '1' :
        gg_name2 = "매점상품권"
    elif gg_category2 == '2' :
        gg_name2 = "영화관람권"


    sp = StoreProduct.objects.get(sp_no=sp_no)

    if sc_no == "1" :   # 패키지상품
        try :
            sp.sp_name=sp_name
            sp.sp_price=sp_price
            sp.sp_discount=sp_discount
            sp.sp_items=sp_items
            sp.sp_period=sp_period
            sp.sp_periodNumber=sp_periodNumber
            sp.sp_origin=sp_origin
            sp.sp_txt=sp_txt
            sp.sps_no_id=sps_no
            if file == None or "" :
                pass
            else :
                sp.sp_image=file
            sp.save()
        except Exception as e :
            print(e)
            text = "실패"
        else : 
            try :

                pp1 = PackageProduct.objects.get(pp_no = pp_no1)
                pp1.pp_name= pp_name1
                pp1.pp_price= pp_price1
                pp1.pp_count= pp_count1
                pp1.pp_periodNumber= pp_periodNumber1
                pp1.pp_origin= pp_origin1

                pp2 = PackageProduct.objects.get(pp_no = pp_no2)
                pp2.pp_name= pp_name2
                pp2.pp_price= pp_price2
                pp2.pp_count= pp_count2
                pp2.pp_periodNumber= pp_periodNumber2
                pp2.pp_origin= pp_origin2

                gg1 = GiftconCategory.objects.get(pp_no_id=pp1.pp_no) 
                gg1.gc_category=gg_name1
                gg1.gc_categoryNo=gg_category1


                gg2 = GiftconCategory.objects.get(pp_no_id=pp1.pp_no)
                gg2.gc_category=gg_name2
                gg2.gc_categoryNo=gg_category2

                pp1.save()
                pp2.save()
                gg1.save()
                gg2.save()
           
            except Exception as e :
                print(e)
                text = "실패"
            else :
                text = "성공"

    elif sc_no == "3" :     # 기프트카드
        
            try :
                sp.sc_no_id=sc_no
                sp.sp_name=sp_name
                sp.sp_items=sp_items
                sp.sp_period=sp_period
                sp.sp_periodNumber=sp_periodNumber
                sp.sp_txt=sp_txt
                sp.sps_no_id=sps_no
                if file == None or "" :
                    pass
                else :
                    sp.sp_image=file
                sp.save()
            except Exception as e :
                print(e)
                text = "실패"
            else : 
                text = "성공"        

    else :      # 일반상품
            
        if sp_discount == "" or sp_discount == "None":

            try :
                sp.sc_no_id=sc_no
                sp.sp_name=sp_name
                sp.sp_price=sp_price
                sp.sp_items=sp_items
                sp.sp_period=sp_period
                sp.sp_periodNumber=sp_periodNumber
                sp.sp_origin=sp_origin
                sp.sp_txt=sp_txt
                sp.sps_no_id=sps_no
                if file == None or "" :
                    pass
                else :
                    sp.sp_image=file
                sp.save()
            except Exception as e :
                print(e)
                text = "실패"
            else : 
                text = "성공"
        else :
            try :
                sp.sc_no_id=sc_no
                sp.sp_name=sp_name
                sp.sp_price=sp_price
                sp.sp_items=sp_items
                sp.sp_period=sp_period
                sp.sp_periodNumber=sp_periodNumber
                sp.sp_origin=sp_origin
                sp.sp_txt=sp_txt
                sp.sps_no_id=sps_no
                sp.sp_image=file
                sp_discount=sp_discount
                if file == None or "" :
                    pass
                else :
                    sp.sp_image=file
                sp.save()
            except Exception as e :
                print(e)
                text = "실패"
            else : 
                text = "성공"

    url = "/manager/product"




    context = {
        'login' : login,
        'text' :text,
        "url" : url,


    }
    return render(request,'manager_result.html',context)





def product_remove(request:HttpRequest) :
    login = request.session.get("login")

    sp_no = request.POST.get("sp_no")
    storeProduct = StoreProduct.objects.get(sp_no=sp_no)

    try :
        if sp_no == "1" :
            packageProduct  =  PackageProduct.objects.filter(sp_no_id=sp_no)

            for p in packageProduct :
                gg = GiftconCategory.objects.get(pp_no_id=p.pp_no)
                gg.delete()

            packageProduct.delete()
            storeProduct.delete()

        else :
            storeProduct.delete()
    
    except :
        text = "삭제실패"
    else :
        text = "삭제성공"



    url ="/manager/product"






    context = {
        'login' : login,

        'text' : text,
        'url' : url,


    }
    return render(request,'manager_result.html',context)


def giftcon(request:HttpRequest) :
    login = request.session.get("login")

    
    giftconstate = GiftconState.objects.all()
    giftcon = Giftcon.objects.order_by('-giftcon_no').all()

    search = request.GET.get('search')
    mode = request.GET.get('mode')


    if search  == None :
        search  = ''

    if mode == None :
        giftcon = Giftcon.objects.order_by('-giftcon_no').all()
    elif mode  == '1' :
        try :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(giftcon_number=search)
        except :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=0)

    elif mode  == '2' :
        try :
            user = Members.objects.get(member_id=search)
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=user.member_no)           
        except :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=0)
        


    elif mode  == '3' :
        try :
            user = Members.objects.get(member_name=search)
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=user.member_no)        
        except :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=0)






    #페이지 네비게이션
    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 10   # 한 페이지당 띄울 글의 개수 
    
    paginator = Paginator(giftcon,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 
    
    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지



    context = {
        'login' : login,
        # 'giftcon' : giftcon,
        'giftconstate' : giftconstate,

        'search' : search,
        'mode' : mode,



        'giftcon' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,

    }
    return render(request,'manager_giftcon.html',context)


def giftcon_num(request:HttpRequest,num:int) :
    login = request.session.get("login")


    giftconstate = GiftconState.objects.all()
    # giftcon = Giftcon.objects.order_by('-giftcon_no').filter(gs_no_id=2)

    search = request.GET.get('search')
    mode = request.GET.get('mode')

    print(num)

    if search  == None :
        search  = ''

    if mode == None :
        giftcon = Giftcon.objects.order_by('-giftcon_no').filter(gs_no_id=num)
    elif mode  == '1' :
        try :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(giftcon_number=search,gs_no_id=num)
        except :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=0,gs_no_id=num)

    elif mode  == '2' :
        try :
            user = Members.objects.get(member_id=search)
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=user.member_no,gs_no_id=num)           
        except :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=0,gs_no_id=num)

    elif mode  == '3' :
        try :
            user = Members.objects.get(member_name=search)
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=user.member_no,gs_no_id=num)        
        except :
            giftcon = Giftcon.objects.order_by('-giftcon_no').filter(user_no_id=0,gs_no_id=num)



        





    #페이지 네비게이션
    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 10   # 한 페이지당 띄울 글의 개수 

    paginator = Paginator(giftcon,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 

    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지



    context = {
        'login' : login,
        # 'giftcon' : giftcon,
        'giftconstate' : giftconstate,
        # 'ss' : ss,
        'search' : search,
        'mode' : mode,
        'num' : num,

        'giftcon' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,

    }
    return render(request,'manager_giftcon.html',context)



def giftcon_state(request:HttpRequest) :
    login = request.session.get("login")

    giftcon_no = request.POST.get('giftcon_no')
    # state = request.POST.get('state')

    # print(state)

    try :
        con = Giftcon.objects.get(giftcon_no=giftcon_no)
        if con.gs_no_id == 1 :
            con.gs_no_id = 2
        elif con.gs_no_id == 2 :
            con.gs_no_id = 1
        con.save()
    except Exception as e :
        print(e)
        text = "실패"
    else :
        text = "변경되었습니다"


    url = "/manager/giftcon"






    context = {
        'login' : login,
        'text' : text,
        'url' : url,


    }
    return render(request,'manager_result.html',context)

