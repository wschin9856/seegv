from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from SEEGV.models import FQ,News,Members,Ea,Theater,Region,GroupAsk
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
def index(request:HttpRequest):
    login=request.session.get("login")
    news = News.objects.filter().all().order_by('-nw_date','-nw_no')[0:5]
    context = {
        'login':login,
        'news':news,
    }
    return render(request,'support.html',context)
# Create your views here.
def frequency(request:HttpRequest):
    login=request.session.get("login")
    code = request.GET.get("code",'0')
    searchtext = request.GET.get("searchtext",None)
    if code=='0' and searchtext != None:
        fq=FQ.objects.filter(fq_title__contains=searchtext)
    elif code=='0':
        fq=FQ.objects.all()
    else:
        fq=FQ.objects.filter(fqo_name=code)
    fqcount=fq.count()
    paginator = Paginator(fq, 9)  # Change 10 to the number of items per page you desire
    page_number = request.GET.get('page')
    try:
        fq = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fq = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fq = paginator.page(paginator.num_pages)

    context = {
        'login': login,
        'fq': fq,
        'searchtext': searchtext,
        'fqcount':fqcount,
        'code':code,
    }
    return render(request, 'support_fre.html', context)
def detail(request:HttpRequest):
    login=request.session.get("login")
    no1 = request.GET.get("no")
    freq = FQ.objects.get(pk=int(no1))
    freq.fq_hit+=1
    freq.save()
    freq.fq_content = freq.fq_content.replace('\r\n','<br>')
    try:
        pr_freq = FQ.objects.get(pk=freq.pk-1);
    except:
        pr_freq = None
    try:
        af_freq = FQ.objects.get(pk=freq.pk+1);
    except:
        af_freq = None
    context = {
        'login':login,
        'freq':freq,
        'pr_freq':pr_freq,
        'af_freq':af_freq,
    }
    return render(request,'support_detail.html',context)
def news(request:HttpRequest):
    login=request.session.get("login")
    code = request.GET.get("code",'0')
    searchtext = request.GET.get("searchtext",None)
    if code=='0' and searchtext != None:
        fq=News.objects.filter(nw_title__contains=searchtext)
    elif code=='0':
        fq=News.objects.all()
    else:
        fq=News.objects.filter(nwo_name=code)
    fqcount=fq.count()
    paginator = Paginator(fq, 9)  # Change 10 to the number of items per page you desire
    page_number = request.GET.get('page')
    try:
        fq = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        fq = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        fq = paginator.page(paginator.num_pages)

    context = {
        'login': login,
        'fq': fq,
        'searchtext': searchtext,
        'fqcount':fqcount,
        'code':code,
    }
    return render(request, 'support_news.html', context)
def detail2(request:HttpRequest):
    login=request.session.get("login")
    no1 = request.GET.get("no")
    freq = News.objects.get(pk=int(no1))
    freq.nw_hit+=1
    freq.save()
    freq.nw_content = freq.nw_content.replace('\r\n','<br>')
    try:
        pr_freq = News.objects.get(pk=freq.pk-1);
    except:
        pr_freq = None
    try:
        af_freq = News.objects.get(pk=freq.pk+1);
    except:
        af_freq = None
    context = {
        'login':login,
        'freq':freq,
        'pr_freq':pr_freq,
        'af_freq':af_freq,
    }
    return render(request,'support_detail2.html',context)
def email(request:HttpRequest):
    login=request.session.get('login')
    member = Members.objects.get(pk=login)
    region = Region.objects.all()
    context ={
        'login':login,
        'member':member,
        'region':region,
    }
    return render(request,'support_email.html',context)
def emailresult(request:HttpRequest):
    login=request.session.get('login')
    op = request.POST.get('askvalue')
    title = request.POST.get('title')
    content = request.POST.get('content')
    files = request.FILES.get('files')
    regdate = timezone.now().date()
    state = '답변대기중'
    satisfy = '평가대기중'
    mcontent = '답변대기중'
    member_no = Members.objects.get(pk=login)
    theater_no = request.POST.get('theaterselect')
    ea = Ea.objects.create(ea_op=op,ea_title=title,ea_content=content,ea_file=files,ea_regdate=regdate,ea_state=state,ea_satisfy=satisfy,ea_mcontent=mcontent,member_no=member_no,theater_no_id=theater_no)
    ea.save()
    return redirect('/support/email/')
def group(request:HttpRequest):
    login=request.session.get('login')
    region = Region.objects.all()
    context = {
        'login':login,
        'region':region,
    }
    return render(request,'support_group.html',context)
def groupresult(request:HttpRequest):
    login=request.POST.get('login')
    date = request.POST.get('date')
    time = request.POST.get('time')
    person = request.POST.get('person')
    content = request.POST.get('content')
    membername = request.POST.get('memberN')
    tel = request.POST.get('tel')
    email = request.POST.get('email')
    theater = request.POST.get('theater')
    ga = GroupAsk.objects.create(ga_date=date,ga_time=time,ga_person=person,ga_content=content,ga_membername=membername,ga_tel=tel,ga_email=email,theater_no_id=theater)
    return redirect ('/support/group')