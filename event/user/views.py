from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse,JsonResponse
from SEEGV.models import Profile,Members, MemberJoinDate,Point,Terms,Agreement,Region,Theater,Bookmark,ApplyMember,Event,Giftcon,MoviePreview,StoreProduct,PackageProduct,Movie,Giftcard,StoreOrder,ProductOrder,GiftconUser,GiftcardUse,PointUse
from datetime import datetime
from json import dumps
import json





from django.core.paginator import Paginator 


from django.conf import settings
#현교 코드------------------------
from django.utils import timezone
#---------------------------------
from django.conf import settings






#민국-----------
def check_login(request):
    
    login_id = request.session.get("login_id")
    is_logged_in = login_id is not None
    return JsonResponse({'is_logged_in': is_logged_in})

def movielog(request:HttpRequest):
    login = request.session.get("login")
    login_id = request.session.get("login_id")
    member = Members.objects.get(member_id=login_id)
    member_no = member.member_no
    movielist = MoviePreview.objects.filter(member_no=member_no)
    ml = Movie.objects.filter(no__in=movielist.values_list('Movie_no', flat=True))
    currentdate = timezone.now().date()

    context = {
        'ml':ml,
        'login': login,
        'currentdate':currentdate,
    }
    return render(request,'mycgv_movielog.html',context)


def movielog(request:HttpRequest):
    login = request.session.get("login")
    login_id = request.session.get("login_id")
    member = Members.objects.get(member_id=login_id)
    member_no = member.member_no
    movielist = MoviePreview.objects.filter(member_no=member_no,PreEgg_no=1)
    ml = Movie.objects.filter(no__in=movielist.values_list('Movie_no', flat=True))
    currentdate = timezone.now().date()
    for movie in ml:
        days_opening = (movie.opendate - currentdate).days
        movie.d_day = days_opening

    context = {
        'ml':ml,
        'login': login,
        'currentdate':currentdate,
        'premovies':movielist,
    }
    return render(request,'mycgv_movielog.html',context)




def movielogdelete(request):

    member_no = request.GET.get('member')
    premovie = request.GET.get('premovie')
    premovies = request.GET.get('all')

    MoviePreview.objects.filter(member_no=member_no,Movie_no=premovie).delete()
    



    return JsonResponse({'message': 'Preview saved successfully'})

#------------------------





def get_win(request):
    login = request.session.get("login")
    code = request.GET.get("code")
    try:
        apply = ApplyMember.objects.get(event_no_id=int(code),member_no_id=int(login),aM_win=1)
        return JsonResponse({'indata':True})
    except :
        return JsonResponse({'indata':False})
def myevent(request:HttpRequest):
    login = request.session.get("login")
    member = Members.objects.get(pk=int(login))
    apevent = ApplyMember.objects.filter(member_no=member.member_no)
    nowdate = timezone.now().date()
    context ={
        'login':login,
        'member':member,
        'apevent' :apevent,
        'nowdate':nowdate
    }
    return render(request,'mycgv_event.html',context)
# Create your views here.


def myeventresult(request:HttpRequest):
    login = request.session.get("login")
    nowdate = timezone.now().date()
    events = Event.objects.filter(event_Announce__lte=nowdate)
    context = {
        'login':login,
        'events':events,
    }
    return render(request,'mycgv_eventresult.html',context)

def myeventdetail(request:HttpRequest):
    login = request.session.get("login")
    code = request.GET.get("code")
    event = Event.objects.get(pk=int(code))
    apply = ApplyMember.objects.filter(event_no_id=int(code),aM_win=1)
    context = {
        'login':login,
        'apply':apply,
        'event':event,
    }
    return render(request,'mycgv_eventdetail.html',context)





# Create your views here.

def index(request:HttpRequest) :
    login = request.session.get("login")

    context = {
        'login' : login

    }
    return render(request,'index.html',context)



############### 로그인 로그아웃 ###############

def login(request:HttpRequest) :
    id = request.POST.get('id')     # POST 방식으로 받아온 ID가있으면 해당 아이디 표시
    returnURL = request.GET.get('returnURL')

    if returnURL == None :
        returnURL = '/'

    check = False
    if id == None or id == '':      # 받아온 아이디가 없는 경우
        id = request.COOKIES.get('ckid')    # 쿠키에 저장된 아이디 사용
        if id != None:              # 쿠키로 저장된 아이디가 있는 경우
            check = True            # html에서 쿠키박스 체크가 되어있는 상태
        else:                       # 쿠키로 저장된 아이디가 없는경우   
            id = ''                 # 아이디를 비울 것

    context = {
        "id" : id,
        'check' : check,
        'returnURL' : returnURL,
    }

    return render(request,'login.html',context)


def login_result(request:HttpRequest) :
    returnURL = request.GET.get('returnURL')

    id = request.POST.get('id')
    pw = request.POST.get('pw')
    check = False   # 로그인 성공 여부확인
    ## 로그인 확인

    # 아이디 확인
    try :
        Members.objects.get(member_id=id)
    except :
        text = "존재하지 않는 아이디 입니다."
        url = '/user/login?returnURL=/'
        check = False        
    else :
        # 비밀번호 확인
        try :
            members = Members.objects.get(member_id=id,member_pw=pw)
        except :
            text = "비밀번호를 다시 입력하세요."
            url = '/user/login?returnURL=/'
        else :
            if members.memberInfo_no_id == 1 :   # 이용중
                text = id + "님이 로그인 하셨습니다"
                url = returnURL
                check = True

                # 로그인 세션 저장
                request.session['login'] = members.member_no
                request.session['login_id'] = members.member_id
                request.session['login_name'] = members.member_name
                request.session['type'] = members.memberType_no_id
            
            
            elif members.memberInfo_no_id == 2 : # 휴먼계정
                text = id + "님의 휴먼계정이 해제되었습니다"
                url = returnURL
                check = True
                
                # 로그인 세션 저장
                request.session['login'] = members.member_no
                request.session['login_id'] = members.member_id
                request.session['login_name'] = members.member_name
                request.session['type'] = members.memberType_no_id

            elif members.memberInfo_no_id == 3 : # 탈퇴회원
                text = id + "님은 탈퇴한 회원입니다."
                url = returnURL
            else :
                text = "로그인에 실패했습니다."
                url = returnURL
          
            
    context = {
        'text' : text,
        'check' : check,
        'url' : url,
        
    }      

    response = render(request,'result.html',context)

    ## 쿠키설정
    if check :  # 로그인이 성공한 경우
        ckid = request.POST.get('ckid')

        # 쿠키파일 찾기
        cb = request.COOKIES.get('ckid') # 쿠키파일 불러오기

        if ckid != None : # 체크박스가 선택가 된 상태
            if cb == None : # 쿠키파일이 없을 때
                response.set_cookie('ckid',id,max_age=60*60*24,path='/')
            else : # 쿠키파일이 있을 때
                if cb != id : # 다른 id 쿠키일때
                    response.set_cookie('ckid',id,max_age=60*60*24,path='/')
        else : # 아이디 기억하기 해제
            if cb == id:
                response.delete_cookie('ckid',path='/')
    else :
        pass

    return response



def logout(request:HttpRequest) :

    request.session.pop('login')
    request.session.pop('login_id')
    request.session.pop('login_name')
    request.session.pop('type')

    return redirect('/')


############### 로그인 로그아웃 끝 ###############



############### 회원가입 ###############
def join_check(request:HttpRequest) :

    return render(request,'join_check.html',)



def join(request:HttpRequest) :
    # 미가입회원 > 회원가입창
    # 가입된 회원 > 안내 후 로그인창으로 이동
    # 생년월일 오 기입 > 안내 후 joincheck 로 이동

    # join_check에서 받은 정보 출력
    user_name = request.POST.get("user_name")
    user_birth = request.POST.get("user_birth")
    user_tel = request.POST.get("user_tel")


    tel2 = str(user_tel)[:4]
    tel3 = user_tel[4:]
    years = user_birth[:4]
    month = user_birth[4:6]
    day = user_birth[6:]


    now = datetime.now()
    nowyears = now.year

    text = ''
    url = ''
    check = False

    ## 필수동의 서명
    terms = Terms.objects.all()
    pp = (1,2,3) ## 데이터 베이스 생성해야함


    
 
    ## 생년월일 입력 확인
    if int(years) > int(nowyears) or int(month) > 12 or int(day) > 31 :
            text = "잘못된 생년월일입니다."
            url = "/user/join/check"
    elif user_tel.__len__() != 8 :
            text = "전화번호를 8자리에 맞추어 입력해 주세요."
            url = "/user/join/check"        
    else :
        try: 
            joincheck = Members.objects.get(member_name = user_name, member_years = years, member_month = month,member_day = day, member_tel2 = tel2 , member_tel3 = tel3 )    
        except :    
            check = True ## 회원가입창을 보여줌
        else :
            text = "이미 가입된 회원입니다."
            url = '/user/login?returnURL=/'    
            check = False ## consol창으로 안내
        

    context = {
        'text' : text,
        'url' : url,
        'check' : check,
        'user_name' : user_name,
        'tel2' : tel2,
        'tel3' : tel3,
        'years' : years,
        'month' : month,
        'day' : day,
        'nowyears' : nowyears,
        'terms' : terms,
        'pp' : pp,
    
    }
    return render(request,'join.html',context)


def ajax_post_id(request:HttpRequest):
    s = request.POST.get('id')
    idcheck = Members.objects.values('member_id').filter(member_id=s).first()

    msg = ""
    if idcheck != None and s == idcheck['member_id']:
        msg = "중복된 아이디입니다."
        ic = False
    elif s == '':
        msg = "아이디를 입력하세요"
        ic = False
    elif s.find("admin") != -1 :
        msg = "admin은 아이디로 사용할 수 없는 단어입니다."
        ic = False
    elif s.find("staff") != -1 :
        msg = "admin은 아이디로 사용할 수 없는 단어입니다."
        ic = False

    else:
        msg = "사용가능한 아이디 입니다."
        ic = True

    return JsonResponse({'msg':msg,'ic':ic})




def join_result(request:HttpRequest) :
    name = request.POST.get('name')
    years = request.POST.get('years')
    month = request.POST.get('month')
    day = request.POST.get('day')
    tel2 = request.POST.get('tel2')
    tel3 = request.POST.get('tel3')
    id = request.POST.get('id')
    pw = request.POST.get('pw')
    pwck = request.POST.get('pwck')
    mailid = request.POST.get('mailid')
    mailaddress = request.POST.get('mailaddress')
    gender = request.POST.get('gender')

    checkpage = True


    ic = request.POST.get('ic') # ID 사용 가능 여부 idcheck
    
    now = datetime.now().strftime('%Y-%m-%d')

    text = ''
    url = ''
    check = True

    pp = (1,2,3)    # 해당 페이지에 출력 되는 약관동의 넘버
    ck = {}     # 약관 동의 내역(dic 타입으로 저장 )
    for i in pp :
        ck.update({i : request.POST.get("terms"+str(i))}) 

    
    for i in pp :
        terms = Terms.objects.get(terms_no=i)
        if terms.terms_required == 0 : # 필수동의 일 떄
            if ck.get(i) == '0': #비동의
                text = "필수 동의 항목에 비 동의 시 가입이 불 가능합니다."
                url = "/"
                check = False
                checkpage = False


    idcheck = Members.objects.values('member_id').filter(member_id=id).first()
    if check :
        if id != None and id == idcheck :   # 중복 체크하는 이유 : result 페이지에서 새로고침 하면 같은 아이디로 반복해서 가입됨.
            text = "중복된 아이디입니다."
            checkpage = False
        elif ic == False : 
            text = "사용이 불가능한 아이디입니다."
            checkpage = False
        elif pw != pwck :
            text = "비밀번호가 일치하지 않습니다."
            checkpage = False
        else :
        # 가입시 생성되는 데이더
            try:
                #회원정보
                members = Members.objects.create(member_name=name,member_id=id,member_pw=pw,member_years=years,member_month=month,member_day=day,member_tel1='010',member_tel2=tel2,member_tel3=tel3,member_mailId=mailid,member_mailAddress=mailaddress,member_gender=gender,member_class_id='1',memberType_no_id='2',memberInfo_no_id=1)
                # 가입일
                joindate = MemberJoinDate.objects.create(mjd_date=now,member_no_id=members.member_no)
                # 포인트 적립
                point1 = Point.objects.create(pc_no_id= 1,member_no_id=members.member_no,point=0)
                point2 = Point.objects.create(pc_no_id= 2,member_no_id=members.member_no,point=0)
                point3 = Point.objects.create(pc_no_id= 3,member_no_id=members.member_no,point=0)
                point4 = Point.objects.create(pc_no_id= 4,member_no_id=members.member_no,point=0)
                # 약관 동의
                for i in pp :
                    if Terms.objects.get(terms_no=i) :
                        termcheck = Agreement.objects.create(useragreement=ck.get(i),member_no_id=members.member_no,terms_no_id=i)
                # 프로필 컬럼
                profile = Profile.objects.create(member_no_id=members.member_no)
            except Exception as e :
                print(e)
                text = "가입에 실패했습니다."
                checkpage = False                  
            else :    
                url = "/user/login"
                text = "가입이 완료되었습니다."
                checkpage = True

    # 회원가입 페이지로 다시 넘어갈 때 필요한 데이터
    user_birth = years+month+day
    user_tel = tel2+tel3
    user_name = name
        

    context = {
        'text' : text,
        'url' : url,
        'user_birth' : user_birth,
        'user_tel' : user_tel,
        'user_name' : user_name,
        'checkpage' : checkpage,
 
    }

    return render(request,'join_result.html',context)
############### 회원가입 끝 ###############



############### 아이디 비밀번호 찾기 ###############
def login_findID(request:HttpRequest) :

    pass
    return render(request,'login_findID.html')



def login_findID_result(request:HttpRequest) :
    user_name = request.POST.get("user_name")
    user_birth = request.POST.get("user_birth")
    user_tel = request.POST.get("user_tel")

    tel2 = user_tel[:4]
    tel3 = user_tel[4:]

    years = user_birth[:4]
    month = user_birth[4:6]
    day = user_birth[6:]


    try: 
        findID = Members.objects.get(member_name = user_name, member_years = years, member_month = month,member_day = day, member_tel2 = tel2 , member_tel3 = tel3 )    
    except :    
        text = "아이디가 존재하지 않습니다." 
        check = True
    else :
        text = "귀하의 아이디는 "+ findID.member_id+ "입니다."
        check = False
 
    if check :
        findID = None
        

    
    context = {
        'text' : text,
        'check' : check,
        'user_name' : user_name,
        'user_birth' : user_birth,
        'user_tel' : user_tel,
        'findID' : findID,
    }



    return render(request,'login_findID_result.html',context)


def login_findPW(request:HttpRequest) :
    user_id = request.POST.get("user_id")
    user_name = request.POST.get("user_name")
    user_birth = request.POST.get("user_birth")
    user_tel = request.POST.get("user_tel")

    if user_id == None :
        user_id = ""

    if user_name == None :
        user_name = ""

    if user_birth == None :
        user_birth = ""
 
    if user_tel == None :
        user_tel = ""


    context = {

        'user_id' : user_id,        
        'user_name' : user_name,
        'user_birth' : user_birth,
        'user_tel' : user_tel,

    }

    return render(request,'login_findPW.html',context)



def login_findPW_result(request:HttpRequest) :
    user_id = request.POST.get("user_id")
    user_name = request.POST.get("user_name")
    user_birth = request.POST.get("user_birth")
    user_tel = request.POST.get("user_tel")

    tel2 = user_tel[:4]
    tel3 = user_tel[4:]

    years = user_birth[:4]
    month = user_birth[4:6]
    day = user_birth[6:]


    try: 
        findID = Members.objects.get(member_id = user_id,member_name = user_name, member_years = years, member_month = month,member_day = day, member_tel2 = tel2 , member_tel3 = tel3 )    
    except :    
        text = "존재하지 않는 회원정보입니다." 
        check = True
        url = '/user/login/findPW'
        ## 비밀번호 찾기로 다시 이동
    else :
        text = findID.member_id + "님의 비밀번호는 "+ findID.member_pw+ "입니다."
        check = False
        url = '/user/login?returnURL=/' 

    if check :
        findID = None

    
    context = {
        'text' : text,
        'check' : check,
        'user_id' : user_id,        
        'user_name' : user_name,
        'user_birth' : user_birth,
        'user_tel' : user_tel,
        'findID' : findID,
    }



    return render(request,'login_findPW_result.html',context)


############### 아이디 비밀번호 찾기 끝 ###############


############### 마이페이지 시작 ##################################################

# 마이페이지 메인화면
def mycgv(request:HttpRequest) :
    login = request.session.get("login")
    login_id = request.session.get("login_id")
    login_name = request.session.get("login_name")
    
    member = Members.objects.get(member_id = login_id)

    member_class = member.member_class

    ## 자주가는 cgv 모달설정
    url = request.GET.get('url')
    region = Region.objects.values("no","name")
    theater = Theater.objects.values("no","name","Region_no")    

    ## 자주가는 cgv 표출

    bookmark = Bookmark.objects.filter(member_no_id = login).values('th_no_id')

    no = ""
    name = ""

    # 닉네임 가져오기
    profile = Profile.objects.get(member_no_id = login)


    for i in bookmark :

        f_theater = Theater.objects.get(no=i['th_no_id'])
        if name == "":
            name = f_theater.name
            no = str(i['th_no_id'])
        else :
            name=name+","+ f_theater.name
            no=no+","+ str(i['th_no_id'])

    # 포인트
    pointList = Point.objects.filter(member_no_id = login)
    point = 0
    for p in pointList :
        point = p.point+point







    context = {
        'login_id' : login_id,
        'login_name' : login_name,
        'login' : login,
        'member_class' : member_class,
        'url' : url,
        'region' : region,
        "theater" : theater,
        "no" : no,
        "name" : name,
        "profile" : profile,
        "point" : point,


    }

    return render(request,'mycgv.html',context)


############### 회원탈퇴 시작 ###############
#회원 탈퇴
def mycgv_leave(request:HttpRequest) :
    login = request.session.get("login")
    pw = request.POST.get("pw")


    member = Members.objects.get(member_no=login)

    text = ''
    url = ''

    if pw != None and pw == member.member_pw :
        check = True
    else :
        # 비밀번호를 잘못 입력할 경우 pwcheck로 되돌아 가게 만듬
        check = False
        text = "비밀번호를 잘못 입력하셨습니다."
        url = "/user/mycgv/pwcheck?url=/user/mycgv/leave"
    
    
    context = {
        'login' : login,
        'check' : check,
        'text' : text,
        'url' : url,

    }
    return render(request,'mycgv_leave.html',context)


def mycgv_leave_result(request:HttpRequest) :
    login = request.session.get("login")


    member = Members.objects.get(member_no = login)
    joindate = MemberJoinDate.objects.get(member_no_id = login)

    now = datetime.now().strftime('%Y-%m-%d')

    text = ""
    url = ""

    try :
        # 데이터 삭제대신 데이터베이스에 탈퇴회원으로 info변경, 탈퇴 날짜 등록
        member.memberInfo_no_id = 3
        joindate.mjd_leave = now

        member.save()
        joindate.save()
    except:
        text = "회원 탈퇴에 실패했습니다."
        url = "/user/withdrawal"
    else:
        text = "탈퇴가 완료 되었습니다."
        url = "/"
        
        request.session.pop('login')
        request.session.pop('login_id')
        request.session.pop('login_name')
        request.session.pop('type')



    context = {
        'login' : login,
        'text' : text,
        'url' : url,

    }
    return render(request,'result.html',context)

############### 회원탈퇴 끝 ###############



############### 회원정보 시작 ###############

# 회원정보
def mycgv_myInfo(request:HttpRequest) :
    login = request.session.get("login")
    pw = request.POST.get("pw")


    member = Members.objects.get(member_no=login)

    text = ''
    url = ''

    if pw != None and pw == member.member_pw :
        check = True
    else :
        # 비밀번호를 잘못 입력할 경우 pwcheck로 되돌아 가게 만듬
        check = False
        text = "비밀번호를 잘못 입력하셨습니다."
        url = "/user/mycgv/pwcheck?url=/user/mycgv/myInfo"

    ##############################비밀번호 확인

    id = member.member_id
    name = member.member_name
    years = member.member_years
    month = member.member_month
    day = member.member_day
    tel2 = member.member_tel2
    tel3 = member.member_tel3
    mailid = member.member_mailId
    mailaddress = member.member_mailAddress
    gender = member.member_gender


    context = {
        'login' : login,
        'text' : text,
        'url' : url,
        'check' : check,
        'id' : id,
        'name' : name,
        'years' : years,
        'month' : month,
        'day' : day,
        'tel2' : tel2,
        'tel3' : tel3,
        'mailid' : mailid,
        'mailaddress' : mailaddress,
        'gender' : gender,

    }
    return render(request,'mycgv_myInfo.html',context)



# 회원정보 수정 결과
def mycgv_myInfo_result(request:HttpRequest) :
    login = request.session.get("login")
    tel2 = request.POST.get("tel2")
    tel3 = request.POST.get("tel3")
    mailid = request.POST.get("mailid")
    mailaddress = request.POST.get("mailaddress")
    pw = request.POST.get("pw")
    pwck = request.POST.get("pwck")

    member = Members.objects.get(member_no=login)

    url = "/user/mycgv/pwcheck?url=/user/mycgv/myInfo"
    text = ""
    check = True

    # 전화번호 입력
    if tel2 == "" and tel3 == "" :
        pass
    elif tel2 != "" and tel3 != "" :
        if tel2.__len__() != 4 or tel3.__len__() != 4 :
            text = text + "전화번호가 잘못 입력되었습니다.\\n"
        elif tel2.__len__() == 4 or tel3.__len__() == 4 :
            try :
                member.member_tel2 = tel2
                member.member_tel3 = tel3
                member.save()
            except :
                text = text + "전화번호 변경에 실패했습니다.\\n"
            else :
                text = text + "전화번호가 변경되었습니다.\\n"
    elif tel2 == "" or tel3 == "" :
        text = text + "전화번호가 미 입력된 부분이 있습니다.\\n"
    else :
        text = text + "전화번호 변경에 오류가 생겼습니다.\\n"

    # 이메일 입력
    if mailid == "" and mailaddress == "" :
        pass
    elif mailid != "" and mailaddress != "" :
        try:
            member.member_mailId = mailid
            member.member_mailAddress = mailaddress
            member.save()
        except :
            text = text + "메일 변경에 실패했습니다.\\n"
        else :
            text = text + "메일이 변경되었습니다.\\n"
    elif mailid == "" or mailaddress == "" :
        text = text + "이메일이 미 입력된 부분이 있습니다.\\n"    
    else :
        text = text + "이메일 변경에 오류가 생겼습니다.\\n"       

    # 비밀번호 입력
    if pw == "" and pwck == "" :
        pass
    elif pw != "" and pwck != "" :
        if pw != pwck :
            text = text+ "비밀번호가 동일하지 않습니다.\\n"
        elif pw == pwck :
            try :
                member.member_pw = pw
                member.save()
            except :
                text = text + "비밀번호 변경에 실패했습니다.\\n"
            else :
                text = text + "비밀번호가 변경되었습니다.\\n"              
    else :
        if pw != "" and pwck == "": 
            text = text + "비밀번호 확인란을 입력해주세요.\\n"
        else :
            text = text + "비밀번호 변경에 오류가 생겼습니다.\\n"

    context = {
        'login' : login,
        'url' : url,
        'text' : text,
        'check' : check,

    }
    return render(request,'result.html',context)


############### 회원정보 끝 ###############


############### 비밀번호 확인 시작 ###############
def mycgv_pwcheck(request:HttpRequest) :
    login = request.session.get("login")
    login_id = request.session.get("login_id")
    url = request.GET.get('url')

    context = {
        'login' : login,
        'login_id' : login_id,
        'url' : url,

    }

    return render(request,'mycgv_pwcheck.html',context)
############### 비밀번호 확인 끝 ###############


############### 약관동의 시작 ###############

def mycgv_terms(request:HttpRequest) :
    login = request.session.get("login")
    pw = request.POST.get("pw")


    member = Members.objects.get(member_no=login)

    text = ''
    url = ''

    if pw != None and pw == member.member_pw :
        check = True
    else :
        # 비밀번호를 잘못 입력할 경우 pwcheck로 되돌아 가게 만듬
        check = False
        text = "비밀번호를 잘못 입력하셨습니다."
        url = "/user/mycgv/pwcheck?url=/user/mycgv/terms"

    ################################## 비밀번호 확인

    terms = Terms.objects.all()
    pp = (3,4,5,6,7) ## 데이터 베이스 생성해야함

    agreement = Agreement.objects.filter(member_no_id=login)
    ag = Agreement.objects.values("terms_no_id").filter(member_no_id=login)
    aa = [] # agreement 에서 해당 아이디의 terms_no_id의 값들만 뽑아냄

    for w in ag :
        aa.append(w.get("terms_no_id"))



    context = {
        'login' : login,
        'terms' : terms,
        'pp' : pp,
        'agreement' :agreement,
        'text' : text,
        'url' : url,
        'check' : check,
        'aa' : aa,

    }

    return render(request,'mycgv_terms.html',context)


def mycgv_terms_result(request:HttpRequest) :
    login = request.session.get("login")
    member = Members.objects.get(member_no=login)

    text = '저장되었습니다'
    url = '/user/mycgv/pwcheck?url=/user/mycgv/terms'
    check = True

    pp = (3,4,5,6,7) ## 데이터 베이스 생성해야함
    ck = {}     # 약관 동의 내역(dic 타입으로 저장 )
    for i in pp :
        ck.update({i : request.POST.get("terms"+str(i))}) 

    for i in pp :
        terms = Terms.objects.get(terms_no=i)
        if terms.terms_required == 0 : # 필수동의 일 떄
            if ck.get(i) == '0': #비동의
                text = "필수 동의 항목에 비 동의하여 회원 탈퇴 서비스로 연결됩니다."
                url = "/user/mycgv/pwcheck?url=/user/mycgv/leave"
                check = False

    if check :
        for i in pp :
            Terms.objects.get(terms_no=i)
            try :
                arg = Agreement.objects.get(member_no_id=member.member_no,terms_no_id=i)
            except :
                termcheck = Agreement.objects.create(useragreement=ck.get(i),member_no_id=member.member_no,terms_no_id=i)
                print('저장되었습니다2')                
            else:
                arg.useragreement = ck.get(i)
                arg.save()
                print('저장되었습니다1')




    context = {
        'login' : login,
        'text' :text,
        'url' :url,

    }

    return render(request,'result.html',context)

############### 약관동의 끝 ###############


############### 자주가는 cgv설정 ###############


def mycgv_popup_ajax(request:HttpRequest) :

################################### GET방식
    select_region = request.GET.get('select_region')
    theater = Theater.objects.filter(Region_no_id=select_region)

    msg = ''
    for t in theater :
        # print(t)
        text = '<option name ='+ str(t.name) +' value="'+ str(t.no) +'">' + str(t.name) + '</option>'
        msg= msg + text
    

   


    return JsonResponse({'msg':msg}) #Json 타입으로 반환
    
def mycgv_popup_ajax2(request:HttpRequest) :



################################ POST방식(popup copy4)
    select_theater = request.POST.get('select_theater')
    theater = Theater.objects.get(no=select_theater)

    t = {'no':theater.no, 'name':theater.name}
    msg = theater.name





    return JsonResponse({'msg':msg,'t':t}) #Json 타입으로 반환
    

def mycgv_popup_ajax3(request:HttpRequest) :


################################ POST방식(popup copy4)
    data = request.POST.get('data')
    login = request.session.get("login")

    data1 = json.loads(data) # JSON type을 변환

    try :
        Bookmark.objects.filter(member_no_id=login).delete()
    except :
        pass

    try :
        for i in data1 :
            Bookmark.objects.create(member_no_id=login,th_no_id=i['no'])
    except :
        msg = '저장을 실패했습니다.' 
    else :
        msg = '저장되었습니다.'


    return JsonResponse({'msg':msg}) #Json 타입으로 반환


############### 자주가는 cgv설정 끝 ###############

############### 프로필 설정 ###############

def mycgv_profile(request:HttpRequest) :
    login = request.session.get("login")



    member = Members.objects.get(member_no=login)

    id = member.member_id
    name = member.member_name

    terms = Terms.objects.all()
    pp = [7]

    try :
        profile = Profile.objects.get(member_no_id=login)
    except :
        profile = None




    context = {
        'login' : login,
        'id' : id,
        'name' : name,
        'profile' : profile,
        'terms' : terms,
        'pp' : pp,


    }
    return render(request,'mycgv_profile.html',context)




def mycgv_profile_result(request:HttpRequest) :
    login = request.session.get("login")

    mynickname = request.POST.get("mynickname")
    myprofile = request.FILES.get('myprofile')


    terms = Terms.objects.all()

    image_check = request.POST.get("image_check") # 기존 프로필 이미지 삭제여부 확인

    # ################# 동의 항목 처리 (7번항목만 해야하는지??? 우선 추가 terms가 있다고 생각하고 작성)


    check = True

    pp = [7]    # 해당 페이지에 출력 되는 약관동의 넘버
    ck = {}     # 약관 동의 내역(dic 타입으로 저장 )
    for i in pp :
        ck.update({i : request.POST.get("terms"+str(i))}) 


    for i in pp :
        terms = Terms.objects.get(terms_no=i)  
        if terms.terms_no == 7 :    # int
            # terms 생성/수정
            try :
                agreement = Agreement.objects.get(member_no_id=login,terms_no_id=terms.terms_no)
            except : 
                Agreement.objects.create(useragreement=ck.get(i),member_no_id=login,terms_no_id=terms.terms_no)
            else :
                agreement.useragreement=ck.get(i)

            if ck.get(i) == '0': #비동의 str
                text = "동의 안함 설정 시, [닉네임] [프로필 사진] 를 이용하실 수 없습니다."
                url = "/"
                check = False 
                # terms 생성/수정
            elif ck.get(i) == '1':  # 동의
                check = True 

    ################# 동의 항목 처리


    
    if check :
        url = "/user/mycgv/profile"
        text = "저장되었습니다."
        try :
            profile = Profile.objects.get(member_no_id=login)
        except :       
                text = "저장을 실패했습니다."       
        else : 
            if image_check != "" and image_check != None :   # 기존 프로필이미지 유지
                    
                profile.nickname = mynickname
                profile.save()
            elif image_check == "" or image_check == None : # 기존 프로필 이미지 삭제

                profile.nickname = mynickname
                profile.filename = myprofile
                profile.profileimage = myprofile
                profile.save()
                
    else :
        pass


    context = {
        'login' : login,
        'text' : text,
        'url' : url,
        'terms' : terms,

    }

    return render(request,'result.html',context)


def mycgv_giftcon(request:HttpRequest) :
    login = request.session.get("login")
    con = Giftcon.objects.order_by('giftcon_no').filter(user_no_id=login)
    storeProduct = StoreProduct.objects.all()
    packageProduct = PackageProduct.objects.all()

    ck_type = request.GET.get('type','0')     #전체/영화티켓 - 1/매점상품 -2 GiftconCategory/gc_no,gc_category
    mode = request.GET.get('mode','1')     #사용가능1/사용불가능2/기간경과3/취소4 GiftconState/gs_no,giftcon_state
    
    if ck_type == '0' :
        con = Giftcon.objects.order_by('giftcon_no').filter(user_no_id=login,gs_no_id=mode)
    else :
        con = Giftcon.objects.order_by('giftcon_no').filter(user_no_id=login,gs_no_id=mode,gc_categoryNo=ck_type)


   



    #페이지 네비게이션
    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 10   # 한 페이지당 띄울 글의 개수 

    paginator = Paginator(con,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 

    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지


    context = {
        'login' : login,
        # 'giftcon' : giftcon,
        'storeProduct' : storeProduct,
        'packageProduct' : packageProduct,

        'giftcon' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,
        'mode' : mode,
        'ck_type' : ck_type,
        # 'search' : search, 

    }
    return render(request,'mycgv_giftcon.html',context)


def mycgv_giftcard(request:HttpRequest) :
    login = request.session.get("login")


    card = Giftcard.objects.filter(member_no_id=login)  #쿼리셋으로 열림 >>리스트로 변경



    context = {
        'login' : login,
        'card' : card,
    }
    return render(request,'mycgv_giftcard.html',context)


def mycgv_giftcorn_register(request:HttpRequest) :
    login = request.session.get("login")


    context = {
        'login' : login,
    }
    return render(request,'mycgv_giftcon_register.html',context)




def mycgv_giftcorn_register_result(request:HttpRequest) :
    login = request.session.get("login")

    giftcon_number = request.POST.get('giftcon_number')
    

    
    url = '/user/mycgv/giftcon/register'

    try : 

        giftcon = Giftcon.objects.get(giftcon_number=giftcon_number)
        
    except :
        text = "잘못된 기프트콘 번호 입니다."

    else : 
        if giftcon.user_no == None :
            giftcon.user_no_id = login
            giftcon.save()
            if giftcon.gs_no == '3' :
                text = "기간이 만료된 기프티콘입니다"
            elif giftcon.gs_no == '2' :
                text = "결제가 취소된 기프티콘 입니다."
            else :
                text = "기프트콘이 등록 되었습니다"
                url = '/user/mycgv/giftcon'
        else :
            text = "이미 사용자가 등록된 기프트콘 번호입니다."

    
    context = {

        'login' : login,
        'text' : text,
        'url' : url

        }
    return render(request,'result.html',context)


def mycgv_giftcard_register(request:HttpRequest) :
    login = request.session.get("login")


    context = {
        'login' : login,
    }
    return render(request,'mycgv_giftcard_register.html',context)




def mycgv_giftcard_register_result(request:HttpRequest) :
    login = request.session.get("login")

    giftcard_number = request.POST.get('giftcard_number')
    giftcard_pw = request.POST.get('giftcard_pw')
    

    
    url = '/user/mycgv/giftcard/register'

    try : 

        giftcard = Giftcard.objects.get(giftcard_number=giftcard_number,giftcard_pw=giftcard_pw)
    except :
        text = "기프트콘 번호 및 비밀번호가 잘못 입력되었습니다."
    else : 
        if giftcard.member_no == None :
            giftcard.member_no_id = login
            giftcard.save()
            if giftcard.gs_no == '3' :
                text = "기간이 만료된 기프트카드입니다"
            elif giftcard.gs_no == '2' :
                text = "결제가 취소된 기프트카드입니다."
            else :
                text = "기프트카드가 등록 되었습니다"
                url = '/user/mycgv/giftcard'
        else :
            text = "이미 사용자가 등록된 기프트카드 번호입니다."



    
    context = {

        'login' : login,
        'text' : text,
        'url' : url

        }
    return render(request,'result.html',context)





def mycgv_payment(request:HttpRequest) :
    login = request.session.get("login")
    storeOrder = StoreOrder.objects.order_by("-order_date").filter(member_no_id=login)
    # ProductOrder = 




    #페이지 네비게이션
    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 10   # 한 페이지당 띄울 글의 개수 

    paginator = Paginator(storeOrder,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 

    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지



    context = {
        'login' : login,
        # 'storeOrder' : storeOrder,


        'storeOrder' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,

    }
    return render(request,'mycgv_payment.html',context)




def mycgv_payment_detail(request:HttpRequest) :
    login = request.session.get("login")
    order_no = request.GET.get("no")

    storeOrder = StoreOrder.objects.get(order_no=order_no)
    giftconUser = GiftconUser.objects.get(order_number=storeOrder.order_number)

    ch = 0
    try : 
        giftcard = Giftcard.objects.get(order_no_id=order_no)
    except :    # 기프트콘
        giftcon = Giftcon.objects.filter(order_no_id=order_no)
        productOrder = ProductOrder.objects.filter(order_no_id=order_no)
        List = []
        ch = 1
        print("1번")
        for i in giftcon :
            if i.pp_no == None :    # 일반상품
                List.append({'number':i.giftcon_number,'name':i.sp_no.sp_name,'now':i.gs_no.giftcon_state})
            else :  # 패키지상품
                List.append({'number':i.giftcon_number,'name':i.pp_no.pp_name,'now':i.gs_no.giftcon_state})
    
    
    
    else :      # 기프트카드
        ch= 2
        giftcard = Giftcard.objects.get(order_no_id=order_no)
        productOrder = ProductOrder.objects.filter(order_no_id=order_no)
        List = {'number':giftcard.giftcard_number,'card_pw':giftcard.giftcard_pw,'name': productOrder[0].sp_no.sp_name,'now':giftcard.gs_no.giftcon_state}
        print('2번')



    context = {
        'login' : login,
        'storeOrder' : storeOrder,
        'productOrder' : productOrder,
        'giftconUser' : giftconUser,
        'List' : List,
        'ch' : ch,
        'order_no' : order_no,

    }
    return render(request,'mycgv_payment_detail.html',context)

def mycgv_point(request:HttpRequest) :
    login = request.session.get("login")

    point = Point.objects.filter(member_no_id=login)
    pointUse = PointUse.objects.order_by("-pointUse_date","-pointUse_no").filter(member_no_id=login)









    page = request.GET.get('page','1')  

    MAX_PAGE_CNT = 10   # 페이지 네이게이션에서 보여지는 페이지 수
    MAX_LIST_CNT = 5   # 한 페이지당 띄울 글의 개수 

    paginator = Paginator(pointUse,MAX_LIST_CNT)
    page_obj = paginator.get_page(page) 

    last_page = paginator.num_pages

    current_block = (int(page) - 1) // MAX_PAGE_CNT + 1 # 블럭설정
    start_page = (current_block-1) * MAX_PAGE_CNT +1 #블럭 내 시작 페이지
    end_page = start_page * MAX_PAGE_CNT #블럭 내 끝 페이지







    context = {
        'login' : login,
        'point' : point,
        # 'pointUse' : pointUse,
        'pointUse' : page_obj,
        "last_page" :  last_page,
        "start_page" : start_page,
        "end_page" : end_page,        

    }
    return render(request,'mycgv_point.html',context)
\


def mycgv_refund(request:HttpRequest):
    login = request.session.get("login")

    order_no = request.POST.get("order_no")
    print(order_no)

    storeOrder = StoreOrder.objects.get(order_no=order_no)
    giftconUser = GiftconUser.objects.get(order_number=storeOrder.order_number)
    
    ch = 0
    state = 0
    url = "/user/mycgv/payment/detail?no=" + order_no
    text = ''
    now = datetime.now().strftime('%Y-%m-%d')
    if storeOrder.order_state == 0 :
        text = "이미 환불된 결제내역입니다"

    else :
        try : 
            giftcard = Giftcard.objects.get(order_no_id=order_no)
        except :    # 기프트콘
            giftcon = Giftcon.objects.filter(order_no_id=order_no)
            ch = 1
   
            for i in giftcon :
                if i.gs_no_id == 1 :
                    pass
                else :
                    ch = 2

            if ch == 2 :
                text = "환불이 불가능한 기프트콘이 있습니다."
            elif ch == 1 : 

                text = "환불이 완료 되었습니다."
                try : 
                    pointUse = PointUse.objects.create(pc_no_id=storeOrder.pointUse_no.pc_no_id,member_no_id=login,savepoint=-storeOrder.pointUse_no.savepoint,usepoint=0,pointUse_place=storeOrder.pointUse_no.pointUse_place,pointUse_date=now)
                    pointp = Point.objects.get(member_no_id = login,pc_no_id = pointUse.pc_no_id)

                    p = pointp.point
                    pointp.point = int(p)-int(pointUse.usepoint)
                    pointp.save()
                except Exception as e :
                    print(e)
                    text = "환불을 실패했습니다."
                else :
                    storeOrder.order_state = 0  #결제취소
                    storeOrder.save()
                    for i in giftcon :
                        i.gs_no_id = 4
                        i.save()
                    
            


        else :      # 기프트카드
            giftcard = Giftcard.objects.get(order_no_id=order_no)
            use = GiftcardUse.objects.filter(giftcard_no_id=giftcard.giftcard_no)
            

            if use.__len__() == 0 :
                try :
                    pointUse = PointUse.objects.create(pc_no_id=storeOrder.pointUse_no.pc_no_id,member_no_id=login,savepoint=0,usepoint=storeOrder.pointUse_no.savepoint,pointUse_place=storeOrder.pointUse_no.pointUse_place,pointUse_date=now)
                    pointp = Point.objects.get(member_no_id = login,pc_no_id = pointUse.pc_no_id)

                    p = pointp.point
                    pointp.point = int(p)-int(pointUse.usepoint)
                    pointp.save()

                    storeOrder.order_state = 0  #결제취소
                    storeOrder.save()
                    PointUse.objects.create(pc_no_id=storeOrder.pointUse_no.pc_no_id,member_no_id=login,savepoint=0,usepoint=storeOrder.pointUse_no.savepoint,pointUse_place=storeOrder.pointUse_no.pointUse_place,pointUse_date=now)
                
                except :
                    text = "환불을 실패했습니다."
                else :
                    giftcard.gs_no_id = 4
                    giftcard.save()
                    text = "환불이 완료 되었습니다."
            else :
                text = "사용중인 기프트카드는 환불 할 수 없습니다."




    context = {
        'login' : login,
        'url' : url,
        'text' : text,
        

        }
    return render(request,'result.html',context)