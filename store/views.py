from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse,JsonResponse
from SEEGV.models import StoreCategory,PackageProduct,StoreProduct,AddList,Event,Members,ProductOrder,StoreOrder,GiftconUser,PointRule,PointCategory,Point,PointUse,Giftcon,Giftcard,GiftconCategory
import os 
from django.conf import settings
import datetime
import random


def index(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()

    context = {
        'login' : login,
        'category' : category,

    }
    return render(request,'index.html',context)


def store(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()
    storeProduct = StoreProduct.objects.all()  
    package = StoreProduct.objects.filter(sc_no_id = 1)
    moviet = StoreProduct.objects.filter(sc_no_id = 2)
    giftcard = StoreProduct.objects.filter(sc_no_id = 3)


    context = {
        'login' : login,
        'category' : category,
        'package' :package,
        'moviet' : moviet,
        'giftcard' : giftcard,
    }
    return render(request,'store_main.html',context)




def category(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바

    sc_no = request.GET.get('sc_no')    # 카테고리 넘버
    storeProduct = StoreProduct.objects.filter(sc_no_id=sc_no,sps_no_id='1') 
    sc_category = StoreCategory.objects.get(sc_no=sc_no)


    context = {
        'login' : login,
        'category' : category,
        'storeProduct' : storeProduct,
        'sc_category' : sc_category,
        'sc_no' : sc_no,


    }
    return render(request,'store_category.html',context)

def product(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바


    sp_no = int(request.GET.get('sp_no'))    # 상품 넘버
    storeProduct = StoreProduct.objects.get(sp_no=sp_no,sps_no_id='1') 
    

    context = {
        'login' : login,
        'category' : category,
        'storeProduct' : storeProduct,
        'sp_no' : sp_no,


    }
    return render(request,'store_product.html',context)





def product_add(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바


    sp_no = int(request.POST.get('sp_no') )   # 상품 넘버
    
    storeProduct = StoreProduct.objects.get(sp_no=sp_no)
    sc_no = StoreProduct.objects.values('sc_no').get(sp_no=sp_no)

    count1 = request.POST.get('count1')
    count2 = request.POST.get('count2')
    count3 = request.POST.get('count3') 
    now = datetime.datetime.now().strftime('%Y-%m-%d')


    if sc_no["sc_no"] == 3 :
        count = int(count1)
        print(type(count))
        try :
            AddList.objects.create(addList_count=count, addList_date=now, member_no_id=login, sp_no_id=sp_no)
        except Exception as e: 
            text = "장바구니 추가실패."
            url = "addList"
            print('1번')
        else : 
            text = "장바구니에 추가 되었습니다."
            url = "addList"            
    elif  sc_no["sc_no"] == 1:
        count = int(count2)
        try:
            AddList.objects.create(addList_count=count, addList_date=now, member_no_id=login, sp_no_id=sp_no)
        except : 
            text = "장바구니 추가실패."
            url = "addList"
            print('2번')
        else : 
            text = "장바구니에 추가 되었습니다."
            url = "addList"
    else :
        count = int(count3)
        try:
            AddList.objects.create(addList_count=count, addList_date=now, member_no_id=login, sp_no_id=sp_no)
        except : 
            text = "장바구니 추가실패."
            url = "addList"
            print('3번')
        else : 
            text = "장바구니에 추가 되었습니다."
            url = "addList"       
        



    context = {
        'login' : login,
        'category' : category,
        'storeProduct' : storeProduct,
        'sp_no' : sp_no,
        'text' : text,
        'url' : url,


    }
    return render(request,'result.html',context)











def addList(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바   


    addList = AddList.objects.filter(member_no_id=login)
    storeProduct = StoreProduct.objects.all()


    for i in addList :
        i.addList_checkde = 0
        i.save()
    


    context = {
        'login' : login,
        'category' : category,
        'addList' : addList,
        'storeProduct' :storeProduct,



    }
    return render(request,'store_addList.html',context)    




def addList_ajax(request:HttpRequest):
    login = request.session.get("login")
    addList_no = request.POST.get("addList_no")
    value = request.POST.get("value")

    try : 
        addList = AddList.objects.get(addList_no=addList_no)
        addList.addList_count = value
        addList.save()
    except:
        msg = "실패"
    else :
        msg = "변경되었습니다"



    return JsonResponse({'msg':msg}) #Json 타입으로 반환



def purchase(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바   
   
    method = request.GET.get("method")  # 바로구입 : 1 장바구니 : 0
    if method == '1' :
        sp_no = request.POST.get("sp_no")
    else :
        sp_no = request.GET.get("no")
        count = request.GET.get("count")   # 장바구니에서의 상품 갯수


    storeProduct = StoreProduct.objects.get(sp_no=sp_no)    

    ##########개별 구매
    sc_no = StoreProduct.objects.values('sc_no').get(sp_no=sp_no)
    
    price1 = request.POST.get("price1") # 기프트 카드의 가격
    count2 = request.POST.get("count2") # 패키지상품의 갯수
    count3 = request.POST.get("count3") # 일반상품의 갯수



    if method == '1' :
        list = None # add_list no이므로 바로 구입하기에서는 필요없음
        if sc_no['sc_no'] ==  3 : # 기프트카드
            print('기프트카드')
            price = price1
            count = 1
            f_price = int(price) * count
            total_discount = 0

        elif sc_no['sc_no'] ==  1 : # 패키지 상품
            print('패키지상품')
            price = storeProduct.sp_discount
            count = count2
            f_price = int(price) * int(count)
            total_discount = int(storeProduct.sp_price - storeProduct.sp_discount) * int(count)

        else : #일반상품
            print('일반상품')
            price = storeProduct.sp_price
            count = count3
            f_price = int(price) * int(count)
            total_discount = 0

        ############## 개별 구매
    else :  ### 장바구니 
        list = request.GET.get("list") # add_list no
        addList = AddList.objects.get(addList_no=list)
        if sc_no['sc_no'] ==  1 : # 패키지 상품
            print('패키지상품_add')
            price = storeProduct.sp_discount
            count = addList.addList_count
            f_price = int(price) * int(count)
            total_discount = int(storeProduct.sp_price - storeProduct.sp_discount) * int(count)

        else : #일반상품
            print('일반상품_add')
            price = storeProduct.sp_price
            count = addList.addList_count
            f_price = int(price) * int(count)
            total_discount = 0


    ## 구매자 정보
    member = Members.objects.get(member_no=login)


    context = {
        'login' : login,
        'category' : category,
        'sp_no' : sp_no,
        'count' : count,
        'storeProduct' : storeProduct,
        'price' : price,
        'f_price' : f_price,
        'total_discount' : total_discount,
        'member' : member,
        'list' : list,
        'method' : method,


    }
    return render(request,'store_purchase.html',context)    

def purchase_result(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바  

    member = Members.objects.get(member_no=login) 

    sp_no = request.POST.get("sp_no")   # 구매하기 품목명
    product = StoreProduct.objects.get(sp_no=sp_no)
   
    list = request.POST.get("list") 
    method = request.POST.get("method") 


    if product.sp_discount != None :    # 패키지
        item = 1
        price = product.sp_price
        payment = product.sp_discount
        count = request.POST.get("count")  # 구매수량
        discount = product.sp_price - product.sp_discount
    elif product.sp_price == None : # 기프트카드
        item = 2
        price = request.POST.get("giftcard_price") # 기프트카드 가격
        payment = price
        count = 1
        discount = 0
    else :  # 일반상품
        item = 3
        price = product.sp_price
        payment = product.sp_price
        count = request.POST.get("count")  
        discount = 0




    total_price = int(price) * int(count)
    order_discount = int(discount) * int(count)
    order_payment = int(payment) * int(count)


    # 구매시 생성되어야 하는 항목
    # 일반상품 주문시


    #####################################동일내역
    try :
        # GiftconUser(수취자)3
        tel = member.member_tel1+member.member_tel2+member.member_tel3
        giftconUser = GiftconUser.objects.create(userName=member.member_name,userTel=tel)


        # StoreOrder(주문내역)1
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        date = str(datetime.datetime.now().strftime('%Y%m%d'))

        storeOrder = StoreOrder.objects.create(order_date=now,member_no_id=login,order_price=total_price,order_discount=order_discount,order_payment=order_payment,order_method=1,order_state=1,giftconUser_no_id=giftconUser.giftconUser_no)
        order_no = str(storeOrder.order_no)
        storeOrder.order_number = date + order_no
        storeOrder.save()
        giftconUser.order_number=storeOrder.order_number
        giftconUser.save()

        # ProductOrder(주문상품 정보)2
        productOrder = ProductOrder.objects.create(order_no_id=storeOrder.order_no,order_number=storeOrder.order_number,sp_no_id=sp_no,order_count=count,order_price=price,order_discount=discount)


        #포인트 적립
            # 실구매가의 0.05%적립

        pointrule = PointRule.objects.get(PointRule_no=5)
        point = order_payment * (pointrule.pointRule/100)
        pointUse = PointUse.objects.create(pc_no_id=2,member_no_id=login,savepoint=point,usepoint=0,pointUse_place='온라인/스토어',pointUse_date=now)
        
        storeOrder.pointUse_no_id = pointUse.pointUse_no
        storeOrder.save()

        po = Point.objects.get(pc_no_id=2,member_no_id =login)
        po.point = po.point + int(point)
        po.save()


        #####################################변동
        # 기프트콘 등록
        

        today = datetime.date.today()

        giftconCategory = GiftconCategory.objects.all()
        
        ran = str(random.randrange(1000000,10000000))


        ### 일반상품 item == 3
        if item == 3 :
            p = datetime.timedelta(days=(30*int(product.sp_periodNumber)))
            period = today + p
                
            for c in range(0,int(count)) :
                ran = str(random.randrange(1000000,10000000))
                giftcon = Giftcon.objects.create(sp_no_id=sp_no,user_no_id=login,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 1)
                giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                giftcon.save()

                giftconCategory = GiftconCategory.objects.get(sc_no_id=product.sc_no)
                giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                giftcon.save()            

        
        ### 패키지상품
        elif item == 1 :
            package = PackageProduct.objects.filter(sp_no_id=sp_no)
            for c in range(0,int(count)) :    #구매갯수
                for pack in package :   # 패키지 내부상품
                    for c in range(0,int(pack.pp_count)) : # 패키지 내부 상품의 갯수
                        p = datetime.timedelta(days=(30*int(pack.pp_periodNumber)))
                        period = today + p

                        ran = str(random.randrange(1000000,10000000))
                        giftcon = Giftcon.objects.create(sp_no_id=sp_no,pp_no_id=pack.pp_no,user_no_id=login,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 1)
                        giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                        giftcon.save()

                        giftconCategory = GiftconCategory.objects.get(pp_no_id=pack.pp_no)
                        giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                        giftcon.save()



        ### 기프트 카드
        elif item == 2 :
            p = datetime.timedelta(days=(30*int(product.sp_periodNumber)))
            period = today + p
            pw = random.randrange(10000000,100000000)

            ran = str(random.randrange(1000000,10000000))
            giftcard = Giftcard.objects.create(cc_no_id=3,order_no_id=storeOrder.order_no,member_no_id=login,giftcard_pw=pw,giftcard_price=price,giftcard_balance=price,giftcard_period=period,gs_no_id = 1)
            giftcard.giftcard_number = str(giftcard.giftcard_no) + ran
            giftcard.save()

        
        user = GiftconUser.objects.get(order_number=storeOrder.order_number)
        usertel = "010 - {} - {}".format(user.userTel[3:7],user.userTel[7:]) 
    except Exception as e :
        print(e)
        text = "결제가 실패되었습니다"
        url ="/store/addList"   
    else :
        text = "결제가 완료되었습니다"
        url ="/user/mycgv/payment/detail?no=" + str(storeOrder.order_no)

        if method == '2' :
            try :
                addList = AddList.objects.get(addList_no=list)
                addList.delete()
                print('장바구니 삭제 완료')
            except Exception as e :
                print(e)
                print('장바구니 삭제 실패')
                
    




    context = {
        'login' : login,
        'category' : category,

        'text' : text,
        'url' : url,




    }
    return render(request,'result.html',context)






def userGift(request:HttpRequest):
    
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바   
   
    method = request.GET.get("method")  # 바로구입 : 1 장바구니 : 0
    if method == '1' :
        sp_no = request.POST.get("sp_no")# 개별구매 상품 번호
    else :
        sp_no = request.GET.get("no")
        count = request.GET.get("count")   # 장바구니에서의 상품 갯수

    print(sp_no)

    storeProduct = StoreProduct.objects.get(sp_no=sp_no)  # 개별구매 상품정보

    ##########개별 구매
    sc_no = StoreProduct.objects.values('sc_no').get(sp_no=sp_no)
    
    price1 = request.POST.get("price1") # 기프트 카드의 가격
    count2 = request.POST.get("count2") # 패키지상품의 갯수
    count3 = request.POST.get("count3") # 일반상품의 갯수



    if method == '1' :
        list = None # add_list no이므로 바로 구입하기에서는 필요없음
        if sc_no['sc_no'] ==  3 : # 기프트카드
            print('기프트카드')
            price = price1
            count = 1
            f_price = int(price) * count
            total_discount = 0

        elif sc_no['sc_no'] ==  1 : # 패키지 상품
            print('패키지상품')
            price = storeProduct.sp_discount
            count = count2
            f_price = int(price) * int(count)
            total_discount = int(storeProduct.sp_price - storeProduct.sp_discount) * int(count)

        else : #일반상품
            print('일반상품')
            price = storeProduct.sp_price
            count = count3
            f_price = int(price) * int(count)
            total_discount = 0

        ############## 개별 구매
    else :  ### 장바구니 
        list = request.GET.get("list") # add_list no
        addList = AddList.objects.get(addList_no=list)
        if sc_no['sc_no'] ==  1 : # 패키지 상품
            print('패키지상품_add')
            price = storeProduct.sp_discount
            count = addList.addList_count
            f_price = int(price) * int(count)
            total_discount = int(storeProduct.sp_price - storeProduct.sp_discount) * int(count)

        else : #일반상품
            print('일반상품_add')
            price = storeProduct.sp_price
            count = addList.addList_count
            f_price = int(price) * int(count)
            total_discount = 0        





    ## 구매자 정보
    member = Members.objects.get(member_no=login)


    context = {
        'login' : login,
        'category' : category,
        'sp_no' : sp_no,
        'count' : count,
        'storeProduct' : storeProduct,
        'price' : price,
        'f_price' : f_price,
        'total_discount' : total_discount,
        'member' : member,
        'list' : list,
        'method' : method,



    }
    return render(request,'store_userGift.html',context)    


def userGift_result(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바  

    member = Members.objects.get(member_no=login) 

    sp_no = request.POST.get("sp_no")   # 구매하기 품목명
    product = StoreProduct.objects.get(sp_no=sp_no)
   
   
    list = request.POST.get("list") 
    method = request.POST.get("method") 

    if product.sp_discount != None :    # 패키지
        item = 1
        price = product.sp_price
        payment = product.sp_discount
        count = request.POST.get("count")  # 구매수량
        discount = product.sp_price - product.sp_discount
    elif product.sp_price == None : # 기프트카드
        item = 2
        price = request.POST.get("giftcard_price") # 기프트카드 가격
        payment = price
        count = 1
        discount = 0
    else :  # 일반상품
        item = 3
        price = product.sp_price
        payment = product.sp_price
        count = request.POST.get("count")  
        discount = 0




    total_price = int(price) * int(count)
    order_discount = int(discount) * int(count)
    order_payment = int(payment) * int(count)


    # 구매시 생성되어야 하는 항목
    # 일반상품 주문시


    #####################################동일내역
    try :
        # GiftconUser(수취자)3
        user_name = request.POST.get('user_name')
        user_tel = request.POST.get('user_tel')
        giftconUser = GiftconUser.objects.create(userName=user_name,userTel=user_tel)


        # StoreOrder(주문내역)1
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        date = str(datetime.datetime.now().strftime('%Y%m%d'))

        storeOrder = StoreOrder.objects.create(order_date=now,member_no_id=login,order_price=total_price,order_discount=order_discount,order_payment=order_payment,order_method=1,order_state=1,giftconUser_no_id=giftconUser.giftconUser_no)
        order_no = str(storeOrder.order_no)
        storeOrder.order_number = date + order_no
        storeOrder.save()
        giftconUser.order_number=storeOrder.order_number
        giftconUser.save()

        # ProductOrder(주문상품 정보)2
        productOrder = ProductOrder.objects.create(order_no_id=storeOrder.order_no,order_number=storeOrder.order_number,sp_no_id=sp_no,order_count=count,order_price=price,order_discount=discount)


        #포인트 적립
            # 실구매가의 0.05%적립

        pointrule = PointRule.objects.get(PointRule_no=5)
        point = order_payment * (pointrule.pointRule/100)
        pointUse = PointUse.objects.create(pc_no_id=2,member_no_id=login,savepoint=point,usepoint=0,pointUse_place='온라인/스토어',pointUse_date=now)
        
        storeOrder.pointUse_no_id = pointUse.pointUse_no
        storeOrder.save()

        po = Point.objects.get(pc_no_id=2,member_no_id =login)
        po.point = po.point + int(point)
        po.save()


        #####################################변동
        # 기프트콘 등록
        

        today = datetime.date.today()

        giftconCategory = GiftconCategory.objects.all()
        
        ran = str(random.randrange(1000000,10000000))


        ### 일반상품 item == 3
        if item == 3 :
            p = datetime.timedelta(days=(30*int(product.sp_periodNumber)))
            period = today + p
            
            List = []

            for c in range(0,int(count)) :
                ran = str(random.randrange(1000000,10000000))
                giftcon = Giftcon.objects.create(sp_no_id=sp_no,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 5)
                giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                giftcon.save()

                giftconCategory = GiftconCategory.objects.get(sc_no_id=product.sc_no)
                giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                giftcon.save()  

                number = giftcon.giftcon_number
                name = product.sp_name
                List.append({'number':number,'name':name})
                        

        
        ### 패키지상품
        elif item == 1 :
            package = PackageProduct.objects.filter(sp_no_id=sp_no)
            
            List = []

            for c in range(0,int(count)) :    #구매갯수
                for pack in package :   # 패키지 내부상품
                    for c in range(0,int(pack.pp_count)) : # 패키지 내부 상품의 갯수
                        p = datetime.timedelta(days=(30*int(pack.pp_periodNumber)))
                        period = today + p

                        ran = str(random.randrange(1000000,10000000))
                        giftcon = Giftcon.objects.create(sp_no_id=sp_no,pp_no_id=pack.pp_no,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 5)
                        giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                        giftcon.save()

                        giftconCategory = GiftconCategory.objects.get(pp_no_id=pack.pp_no)
                        giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                        giftcon.save()
                        
                        number = giftcon.giftcon_number
                        name = pack.pp_name
                        List.append({'number':number,'name':name})







        ### 기프트 카드
        elif item == 2 :
            p = datetime.timedelta(days=(30*int(product.sp_periodNumber)))
            period = today + p
            pw = random.randrange(10000000,100000000)

            ran = str(random.randrange(1000000,10000000))
            giftcard = Giftcard.objects.create(cc_no_id=3,order_no_id=storeOrder.order_no,giftcard_pw=pw,giftcard_price=price,giftcard_balance=price,giftcard_period=period,gs_no_id=5)
            giftcard.giftcard_number = str(giftcard.giftcard_no) + ran
            giftcard.save()

            number = giftcard.giftcard_number
            name = product.sp_name
            card_pw = giftcard.giftcard_pw

            List = {'number':number,'name':name,'card_pw':card_pw}

    except Exception as e :
        print(e)
        text = "결제가 실패되었습니다"
        url ="/store/addList"   
    else :
        text = "결제가 완료되었습니다"
        url ="/user/mycgv/payment/detail?no=" + str(storeOrder.order_no)

        if method == '2' :
            try :
                addList = AddList.objects.get(addList_no=list)
                addList.delete()
                print('장바구니 삭제 완료')
            except Exception as e :
                print(e)
                print('장바구니 삭제 실패')



    ### 기프트 카드   


    context = {
        'login' : login,
        'category' : category,


        'text' : text,
        'url' : url,


    }

    return render(request,'result.html',context)








def addList_purchase(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바   
   
    
    List = AddList.objects.values('addList_no').filter(member_no_id=login)
    method = request.GET.get("method")  # 바로구입 : 1 장바구니 : 0

    list = []   # 장바구니에 담긴 상품 전체
    for no in List:
        list.append(no['addList_no'])
 
        # 장바구니 안에서 선택한 상품 check = 1로  바꾸기
    for i in list :
        no = request.POST.get("ck"+str(i))
        if no != None :
            add = AddList.objects.get(member_no_id=login,addList_no=i)
            add.addList_checkde = 1
            add.save()
        else :
            pass

    
    addList = AddList.objects.filter(member_no_id=login,addList_checkde = 1)

    ## 패키지내부상품
    ppList = PackageProduct.objects.all()

    # 합계금액 구하기
    # 총 상품금액
    totalPrice = 0
    totalDiscount = 0
    
    for i in addList :

        if i.sp_no.sc_no_id == 1 :## 패키지 상품
            totalPrice = totalPrice + i.sp_no.sp_price
            discount = i.sp_no.sp_price - i.sp_no.sp_discount
            totalDiscount = totalDiscount + discount
        elif i.sp_no.sc_no_id == 3 : ## 기프트카드는 장바구니 구매가 안됨 
            pass
        else :
            totalPrice = totalPrice + i.sp_no.sp_price
            if i.sp_no.sp_discount == None :
                discount = 0
            else :
                discount = i.sp_no.sp_discount
            totalDiscount = totalDiscount + discount



    f_price = totalPrice - totalDiscount

    print(addList.__len__())
    if addList.__len__() == 0 :
        text = "장바구니에서 구입할 상품을 선택하세요"
        url = "/store/addList"
        check = True
    else :
        text = ""
        url = ""
        check = False

    print(check)


    ## 구매자 정보
    member = Members.objects.get(member_no=login)
 
    context = {
        'login' : login,
        'category' : category,
        'addList' : addList,
        'ppList' : ppList,
        'totalPrice' : totalPrice,
        'totalDiscount' : totalDiscount,
        'f_price' : f_price,
        'member' : member,
        'text' : text,
        'url' : url,
        "check" : check,

    }
    return render(request,'store_addList_purchase.html',context)    



def addList_purchase_result(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바  

    total_price = request.POST.get('totalPrice')
    order_discount = request.POST.get('totalDiscount')
    order_payment = request.POST.get('f_price')

    member = Members.objects.get(member_no=login) 
    addList = AddList.objects.filter(member_no_id=login,addList_checkde = 1)


    ## 한번만 생겨야하는 항목

    # GiftconUser(수취자)3
    tel = member.member_tel1+member.member_tel2+member.member_tel3
    giftconUser = GiftconUser.objects.create(userName=member.member_name,userTel=tel)


    # StoreOrder(주문내역)1
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    date = str(datetime.datetime.now().strftime('%Y%m%d'))

    storeOrder = StoreOrder.objects.create(order_date=now,member_no_id=login,order_price=total_price,order_discount=order_discount,order_payment=order_payment,order_method=1,order_state=1,giftconUser_no_id=giftconUser.giftconUser_no)
    order_no = str(storeOrder.order_no)
    storeOrder.order_number = date + order_no
    storeOrder.save()
    giftconUser.order_number=storeOrder.order_number
    giftconUser.save()

    #포인트 적립
        # 실구매가의 0.05%적립

    pointrule = PointRule.objects.get(PointRule_no=5)
    point = int(order_payment) * (pointrule.pointRule/100)


    pointUse = PointUse.objects.create(pc_no_id=2,member_no_id=login,savepoint=point,usepoint=0,pointUse_place='온라인/스토어',pointUse_date=now)
    
    storeOrder.pointUse_no_id = pointUse.pointUse_no
    storeOrder.save()

    po = Point.objects.get(pc_no_id=2,member_no_id =login)

    po.point = int(po.point) + int(point)
    po.save()





    ## 상품별로 생성 되어야 하는 항목

    for add in addList :
        sp_no = add.sp_no_id   # 품목명
        product = StoreProduct.objects.get(sp_no=sp_no)
    
        if product.sp_discount != None :    # 패키지
            item = 1
            price = product.sp_price
            payment = product.sp_discount
            count = add.addList_count  # 구매수량
            discount = product.sp_price - product.sp_discount
        else :  # 일반상품
            item = 3
            price = product.sp_price
            payment = product.sp_price
            count = add.addList_count 
            discount = 0




        total_price = int(price) * int(count)
        order_discount = int(discount) * int(count)
        order_payment = int(payment) * int(count)

        #####################################동일내역



        # ProductOrder(주문상품 정보)2
        productOrder = ProductOrder.objects.create(order_no_id=storeOrder.order_no,order_number=storeOrder.order_number,sp_no_id=sp_no,order_count=count,order_price=price,order_discount=discount)




        #####################################변동
        # 기프트콘 등록
        

        today = datetime.date.today()

        giftconCategory = GiftconCategory.objects.all()
        
        ran = str(random.randrange(1000000,10000000))


        ### 일반상품 item == 3
        if item == 3 :
            p = datetime.timedelta(days=(30*int(product.sp_periodNumber)))
            period = today + p
                
            for c in range(0,int(count)) :
                ran = str(random.randrange(1000000,10000000))
                giftcon = Giftcon.objects.create(sp_no_id=sp_no,user_no_id=login,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 1)
                giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                giftcon.save()

                giftconCategory = GiftconCategory.objects.get(sc_no_id=product.sc_no)
                giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                giftcon.save()            

        
        ### 패키지상품
        elif item == 1 :
            package = PackageProduct.objects.filter(sp_no_id=sp_no)
            for c in range(0,int(count)) :    #구매갯수
                for pack in package :   # 패키지 내부상품
                    for c in range(0,int(pack.pp_count)) : # 패키지 내부 상품의 갯수
                        p = datetime.timedelta(days=(30*int(pack.pp_periodNumber)))
                        period = today + p

                        ran = str(random.randrange(1000000,10000000))
                        giftcon = Giftcon.objects.create(sp_no_id=sp_no,pp_no_id=pack.pp_no,user_no_id=login,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 1)
                        giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                        giftcon.save()

                        giftconCategory = GiftconCategory.objects.get(pp_no_id=pack.pp_no)
                        giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                        giftcon.save()



    
    
    user = GiftconUser.objects.get(order_number=storeOrder.order_number)
    usertel = "010 - {} - {}".format(user.userTel[3:7],user.userTel[7:]) 


    addList.delete()

    text = "결제가 완료되었습니다"
    url ="/user/mycgv/payment/detail?no=" + str(storeOrder.order_no)

    context = {
        'login' : login,
        'category' : category,

        'text' : text,
        'url' : url,




    }
    return render(request,'result.html',context)




def addList_userGift(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바   
   
    
    List = AddList.objects.values('addList_no').filter(member_no_id=login)
    method = request.GET.get("method")  # 바로구입 : 1 장바구니 : 0

    list = []   # 장바구니에 담긴 상품 전체
    for no in List:
        list.append(no['addList_no'])
 
        # 장바구니 안에서 선택한 상품 check = 1로  바꾸기
    for i in list :
        no = request.POST.get("ck"+str(i))
        if no != None :
            add = AddList.objects.get(member_no_id=login,addList_no=i)
            add.addList_checkde = 1
            add.save()
        else :
            pass

    
    addList = AddList.objects.filter(member_no_id=login,addList_checkde = 1)

    ## 패키지내부상품
    ppList = PackageProduct.objects.all()

    # 합계금액 구하기
    # 총 상품금액
    totalPrice = 0
    totalDiscount = 0
    
    for i in addList :

        if i.sp_no.sc_no_id == 1 :## 패키지 상품
            totalPrice = totalPrice + i.sp_no.sp_price
            discount = i.sp_no.sp_price - i.sp_no.sp_discount
            totalDiscount = totalDiscount + discount
        elif i.sp_no.sc_no_id == 3 : ## 기프트카드는 장바구니 구매가 안됨 
            pass
        else :
            totalPrice = totalPrice + i.sp_no.sp_price
            if i.sp_no.sp_discount == None :
                discount = 0
            else :
                discount = i.sp_no.sp_discount
            totalDiscount = totalDiscount + discount



    f_price = totalPrice - totalDiscount

    print(addList.__len__())
    if addList.__len__() == 0 :
        text = "장바구니에서 구입할 상품을 선택하세요"
        url = "/store/addList"
        check = True
    else :
        text = ""
        url = ""
        check = False

    print(check)


    ## 구매자 정보
    member = Members.objects.get(member_no=login)
 
    context = {
        'login' : login,
        'category' : category,
        'addList' : addList,
        'ppList' : ppList,
        'totalPrice' : totalPrice,
        'totalDiscount' : totalDiscount,
        'f_price' : f_price,
        'member' : member,
        'text' : text,
        'url' : url,
        "check" : check,

    }
    return render(request,'store_addList_userGift.html',context)    





def addList_userGift_result(request:HttpRequest):
    login = request.session.get("login")
    category = StoreCategory.objects.all()  # 상단 카테고리 네비게이션 바  

    total_price = request.POST.get('totalPrice')
    order_discount = request.POST.get('totalDiscount')
    order_payment = request.POST.get('f_price')

    user_name = request.POST.get('user_name')
    user_tel = request.POST.get('user_tel')

    member = Members.objects.get(member_no=login) 
    addList = AddList.objects.filter(member_no_id=login,addList_checkde = 1)


    ## 한번만 생겨야하는 항목

    # GiftconUser(수취자)3

    giftconUser = GiftconUser.objects.create(userName=user_name,userTel=user_tel)


    # StoreOrder(주문내역)1
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    date = str(datetime.datetime.now().strftime('%Y%m%d'))

    storeOrder = StoreOrder.objects.create(order_date=now,member_no_id=login,order_price=total_price,order_discount=order_discount,order_payment=order_payment,order_method=1,order_state=1,giftconUser_no_id=giftconUser.giftconUser_no)
    order_no = str(storeOrder.order_no)
    storeOrder.order_number = date + order_no
    storeOrder.save()
    giftconUser.order_number=storeOrder.order_number
    giftconUser.save()

    #포인트 적립
        # 실구매가의 0.05%적립

    pointrule = PointRule.objects.get(PointRule_no=5)
    point = int(order_payment) * (pointrule.pointRule/100)


    pointUse = PointUse.objects.create(pc_no_id=2,member_no_id=login,savepoint=point,usepoint=0,pointUse_place='온라인/스토어',pointUse_date=now)
    
    storeOrder.pointUse_no_id = pointUse.pointUse_no
    storeOrder.save()

    po = Point.objects.get(pc_no_id=2,member_no_id =login)

    po.point = int(po.point) + int(point)
    po.save()





    ## 상품별로 생성 되어야 하는 항목

    for add in addList :
        sp_no = add.sp_no_id   # 품목명
        product = StoreProduct.objects.get(sp_no=sp_no)
    
        if product.sp_discount != None :    # 패키지
            item = 1
            price = product.sp_price
            payment = product.sp_discount
            count = add.addList_count  # 구매수량
            discount = product.sp_price - product.sp_discount
        else :  # 일반상품
            item = 3
            price = product.sp_price
            payment = product.sp_price
            count = add.addList_count 
            discount = 0




        total_price = int(price) * int(count)
        order_discount = int(discount) * int(count)
        order_payment = int(payment) * int(count)

        #####################################동일내역



        # ProductOrder(주문상품 정보)2
        productOrder = ProductOrder.objects.create(order_no_id=storeOrder.order_no,order_number=storeOrder.order_number,sp_no_id=sp_no,order_count=count,order_price=price,order_discount=discount)




        #####################################변동
        # 기프트콘 등록
        

        today = datetime.date.today()

        giftconCategory = GiftconCategory.objects.all()
        
        ran = str(random.randrange(1000000,10000000))


        ### 일반상품 item == 3
        if item == 3 :
            p = datetime.timedelta(days=(30*int(product.sp_periodNumber)))
            period = today + p
                
            for c in range(0,int(count)) :
                ran = str(random.randrange(1000000,10000000))
                giftcon = Giftcon.objects.create(sp_no_id=sp_no,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 5)
                giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                giftcon.save()

                giftconCategory = GiftconCategory.objects.get(sc_no_id=product.sc_no)
                giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                giftcon.save()            

        
        ### 패키지상품
        elif item == 1 :
            package = PackageProduct.objects.filter(sp_no_id=sp_no)
            for c in range(0,int(count)) :    #구매갯수
                for pack in package :   # 패키지 내부상품
                    for c in range(0,int(pack.pp_count)) : # 패키지 내부 상품의 갯수
                        p = datetime.timedelta(days=(30*int(pack.pp_periodNumber)))
                        period = today + p

                        ran = str(random.randrange(1000000,10000000))
                        giftcon = Giftcon.objects.create(sp_no_id=sp_no,pp_no_id=pack.pp_no,order_no_id=storeOrder.order_no,order_day=now,giftcon_period=period,gs_no_id = 5)
                        giftcon.giftcon_number = str(giftcon.giftcon_no) + ran
                        giftcon.save()

                        giftconCategory = GiftconCategory.objects.get(pp_no_id=pack.pp_no)
                        giftcon.gc_categoryNo = giftconCategory.gc_categoryNo
                        giftcon.save()



    
    
    user = GiftconUser.objects.get(order_number=storeOrder.order_number)


    addList.delete()

    text = "결제가 완료되었습니다"
    url ="/user/mycgv/payment/detail?no=" + str(storeOrder.order_no)

    context = {
        'login' : login,
        'category' : category,

        'text' : text,
        'url' : url,




    }
    return render(request,'result.html',context)

