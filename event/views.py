from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from SEEGV.models import Event,EventCategory,Event_Kind2,Region,Theater,Apply_Theater,ApplyUrl,Event_Method,Members,VipGrade_option,ApplyMember,Ocb_option1,Ocb_option2,Vipstamp,Vbo,VipClient,Vmobiec_option,VIPcouponmemberManager,VipGrade_manage,VIPbenifitmemberManager,VIPbenifitotherManager
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models.functions import Concat
from django.db.models import F, Value, IntegerField, CharField
from datetime import datetime, timedelta
def get_theaters(request):
    region_id = request.GET.get('region_id')
    theaters = Theater.objects.filter(Region_no_id=region_id).values('no', 'name') 
    theaters_list = list(theaters)
    return JsonResponse({'theaters': theaters_list})

def check_apply(request):
    member_no = request.POST.get('member_no')
    event_no = request.POST.get('event_no')
    ap = ApplyMember.objects.filter(member_no_id=member_no,event_no_id=event_no)
    if ap:
        return JsonResponse({'indata': True})
    else:
        return JsonResponse({'indata': False})

def apply_events(request:HttpRequest):
    event_get = request.GET.get('no')
    login = request.session.get('login')
    member_no = Members.objects.get(pk = int(login))
    event_no = Event.objects.get(pk=int(event_get))
    nowdate = timezone.now().date()
    event=ApplyMember.objects.create(event_no=event_no,member_no=member_no,aM_date=nowdate,aM_win=None)
    apply_member = ApplyMember.objects.all()
    context ={
        'member_no':member_no,
        'event_no':event_no,
        'event':event,
        'apply_member':apply_member
    }
    return render(request,'event/result.html',context)

def event(request:HttpRequest):
    rl = Region.objects.all()
    tl = Theater.objects.all()
    login = request.session.get('login')
    try:
        list=Event.objects.all().distinct().order_by('event_no')
        theater_code = int(request.GET.get('theatercode','0'))
        code = int(request.GET.get('code','1'))
        page = int(request.GET.get('page','2'))
        pageR = page*3
        if code ==1:
            ec = EventCategory.objects.filter(ek_no2_id__in=[1,5])
        elif code == 2:
            ec = EventCategory.objects.filter(ek_no2_id__in=[2])
        elif code == 3:
            ec = EventCategory.objects.filter(ek_no2_id__in=[3,4])
        elif code == 4:
            if theater_code != 0:
                ec=Apply_Theater.objects.filter(Theater_no_id=theater_code)
            else:
                ec=EventCategory.objects.filter(ek_no2_id=6)
        elif code == 5:
            ec = EventCategory.objects.filter(ek_no2_id__in=[7,8,9,10])
        else:
            ec = EventCategory.objects.all()
        ec_no = ec.count()
        if ec_no-pageR>0:
            ec = ec[0:pageR]
        else :
            ec = ec
    except:
        list=Event.objects.all()
        ec = EventCategory.objects.all()
        code = 0
        page = 0 

    context = {
        'login' : login,
        'ecnum' : ec_no,
        'code' : code,
        'page' : page,
        'List' : list,
        'ec':ec,
        'rl':rl,
        'tl':tl,
    }
    return render(request,'event/event.html',context)
def eventContent(request:HttpRequest):
    login = request.session.get("login")
    event_no = int(request.GET.get('no'))
    content = Event.objects.get(event_no=event_no)
    option = EventCategory.objects.filter(event_no_id = event_no)
    try:
        urln = ApplyUrl.objects.get(event_no_id = event_no)
    except:
        urln = None
    try:
        member = Members.objects.get(member_no = int(login))
    except:
        member=None
    context = {
        'member':member,
        'content' : content,
        'option' : option,
        'urln':urln,
        'login':login,
        'event_no':event_no,
    }
    return render(request,'event/eventContent.html',context)
def benefit(request:HttpRequest):
    login = request.session.get('login')
    code = int(request.GET.get('code','1'))
    page = int(request.GET.get('page','1'))
    pageR = page*3
    list=Event.objects.all()
    instance = EventCategory.objects.filter(ek_no2_id=7).order_by('event_no')
    ec = EventCategory.objects.filter(ek_no2_id__in=[7,8,9,10])
    try:
        list=Event.objects.all().distinct().order_by('event_no')
        code = int(request.GET.get('code'))
        page = int(request.GET.get('page','1'))
        if code ==6:
            ec = EventCategory.objects.filter(ek_no2_id__in=[7,8,9,10])
        elif code == 7:
            ec = EventCategory.objects.filter(ek_no2_id=7)
        elif code == 8:
            ec = EventCategory.objects.filter(ek_no2_id=8)
        elif code == 9:
            ec = EventCategory.objects.filter(ek_no2_id=9)
        elif code == 10:
            ec = EventCategory.objects.filter(ek_no2_id=10)
        else:
            ec = EventCategory.objects.all()
        ec_no = ec.count()
        if ec_no-pageR>0:
            ec = ec[0:pageR]
        else :
            ec = ec
    except:
        list=Event.objects.all()
        ec = EventCategory.objects.all()
        code = 0
    context = {
        'login' : login,
        'code' : code,
        'page' : page,
        'List' : list,
        'ec':ec,
        'instance' : instance,
    }
    return render(request,'event/benefit.html',context)

def endevent(request: HttpRequest):
    login = request.session.get('login')
    nowdate = timezone.now().date()
    abc = Event.objects.filter(event_end__lt=nowdate)
    
    context = {
        'login' : login,
        'nowdate': nowdate,
        'list': abc,
    }
    return render(request, 'event/endevent.html', context)
def ajaxtest(request:HttpRequest):
    rl = Region.objects.all()
    tl = Theater.objects.all()
    context = {
        'rl':rl,
        'tl':tl,
    }
    return render(request,'event/ajaxtest.html',context)
def vip(request:HttpRequest):
    login = int(request.session.get('login'))
    member = Members.objects.get(pk=login)
    vipG = VipGrade_option.objects.all()
    ocb1=Ocb_option1.objects.all()
    ocb2=Ocb_option2.objects.all()
    vipstamp1 = Vipstamp.objects.filter(vso2_no_id__in=[1,2]).order_by('-vipgo_no_id','vso2_no_id')
    vipstamp2 = Vipstamp.objects.filter(vso2_no_id=3).order_by('-vipgo_no_id','vso2_no_id')
    vips_numbers = list(vipstamp1.values_list('vips_number', flat=True))
    groupV = [vips_numbers[i:i+2] for i in range(0, len(vips_numbers), 2)]
    vbo = Vbo.objects.filter(vboo_no_id=1).order_by('vboo_no_id','-vipgo_no_id')
    vbo2 = Vbo.objects.filter(vboo_no_id=2).order_by('vboo_no_id','-vipgo_no_id')
    vbo3 = Vbo.objects.filter(vboo_no_id=3).order_by('vboo_no_id','-vipgo_no_id')
    vbo4 = Vbo.objects.filter(vboo_no_id=4).order_by('vboo_no_id','-vipgo_no_id')
    vbo5 = Vbo.objects.filter(vboo_no_id=5).order_by('vboo_no_id','-vipgo_no_id')
    context = {
        'login':login,
        'member':member,
        'vipg':vipG,
        'ocb1':ocb1,
        'ocb2':ocb2,
        'vipstamp1':vipstamp1,
        'vipstamp2':vipstamp2,
        'groupV':groupV,
        'vbo':vbo,
        'vbo2':vbo2,
        'vbo3':vbo3,
        'vbo4':vbo4,
        'vbo5':vbo5,
        
    }
    return render(request,'event/vip.html',context)
def get_grade(request):
    nowgrade = request.POST.get('nowgrade')
    a = VipGrade_option.objects.get(vipgo_name=nowgrade)
    if(a.vipgo_no>=5):
        a=a.vipgo_no
    else:
        a = a.vipgo_no+1
    #print(a)
    grade = VipGrade_option.objects.filter(vipgo_no=a).values('vipgo_name','vipgo_score')
    grade = list(grade)
    #print(grade)
    return JsonResponse({'grade': grade})
def vip_faq(request:HttpRequest):
    searchtext = request.GET.get("searchtext",None)
    if searchtext != None:
        faq = VipClient.objects.filter(vipg_title__contains = searchtext)
    else:
        faq = VipClient.objects.all()
    login=request.session.get('login')
    
    context={
        'login':login,
        'faq':faq,
    }
    return render(request,'event/vip_faq.html',context)
def vip_special(request:HttpRequest):
    login=request.session.get('login')
    context = {
        'login':login,
    }
    return render(request,'event/vip_special.html',context)
def vip_coupons(request:HttpRequest):
    login=request.session.get('login')
    member = Members.objects.get(pk=login)
    #print(member.member_class.vipgo_no)
    a=member.member_class.vipgo_no
    #print(a)
    acoupon = Vmobiec_option.objects.filter(vipgo_no_id=int(a),vmco_op='A')
    bcoupon = Vmobiec_option.objects.filter(vipgo_no_id=int(a),vmco_op='B')
    allcoupon = Vmobiec_option.objects.filter(vipgo_no_id=int(a),vmco_op=None)
    context = {
        'login':login,
        'member':member,
        'acoupon':acoupon,
        'bcoupon':bcoupon,
        'allcoupon':allcoupon,
    }
    return render(request,'event/vip_coupons.html',context)
def vip_couponset(request:HttpRequest):
    login=request.session.get('login')
    code=request.GET.get('code')
    print(code)
    member = Members.objects.get(pk=login)
    startdate = VipGrade_manage.objects.filter(member_no=login,vigm_ed=None)
    start_date = startdate[0].vigm_sd
    end_date = start_date + timedelta(days=365)
    a=member.member_class.vipgo_no
    acoupon = Vmobiec_option.objects.filter(vipgo_no_id=int(a),vmco_op=code).values('onco2_no_id','vmco_score')
    #print(list(acoupon))
    for i in acoupon:
        #print(i['onco2_no_id'])
        #print(i['vmco_score'])
        VIPcouponmemberManager.objects.create(onco2_no_id=i['onco2_no_id'],vipcm_number=i['vmco_score'],member_no_id=login,vipcm_start=start_date,vipcm_end=end_date)
        #print(list(acoupon))
    allcoupon = Vmobiec_option.objects.filter(vipgo_no_id=int(a),vmco_op=None).values('onco2_no_id','vmco_score')
    for i in allcoupon:
        #print(i['onco2_no_id'])
        #print(i['vmco_score'])
        VIPcouponmemberManager.objects.create(onco2_no_id=i['onco2_no_id'],vipcm_number=i['vmco_score'],member_no_id=login,vipcm_start=start_date,vipcm_end=end_date)
        #print(list(acoupon))  
    return redirect('/event/vip/coupons')
def vip_benefitset(request:HttpRequest):
    member = Members.objects.all().values('member_no','member_class_id')
    for i in member:
        #print(i['member_no'])
        temp = Vipstamp.objects.filter(vipgo_no_id=i['member_class_id']).values('vso2_no_id','vips_number')
        for j in temp:
            #print(j['vso2_no_id'])
            #print(j['vips_number'])
            try:
                VIPbenifitmemberManager.objects.create(member_no_id=i['member_no'],vso2_no_id=j['vso2_no_id'],vbmm_number=j['vips_number'])
            except Exception as e:
                print("에러 발생:", e)
        temp2 = Vbo.objects.filter(vipgo_no_id=i['member_class_id']).values('vboo_no_id','vbo_price')
        print(temp2)
        for k in temp2:
                startdate = VipGrade_manage.objects.filter(member_no_id=i['member_no'],vigm_ed=None)
                if startdate.exists():  # 쿼리셋에 결과가 있는지 확인합니다.    
                    start_date = startdate[0].vigm_sd
                    end_date = start_date + timedelta(days=365)
                    try:
                        VIPbenifitotherManager.objects.create(member_no_id=i['member_no'],vboo_no_id=k['vboo_no_id'],vipbo_number=k['vbo_price'],vipbo_start=start_date,vipbo_end=end_date)
                    except Exception as e:
                        print("에러 발생:", e) 
                    
    return redirect('/event/vip')

def vip_mycoupon(request:HttpRequest):
    login = request.session.get('login')
    member = Members.objects.get(pk=login) 
    nowdate = timezone.now()
    #print(nowdate)
    coupon = VIPcouponmemberManager.objects.filter(vipcm_end__gt=nowdate,member_no_id=member)
    benefit = VIPbenifitmemberManager.objects.filter(member_no_id=member)
    other = VIPbenifitotherManager.objects.filter(member_no_id=member)
    context={
        'login':login,
        'member':member,
        'coupon':coupon,
        'benifit':benefit,
        'other':other,
    }
    return render(request,'event/vip_mycoupon.html',context)