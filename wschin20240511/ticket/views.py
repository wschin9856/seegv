from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.core.paginator import Paginator # 장고에서 페이지네비게이션을 하기위해 만들어진 클래스.
from SEEGV.models import Movie, ViewableAge, Region, Theater, HallSchedule, Hall, Screen, Members, PayCard
from SEEGV.models import Ticket, TicketSeat, HallSeat, SeatType, CouponInfo, Coupon, Card, StepDetail, TicketCoupon
from SEEGV.models import PointCategory, PointUse, VipPointSave, Point
import datetime
# import calendar
from calendar import Calendar
import json



def input_Coupon(request:HttpRequest):
    login = request.session.get("login")
    login_id = request.session.get("login_id")
    login_name = request.session.get("login_name")
    page_name = request.GET.get('page_name')

    if login > 0 :
        member_no = login
    else:
        member_no = 0 

    # 할인쿠폰 정보 추출 
    # <th width="150px;" margin="5px">쿠폰유형</th>
    # <th width="150px;" margin="5px">쿠폰번호</th>
    # <th width="150px;" margin="5px">유효기간</th>
    # <th width="150px;" margin="5px">포인트</th>
    # CouponInfo테이블 
    # coupon_no = models.ForeignKey(Coupon, on_delete=models.CASCADE)할인쿠폰 seq
    # ci_number = models.IntegerField()    
    # mci_date = models.DateField()사용기한
    # member_no = models.ForeignKey(Members, on_delete=models.CASCADE, null=True)
    # cu_date = models.DateField(null=True) 쿠폰사용일
    # class Coupon(models.Model) :
    #     coupon_no = models.BigAutoField(primary_key=True)
    #     cc_no = models.ForeignKey(CouponCategory, on_delete=models.CASCADE)쿠폰 카테고리 seq
    #     coupon_name = models.CharField(max_length=100)
    #     coupon_date = models.DateField()
    #     coupon_discount = models.IntegerField()    
    #     coupon_txt = models.CharField(max_length=100)
    #     coupon_type = models.IntegerField()

    # myCouponInfo = CouponInfo.objects.filter(member_no = member_no, cu_date = None) #쿠폰사용일자가 널(미사용 쿠폰만 추출)
    myCouponInfo = CouponInfo.objects.filter(member_no = member_no) #쿠폰사용일자가 널이 아닌 것(이미 사용한 것)도 추출
    CouponInfo_Arr = [] # 배열 타입으로 해당 고객의 쿠폰정보 저장
    for myInfo in myCouponInfo:
        # print("myInfo.ci_no, myInfo.coupon_no.coupon_no, myInfo.mci_date, myInfo.member_no.member_no")
        # print(myInfo.ci_no, myInfo.coupon_no.coupon_no, myInfo.mci_date, myInfo.member_no.member_no)
        myInfo_dict = {}
        myInfo_dict['ci_no'] = myInfo.ci_no  # CouponInfo(할인쿠폰 개별 정보) 테이블 키값(PK, 시퀀스)
        myInfo_dict['coupon_no']= myInfo.coupon_no.coupon_no # 쿠폰번호
        myInfo_dict['mci_date']= myInfo.mci_date.strftime('%Y-%m-%d') # 날짜 변수를 문자열로 변환, json 변환 시 에러 예방함
        myInfo_dict['member_no']= myInfo.member_no.member_no 
        myInfo_dict['cu_date']= myInfo.cu_date

        myCoupon = Coupon.objects.get(coupon_no=myInfo.coupon_no.coupon_no)
        cc_no = myCoupon.cc_no.cc_no  # 쿠폰 카테고리 seq 1영화관람권,2CGV할인쿠폰,3기프트카드,간편결제/카드사쿠폰
        coupon_name = myCoupon.coupon_name
        coupon_discount = myCoupon.coupon_discount
        myInfo_dict['cc_no']= cc_no
        myInfo_dict['coupon_name']= coupon_name # 쿠폰유형 명칭
        myInfo_dict['coupon_discount']= coupon_discount
        # CouponInfo_dict[myInfo.ci_no] = myInfo_dict  # CouponInfo 테이블 키값(PK, 시퀀스), 결제시 아래 테이블에 저장
        #                                             # TicketCoupon(models.Model): # 결제내역별 세부 사용내역
        # print(cc_no, coupon_name,coupon_discount)
        CouponInfo_Arr.append(myInfo_dict)
    # print("CouponInfo_Arr")
    # print(CouponInfo_Arr)
    CouponInfo_dump = json.dumps(CouponInfo_Arr)
    # print("CouponInfo_dump")
    # print(CouponInfo_dump)

    context = {
        "CouponInfo_Arr" : CouponInfo_dump,  # 쌍따옴표로 바뀐 딕셔너리 자료
        "login_id" : login_id,
        "login_name" : login_name,
        "page_name" : page_name,
    }
    return render(request,'input_coupon.html', context)

####################### ticket(예매 관련 자료 등록 시작) #####################3
def lastpayment(request:HttpRequest):
    login = request.session.get("login")
    # url = '/ticket/seat_sel/payment' 
    url = '/' 
    html_file = 'lastpayment_result.html'

    if login > 0 :
        member_no = login
    else:
        msg = '로그인 상태가 아니어서 등록할 수 없습니다.'
        context = {
            'url' : url,
            'msg' : msg,
        }
        return render(request, html_file, context)
    
    ######## < 좌석정보를 처리
    hallseat_dict_info = json.loads(request.POST.get('hallseat_dict_info'))
    print("hallseat_dict_info")
    print(hallseat_dict_info)
    hallseat_keys = hallseat_dict_info.keys();
    ticket_totalcnt = 0
    for hallseat_key in hallseat_keys:
        print(hallseat_key)
        ticket_totalcnt += 1
    print(ticket_totalcnt)
 
    ######## <Ticket(예매내역) 테이블 저장
    HallSchedule_no = request.POST.get('HallSchedule_no')
    if HallSchedule_no == None:
        msg = '상영스케줄 번호가 없어서 등록에 실패하였습니다.'
        context = {
            'url' : url,
            'msg' : msg,
        }
        return render(request, html_file, context)
    print("HallSchedule_no")
    print(HallSchedule_no)
    ticket_date = datetime.datetime.today()
    
    ticket_totalprice_str = request.POST.get('ticket_totalprice')
    pos1 = ticket_totalprice_str.find('원')
    if pos1 > 0:
        ticket_totalprice = int(ticket_totalprice_str[0:pos1])
    else:
        ticket_totalprice = int(ticket_totalprice_str)

    # 회원정보 추출
    try: 
        myMembers = Members.objects.get(member_no=int(member_no))
        ticket_gender = myMembers.member_gender
        str_today = datetime.datetime.strftime(ticket_date, '%Y-%m-%d')
        this_year = str_today[:4]
        myage = int(this_year) - int(myMembers.member_years)
        ticket_age = myage // 10
    except Exception as e:
        print(e)
        msg = '회원정보 추출에 실패하였습니다.'
        context = {
            'url' : url,
            'msg' : msg,
        }
        return render(request, html_file, context)

    # Ticket 테이블 저장 
    # 외래키가 포함된 테이블에 저장 시 관계 테이블의 데이터를 먼저 찾아야 한다.
    try: 
        new_HallSchedule = HallSchedule.objects.get(no = HallSchedule_no)
    except Exception as e:
        print(e)

    try: 
        newTicket = Ticket.objects.create(HallSchedule_no=new_HallSchedule, ticket_date=ticket_date,
            member_no=member_no, ticket_totalcnt=ticket_totalcnt, ticket_totalprice=ticket_totalprice,
            ticket_gender=ticket_gender, ticket_age=ticket_age, ticket_cancelflag=0)
    except Exception as e:
        print(e)
        msg = 'Ticket정보 등록에 실패하였습니다.'
        context = {
            'url' : url,
            'msg' : msg,
        }
        return render(request, html_file, context)

    for hallseat_key in hallseat_keys:
        try: 
            new_HallSeat = HallSeat.objects.get(no = int(hallseat_key))
        except Exception as e:
            print(e)
        try: 
            new_TicketSeat = TicketSeat.objects.create(ticket_no=newTicket, HallSeat_no=new_HallSeat)
        except Exception as e:
            print(e)
            msg = 'TicketSeat정보 등록에 실패하였습니다.'
            context = {
                'url' : url,
                'msg' : msg,
            }
            return render(request, html_file, context)
        
    ######## < 직렬화 문자여로 전송한 할인쿠폰 정보를 처리, TicketCoupon.value = JSON.stringify(mycoupon_arr)
    ######## < 데이터가 없는 경우에도 배열에 '0' 값이 셋팅되어 옴
    TicketCoupon_str = json.loads(request.POST.get('TicketCoupon'))
    print("TicketCoupon_str")
    print(TicketCoupon_str)

    tc_price_total = 0
    if TicketCoupon_str[0] == '0':
        pass
    else:
        try: 
            new_StepDetail = StepDetail.objects.get(sd_no = 1)
        except Exception as e:
            print(e)
        for tk_arr in TicketCoupon_str: # 1차원 배열 문자열로 키값이 저장되어 있음
            print("tk_arr")
            print(tk_arr)
            print(type(tk_arr))
            tc_date = ticket_date
            new_CouponInfo = CouponInfo.objects.get(ci_no = int(tk_arr))
            try: 
                new_CouponInfo.cudate = tc_date  # 사용한 쿠폰에 날짜 입력하여 더 이상 못쓰게 한다
                new_CouponInfo.save()
            except Exception as e:
                print(e)
            mycoupon_no = new_CouponInfo.coupon_no.coupon_no
            mynew_Coupon = Coupon.objects.get(coupon_no = mycoupon_no)
            tc_price = mynew_Coupon.coupon_discount
            tc_price_total += tc_price
            print("tc_price")
            print(tc_price)
            print(type(tc_price))
            try: 
                new_TicketCoupon = TicketCoupon.objects.create(ticket_no=newTicket, sd_no=new_StepDetail, 
                            coupon_useno=mycoupon_no, tc_date=tc_date, tc_price=tc_price)
            except Exception as e:
                print(e)

    credit_money = ticket_totalprice - tc_price_total
    credit_card_no = request.POST.get('PayCard')
    print("credit_card_no")
    print(credit_card_no)
    print("credit_money")
    print(credit_money)
    
    try: 
        new_Card = Card.objects.get(card_no=int(credit_card_no))
        new_PayCard = PayCard.objects.create(ticket_no=newTicket, card_no=new_Card)
        new_StepDetail2 = StepDetail.objects.get(sd_no = 37) # 최종결제4단계, 신용카드 시퀀스번호
        new_TicketCoupon2 = TicketCoupon.objects.create(ticket_no=newTicket, sd_no=new_StepDetail2, 
                             coupon_useno=new_PayCard.pc_no, tc_date=tc_date, tc_price=credit_money)
    except Exception as e:
        print(e)

    
    # CGV포인트 적립 : PointCategory(참조), PointUse(삽입)
    # 외래키가 포함된 PointUse테이블에 저장 시 관계 PointCategory테이블의 데이터를 먼저 찾아야 한다.
    try: 
        savingpoint = int(ticket_totalprice * 0.05)
        new_PointCategory = PointCategory.objects.get(pc_no=1) # 1 : 매표 구매 포인트
        new_PointUse = PointUse.objects.create(pc_no = new_PointCategory, member_no=myMembers, savepoint=savingpoint, usepoint=0, pointUse_place='online', pointUse_date=tc_date)
    except Exception as e:
        print(e)

    try: 
        new_Point = Point.objects.get(member_no=myMembers, pc_no=new_PointCategory) # 현재 포인트에 추가 적립 포인트 누적 kkkk
        new_Point.point += savingpoint
        new_Point.save()
    except Exception as e: # 존재하지 않는다면 새로운 데이터 추가
        new_Point = Point.objects.create(pc_no=new_PointCategory, member_no=myMembers, point=savingpoint)
        print(e)

    # VIP 포인트 적립
    try: 
        new_VipPointSave = VipPointSave.objects.create(pc_no = new_PointCategory, member_no=myMembers, vipps_point=savingpoint,vipps_date=tc_date)
    except Exception as e:
        print(e)

    try: 
        newTicket.pointUse_no = new_PointUse
        newTicket.vipps_no = new_VipPointSave
        newTicket.save()
    except Exception as e:
        print(e)

    # 테스트용
    # if login > 0 : 
    #     context = {
    #         'url' : url,
    #         'msg' : 'test!!!',
    #     }
    #     return render(request, html_file, context)

    msg = '예매내역 정보 등록에 성공하였습니다.'
    context = {
        'url' : url,
        'msg' : msg,
    }
    return render(request,'lastpayment_result.html', context)
####################### ticket(예매 관련 자료 등록 끝) #####################3

def payment(request:HttpRequest):
    login = request.session.get("login")
    # login_id = request.session.get("login_id")

    movie_no = request.GET.get('movie_no')
    movie_name = json.loads(request.GET.get('movie_name')) # json 따옴표를 벗긴다
    theater_info = json.loads(request.GET.get('theater_info'))
    date_info = json.loads(request.GET.get('date_info'))
    screentime_no = request.GET.get('screentime_no')
    screen_info = json.loads(request.GET.get('screen_info'))
    seat_info = json.loads(request.GET.get('seat_info'))
    count_info = json.loads(request.GET.get('count_info'))
    info3 = json.loads(request.GET.get('info3'))
    info3_2 = json.loads(request.GET.get('info3_2'))
    info3_3 = json.loads(request.GET.get('info3_3'))
    info3_4 = json.loads(request.GET.get('info3_4'))
    info4 = json.loads(request.GET.get('info4'))
    # pay_money = request.GET.get('pay_money')

    pos = movie_name.find(':', 0)
    if pos > -1:
        new_str = movie_name[pos+2:]
    else:
        new_str = movie_name
    movie_name = new_str
    # print(movie_name)

    # print("screentime_no")
    # print(screentime_no)
    hallschedule = HallSchedule.objects.get(no = screentime_no)
    hall_no = hallschedule.Hall_no
    # print("hall_no")
    # print(hall_no.no) 

    selected_seat = []
    selected_seat = seat_info["seat_info"]
    # print(selected_seat)
    hallseat_list = HallSeat.objects.filter(Hall_no=hall_no.no)
    hallseat_dict = {} # 딕셔너리 타입으로 고객이 선택한 좌석정보(좌석시퀀스, 좌석번호) 저장함
    for hallseat in hallseat_list:
        # print(hallseat.no, hallseat.srow, hallseat.scol, hallseat.Hall_no.no)
        for sseat in selected_seat:  
            myrow = sseat[0:1]
            mycol = int(sseat[1:3])  # 정수형 변환, db 쿼리셋트 역시 int 변환하여 비교해야 함
            # print("sseat[1:3]")
            # print(myrow, mycol)
            # print(hallseat.srow, hallseat.scol)
            if hallseat.srow == myrow and int(hallseat.scol) == mycol:  # 홀좌석 시퀀스를 찾아서 좌석번호와 같이 딕셔너리 저장
                hallseat_dict[hallseat.no] = sseat
                break
    # print("hallseat_dict")
    # print(hallseat_dict)
    hallseat_dump = json.dumps(hallseat_dict)
    # print("hallseat_dump")
    # print(hallseat_dump)

    # 할인쿠폰 정보 추출 
    # <th width="150px;" margin="5px">쿠폰유형</th>
    # <th width="150px;" margin="5px">쿠폰번호</th>
    # <th width="150px;" margin="5px">유효기간</th>
    # <th width="150px;" margin="5px">포인트</th>
    # CouponInfo테이블 
    # coupon_no = models.ForeignKey(Coupon, on_delete=models.CASCADE)할인쿠폰 seq
    # ci_number = models.IntegerField()    
    # mci_date = models.DateField()사용기한
    # member_no = models.ForeignKey(Members, on_delete=models.CASCADE, null=True)
    # cu_date = models.DateField(null=True) 쿠폰사용일
    # class Coupon(models.Model) :
    #     coupon_no = models.BigAutoField(primary_key=True)
    #     cc_no = models.ForeignKey(CouponCategory, on_delete=models.CASCADE)쿠폰 카테고리 seq
    #     coupon_name = models.CharField(max_length=100)
    #     coupon_date = models.DateField()
    #     coupon_discount = models.IntegerField()    
    #     coupon_txt = models.CharField(max_length=100)
    #     coupon_type = models.IntegerField()

    if login > 0 :
        member_no = login
    else:
        member_no = 0 
   
    myCouponInfo = CouponInfo.objects.filter(member_no = member_no, cu_date = None) #쿠폰사용일자가 널(미사용 쿠폰만 추출)
    # CouponInfo_dict = {} # 딕셔너리 타입으로 해당 고객의 쿠폰정보 저장
    CouponInfo_Arr = [] # 배열 타입으로 해당 고객의 쿠폰정보 저장
    for myInfo in myCouponInfo:
        # print(myInfo.ci_no, myInfo.coupon_no.coupon_no, myInfo.mci_date, myInfo.member_no.member_no)
        myInfo_dict = {}
        myInfo_dict['ci_no'] = myInfo.ci_no  # CouponInfo(할인쿠폰 개별 정보) 테이블 키값(PK, 시퀀스)
        myInfo_dict['coupon_no']= myInfo.coupon_no.coupon_no # 쿠폰번호
        myInfo_dict['mci_date']= myInfo.mci_date.strftime('%Y-%m-%d') # 날짜 변수를 문자열로 변환, json 변환 시 에러 예방함
        myInfo_dict['member_no']= myInfo.member_no.member_no 

        myCoupon = Coupon.objects.get(coupon_no=myInfo.coupon_no.coupon_no)
        cc_no = myCoupon.cc_no.cc_no  # 쿠폰 카테고리 seq 1영화관람권,2CGV할인쿠폰,3기프트카드,간편결제/카드사쿠폰
        coupon_name = myCoupon.coupon_name
        coupon_discount = myCoupon.coupon_discount
        myInfo_dict['cc_no']= cc_no
        myInfo_dict['coupon_name']= coupon_name # 쿠폰유형 명칭
        myInfo_dict['coupon_discount']= coupon_discount
        # CouponInfo_dict[myInfo.ci_no] = myInfo_dict  # CouponInfo 테이블 키값(PK, 시퀀스), 결제시 아래 테이블에 저장
        #                                             # TicketCoupon(models.Model): # 결제내역별 세부 사용내역
        # print(cc_no, coupon_name,coupon_discount)
        CouponInfo_Arr.append(myInfo_dict)
    # print("CouponInfo_Arr")
    # print(CouponInfo_Arr)
    CouponInfo_dump = json.dumps(CouponInfo_Arr)
    # print("CouponInfo_dump")
    # print(CouponInfo_dump)

    myCard_Arr = []
    try:
        myCard_list = Card.objects.all()
    except Exception as err:        
        print("error!! : ", err)

    for myCard in myCard_list:
        tmp_Arr = []
        tmp_Arr.append(myCard.card_no)
        tmp_Arr.append(myCard.Card_name)
        myCard_Arr.append(tmp_Arr)
    print("myCard_Arr")
    print(myCard_Arr)
    myCard_dump = json.dumps(myCard_Arr)


    context = {
        "movie_no" : movie_no,
        "movie_name" : movie_name,  
        "theater_info" : theater_info,
        "date_info" : date_info,
        "screentime_no" : screentime_no,
        "screen_info" : screen_info,
        "count_info" : count_info,
        "hallseat_dict" : hallseat_dump, #홀좌석 시퀀스를 찾아서 좌석번호와 같이 딕셔너리 저장
        "info3" : info3,
        "info3_2" : info3_2,
        "info3_3" : info3_3,
        "info3_4" : info3_4,
        "info4" : info4,
        "CouponInfo_Arr" : CouponInfo_dump,  # 쌍따옴표로 바뀐 딕셔너리 자료
        "myCard_Arr" : myCard_dump,  
    }
    return render(request,'payment.html', context)



def seat_sel(request:HttpRequest):
    movie_no = request.GET.get('movie_no')
    movie_name = json.loads(request.GET.get('movie_name')) # json 따옴표를 벗긴다
    theater_info = json.loads(request.GET.get('theater_info'))
    date_info = json.loads(request.GET.get('date_info'))
    screentime_no = request.GET.get('screentime_no')
    screen_info = json.loads(request.GET.get('screen_info'))
    
    pos = movie_name.find(':', 0)
    # print("screentime_no")
    # print(screentime_no)

    if pos > -1:
        new_str = movie_name[pos+2:]
    else:
        new_str = movie_name
    movie_name = new_str
    # print(movie_name)


    seattype_list = SeatType.objects.all()
    seattype_dict = {}
    for sl in seattype_list:
        tmpstr = str(sl.no)
        seattype_dict[tmpstr]=sl.name
    # print("seat type")
    # print(seattype_dict)
    seattype_dump = json.dumps(seattype_dict)

    hallschedule = HallSchedule.objects.get(no = screentime_no)
    hall_no = hallschedule.Hall_no
    # print("hall_no")
    # print(hall_no.no)

    # 해당 상영관 홀 좌석정보 정렬하여 전부 전송
    hallseat_list = HallSeat.objects.filter(Hall_no=hall_no.no).order_by('srow', 'no') #정렬
    hallseat_dict = {} # 딕셔너리 타입으로 모든 좌석정보(좌석번호, 좌석유형) 저장함
    for hallseat in hallseat_list:
        # print(hallseat.srow, hallseat.scol)
        srow = hallseat.srow
        scol = hallseat.scol
        if scol.__len__() == 1 :
            scol = '0' + scol
        seat_num = srow + scol # 'A' + '01' 형태로 행열의 좌석정보 저장
        seattype_no = hallseat.SeatType_no.no
        hallseat_dict[seat_num] = seattype_no # 딕셔너리 요소 추가
    # print(hallseat_dict)
    
    hallseat_dump = json.dumps(hallseat_dict)  # 딕셔너리 데이터 키값에 홑따옴표 대신 쌍따옴표를 넣어준다. json 타입으로 전송 시 필요함
    # print(hallseat_dump)

    hall_list = Hall.objects.get(no=hall_no.no) # 테이블 칼럼이름은 models.py 대소문자 가림
    hall_totseat = hall_list.totseat # 상영관 홀의 총 좌석수
    # print("hall_totseat")
    # print(hall_totseat)
    ticket_list = Ticket.objects.filter(HallSchedule_no = screentime_no, ticket_cancelflag = 0) 
    occupied_seat = 0
    ticketseat_dict = {} # 딕셔너리 타입으로 예매된 좌석정보(좌석번호, 좌석유형) 저장함
    for ticket in ticket_list:
        # print(ticket)
        # print("ticket HallSchedule_no")
        # print(ticket.HallSchedule_no.no)
        # print(ticket.ticket_no)
        ticket_no = ticket.ticket_no
        ticketseat_list = TicketSeat.objects.filter(ticket_no = ticket_no) 
        for ticketseat in ticketseat_list:
            # print("ticketseat")
            # print(ticketseat)
            # print(ticketseat.HallSeat_no.no)
            occupied_seat += 1
            hallseat_no = ticketseat.HallSeat_no.no
            hallseat_list = HallSeat.objects.get(no = hallseat_no)
            srow = hallseat_list.srow
            scol = hallseat_list.scol
            if scol.__len__() == 1 :
                scol = '0' + scol
            seat_num = srow + scol 
            seattype_no = hallseat_list.SeatType_no.no
            # print(seat_num)
            # print("seattype_name")
            # print(seattype_name)
            ticketseat_dict[seat_num] = seattype_no
        # print(ticketseat_dict)
        # print(json.dumps(ticketseat_dict))
        ticketseat_dump = json.dumps(ticketseat_dict)  # 딕셔너리 데이터 키값에 홑따옴표 대신 쌍따옴표를 넣어준다. json 타입으로 전송 시 필요함
    avail_seat = int(hall_totseat) - occupied_seat 

    context = {
        "hallseat_dict" : hallseat_dump,  # 쌍따옴표로 바뀐 딕셔너리 자료
        "ticketseat_dict" : ticketseat_dump, # 쌍따옴표로 바뀐 딕셔너리 자료
        "movie_no" : movie_no,
        "movie_name" : movie_name,  
        "theater_info" : theater_info,
        "date_info" : date_info,
        "screentime_no" : screentime_no,
        "screen_info" : screen_info,
        "hall_totseat" : hall_totseat,
        "seattype_dict" : seattype_dump,
        "occupied_seat" : occupied_seat,
        "avail_seat" : avail_seat,
    }
    return render(request,'seat_sel.html', context)


def myrepl(mystr:str): # 대괄호 및 콤마는 다른 글자로 대치
    new_str = ''
    if mystr.find('[') > -1:
        new_str = mystr.replace('[', '(')
    else:
        new_str = mystr
    new_str2 = ''
    if new_str.find(']') > -1:
        new_str2 = new_str.replace(']', ')')
    else:
        new_str2 = new_str

    if new_str2.find(',') > -1:
        new_str = new_str2.replace(',', '.')
    else:
        new_str = new_str2
    return new_str

       
def strToArray(mystr:str) :
    myarr = []
    pos = 0
    fnd_cnt = 0
    while True :
        foundPos = mystr.find('"', pos)
        if foundPos == -1:
            break
        else:
            nextPos = mystr.find('"', foundPos+1)
            if nextPos == -1:
                print("error!")
                break
            else:
                myarr.append( mystr[foundPos+1:nextPos])
                pos = nextPos+1
                fnd_cnt += 1
    # print("myarr")
    # print(myarr)
    return myarr


def strToArray2(mystr:str) :
    myarr = []
    mylen = mystr.__len__() 
    pos = 0
    while True :
        foundPos = mystr.find(',', pos)
        if foundPos == -1: # 마지막처리
            if mystr[pos:mylen].__len__() > 0 :
                myarr.append( mystr[pos:mylen])    
            break 
        else:
            myarr.append( mystr[pos:foundPos])
            pos = foundPos + 1

    print("myarr")
    print(myarr)
    return myarr



def ajax1(request:HttpRequest):
    mydata = request.POST.get('mydata')
    print("mydata : " + mydata)
    print(mydata.__len__())
    
    myarr = strToArray2(mydata)
    click_movie_no = myarr[0]
    click_theater_no = myarr[1]
    click_date = myarr[2]

    th_list = Theater.objects.values('no', 'name', 'Region_no').order_by('Region_no') # values 메소드는 dict type으로 객체를 반환함
    th_arr = [] # 딕셔너리 타입의 극장목록 데이터를 배열에 저장함
    for tl in th_list:
        # print(tl['no'], tl['name'], tl['Region_no'])
        inth = []
        inth.append(tl['no'])
        inth.append(myrepl(tl['name']))
        inth.append(tl['Region_no'])
        th_arr.append(inth)
    # print("th_arr")
    # print(th_arr)


    # Screen 테이블 전체 스크린 타입 seq (4DX, 2D, ScreenX 등)
    screen_list = Screen.objects.all()
    screen_arr = []
    for sl in screen_list:
        inscreen = []
        inscreen.append(sl.no)
        inscreen.append(myrepl(sl.name))
        inscreen.append(myrepl(sl.cate))
        screen_arr.append(inscreen)

    hall_list = Hall.objects.filter(Theater_no=click_theater_no) # 테이블 칼럼이름은 models.py 대소문자 가림
    hall_arr = []
    for hl in hall_list:
        inhall = []
        inhall.append(hl.no)   # 0
        inhall.append(myrepl(hl.name))   # 1
        inhall.append(myrepl(hl.floor))   # 2
        inhall.append(hl.totseat)   # 3
        inhall.append(hl.Screen_no.no)   # 4
        inhall.append(hl.Theater_no.no)   # 5
        for sa in screen_arr:
            if hl.Screen_no.no == sa[0]:
                inhall.append(myrepl(sa[1])) # 6 screen name
                inhall.append(myrepl(sa[2])) # 7 screen category
                break
        hall_arr.append(inhall)
    # print(hall_arr)

    # 상영 스케줄 
    schedule_arr = []
    schedule_list = HallSchedule.objects.values('no', 'ondate', 'stime', 'etime', 'Hall_no', 'Movie_no').filter(ondate=click_date, Movie_no=click_movie_no )
    # print("schedule_list : ")
    # print(schedule_list)
    # for sl in schedule_list:
    #     print("sl : ")
    #     print(sl['no'], sl['ondate'], sl['stime'], sl['etime'], sl['Movie_no'], sl['Hall_no'])

    for sl in schedule_list:
        # print("sl : ")
        # print(sl['no'], sl['ondate'], sl['stime'], sl['etime'], sl['Movie_no'], sl['Hall_no'])
        i=0
        for hl in hall_arr:
            if hl[0] == sl['Hall_no']:
                inschedule = []
                inschedule.append(sl['no']) # arr index : 0
                inschedule.append(sl['ondate']) # 1
                inschedule.append(sl['stime']) # 2
                inschedule.append(sl['etime']) # 3
                inschedule.append(sl['Movie_no']) # 4
                inschedule.append(sl['Hall_no']) # 5
                inschedule.append(myrepl(hl[1]))  # 6 hall name, 문자열 속에 대괄호는 괄호로 대체
                inschedule.append(myrepl(hl[2])) # 7 hall floor
                inschedule.append(myrepl(hl[3])) # 8 totseat 홀 좌석수
                inschedule.append(myrepl(hl[3])) # 9 잔여 좌석수(나중에 예매내역 확인하여 수정할 것)
                inschedule.append(hl[4]) # 10 hall Screen_no
                inschedule.append(hl[5]) # 11 hall Theater_no
                schedule_arr.append(inschedule)
                break;
            i += 1
    # print("schedule_arr")
    # print(schedule_arr)
    
    i = 0
    for hall_ele in hall_arr:  # 홀별로 스케줄 모두 넣음, 스케줄 없는 홀은 카운터 index8 칼럼을 0로 셋팅, 스케줄 있는 홀은 index9에 1차원 배열로 넣음
        j = 0
        tmp_arr = []
        for sch_ele in schedule_arr:
            if hall_ele[0] == sch_ele[5]:  # hall_no
                tmp_arr.append(sch_ele) 
                j += 1
        if j > 0 :
            hall_arr[i].append(j)        # index8 칼럼
            hall_arr[i].append(tmp_arr)  # index9
        else:
            hall_arr[i].append(0)        # index8 칼럼
        i += 1
    
    # for hall_e in hall_arr:
    #     print("hall_arr_element")
    #     print(hall_e)
    context = {
        "hall_list" : hall_arr,
    }
    return JsonResponse(context)
  
def ajax_getCoupon(request:HttpRequest):
    mydata = request.POST.get('mydata')
    print("mydata : " + mydata)
    print(mydata.__len__())
    if mydata.__len__() < 1:
        context = {
            "coupon_Result" : '',
        }
        return JsonResponse(context)
    if mydata.isdigit() :
        mycoupon_no = int(mydata)
    else:
        context = {
            "coupon_Result" : '',
        }
        return JsonResponse(context)

    try:
        myCoupon = Coupon.objects.get(coupon_no=mycoupon_no)
    except Exception as err:        
        print("error!! : ", err)
        context = {
            "coupon_Result" : '',
        }
        return JsonResponse(context)
    else:
        coupon_dict = {}
    cc_no = myCoupon.cc_no.cc_no  # 쿠폰 카테고리 seq 1영화관람권,2CGV할인쿠폰,3기프트카드,간편결제/카드사쿠폰
    coupon_name = myCoupon.coupon_name
    coupon_discount = myCoupon.coupon_discount
    coupon_dict['coupon_no']= myCoupon.coupon_no
    coupon_dict['cc_no']= cc_no
    coupon_dict['coupon_name']= myCoupon.coupon_name # 쿠폰유형 명칭
    coupon_dict['coupon_date']= myCoupon.coupon_date.strftime('%Y-%m-%d') # 날짜 변수를 문자열로 변환, json 변환 시 에러 예방함
    coupon_dict['coupon_discount']= myCoupon.coupon_discount
    coupon_dict['coupon_type']= myCoupon.coupon_type # 0 : 영화 할인 , 1 : 매점 할인
    print("coupon_dict")
    print(coupon_dict)
    context = {
        "coupon_Result" : coupon_dict,
    }
    return JsonResponse(context)


def coupon_regi(request:HttpRequest):
    coupon_no = request.POST.get('coupon_no')
    login = request.session.get("login")
    if login > 0 :
        member_no = login
    else:
        url = '/ticket/seat_sel/payment/input_Coupon/' 
        msg = '로그인 상태가 아니어서 등록할 수 없습니다.'
        context = {
            'url' : url,
            'msg' : msg,
        }
        return render(request,'coupon_regi_result.html', context)
    if coupon_no == None:
        url = '/ticket/seat_sel/payment/input_Coupon/' 
        msg = '쿠폰번호가 없어서 등록에 실패하였습니다.'
        context = {
            'url' : url,
            'msg' : msg,
        }
        return render(request,'coupon_regi_result.html', context)
    try: 
        myCoupon = Coupon.objects.get(coupon_no=int(coupon_no))
        coupon_date = myCoupon.coupon_date
        myMembers = Members.objects.get(member_no=member_no)
        print("coupon_date")
        print(coupon_date)
        CouponInfo.objects.create(coupon_no = myCoupon, ci_number=int(coupon_no), mci_date=coupon_date, member_no=myMembers)
    except Exception as e:
        print(e)
        url = '/ticket/seat_sel/payment/input_Coupon/' 
        msg = '쿠폰등록에 실패하였습니다.'
        context = {
            'url' : url,
            'msg' : msg,
        }
        return render(request,'coupon_regi_result.html', context)
    
    url = '/ticket/seat_sel/payment/input_Coupon/' 
    msg = '쿠폰등록에 성공하였습니다.'
    context = {
        'url' : url,
        'msg' : msg,
    }
    return render(request,'coupon_regi_result.html', context)


def list(request:HttpRequest):
    login = request.session.get("login")
    mytoday = datetime.datetime.today()
    print(mytoday)
    myyear = mytoday.year
    mymonth = mytoday.month
    myday = mytoday.day
    # str_today = datetime.datetime.strftime(mytoday, '%Y-%m-%d')


    cal = Calendar(firstweekday=0) ## 월요일을 주의 시작으로 설정
    # print(cal.monthdatescalendar(myyear, mymonth))

    weekday_list = ['월', '화', '수', '목', '금', '토', '일'] 
    date_arr1 = []
    i = 0
    for day in cal.itermonthdates(myyear, mymonth):
        myyear2 = day.year
        mymonth2 = day.month
        myday2 = day.day
        if myyear2 >= myyear and mymonth2 >= mymonth and myday2 >= myday and mymonth2 == mymonth:
            indate = []
            indate.append(day.strftime('%Y-%m-%d'))
            indate.append(myyear2)
            indate.append(mymonth2)
            indate.append(myday2)
            indate.append(weekday_list[day.weekday()])
            date_arr1.append(indate)
            i += 1
            if i > 20:
                break


    date_arr2 = []  # 월이 바뀌는 경우에 다른 리스트에 저장
    for day in cal.itermonthdates(myyear, mymonth+1):
        myyear2 = day.year
        mymonth2 = day.month
        myday2 = day.day
        if myyear2 >= myyear and mymonth2 > mymonth:
            indate = []
            indate.append(day.strftime('%Y-%m-%d'))
            indate.append(myyear2)
            indate.append(mymonth2)
            indate.append(myday2)
            indate.append(weekday_list[day.weekday()])
            date_arr2.append(indate)
            i += 1
            if i > 10:
                break
    # print(date_arr1, date_arr2)

    # 장고에서 쿼리하는 법 참고사이트 : https://www.qu3vipon.com/django-orm
    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#field-lookups
    try:
        viewable_list = ViewableAge.objects.all()
        # print("viewable_list : ", viewable_list)
        # for vl in viewable_list:
        #     print("vl : ", vl.no, vl.name)

        movie_list = Movie.objects.values('no', 'krname', 'ViewableAge_no').order_by('-no') # values 메소드는 dict type으로 객체를 반환함
        # for ml in movie_list:
        #     print(ml['no'], ml['krname'], ml['ViewableAge_no'])

        i = 0
        for ml in movie_list:
            for vl in viewable_list:
                if ml['ViewableAge_no'] == vl.no:
                    movie_list[i]['ViewableAge_name'] = vl.name   # movie_list라는 dict형 자료구조에 새로운 키값 및 데어터값을 생성하여 추가      
                    break
            i += 1
        # print("new dict : ")
        # print(movie_list)


        region_list = Region.objects.all()
        region_arr = []   # 2차원 list 형태로 저장
        for rl in region_list:
            inline = []              # 안쪽 리스트로 사용할 빈 리스트 생성
            inline.append(rl.no)     
            inline.append(myrepl(rl.name))     
            inline.append(0)  # 3번째 요소는 지역별 극장갯수를 저장하여 html로 넘김
            region_arr.append(inline)
        # print("region_arr : ")
        # print(region_arr)
          
#####################  문자열 내부에 ","는 모두 "."으로, []는 ()으로 치환하여 전달할 것
        th_list = Theater.objects.values('no', 'name', 'Region_no').order_by('Region_no') # values 메소드는 dict type으로 객체를 반환함
        th_arr = [] # 딕셔너리 타입의 극장목록 데이터를 배열에 저장함
        for tl in th_list:
            # print('극장테이블 : ')
            # print(tl['no'], tl['name'], tl['Region_no'])
            i = 0
            for ra in region_arr:
                if tl['Region_no'] == ra[0]:  # 해당 지역에 존재하는 극장 갯수 증가
                    region_arr[i][2] += 1
                    break
                i += 1 
            inth = []
            inth.append(tl['no'])
            inth.append(myrepl(tl['name']))
            inth.append(tl['Region_no'])
            th_arr.append(inth)

        print("th_arr : ")
        print(th_arr)

        # Screen 테이블 전체 스크린 타입 seq (4DX, 2D, ScreenX 등)
        screen_list = Screen.objects.all()
        screen_arr = []
        for sl in screen_list:
            # print("sl : ")
            # print(sl.no, sl.name, sl.cate)
            inscreen = []
            inscreen.append(sl.no)
            inscreen.append(myrepl(sl.name))
            inscreen.append(myrepl(sl.cate))
            screen_arr.append(inscreen)
        # print("screen_arr ")
        # print(screen_arr)

        # Hall 테이블 전체
        hall_list = Hall.objects.all()
        hall_arr = []
        for hl in hall_list:
            # print("hl : ")
            # print(hl.no, hl.name, hl.floor, hl.totseat, hl.Screen_no, hl.Theater_no)
            inhall = []
            inhall.append(hl.no)
            inhall.append(myrepl(hl.name))
            inhall.append(myrepl(hl.floor))
            inhall.append(hl.totseat)
            
            inhall.append(hl.Screen_no.no)   # foreign key 경우에 참조하는 방식이 다름
            inhall.append(hl.Theater_no.no)  # foreign key 경우에 참조하는 방식이 다름
            hall_arr.append(inhall)
        # print("hall_arr")
        # print(hall_arr)


        # 상영 스케줄  HallSchedule      str_today = datetime.datetime.strftime(mytoday, '%Y-%m-%d')
        schedule_list = HallSchedule.objects.filter(ondate__gte=mytoday)
        
        # print("schedule_list : ")
        # print(schedule_list)
        schedule_arr = []
        for sl in schedule_list:
            # print("sl : ")
            # print(sl.no, sl.ondate, sl.stime, sl.etime, sl.Movie_no, sl.Hall_no)
            inschedule = []
            inschedule.append(sl.no) # arr index : 0
            inschedule.append(sl.ondate.strftime('%Y-%m-%d')) # 1
            inschedule.append(sl.stime) # 2
            inschedule.append(sl.etime) # 3
            inschedule.append(sl.Movie_no.no) # 4  foreign key 경우에 참조하는 방식이 다름
            inschedule.append(sl.Hall_no.no) # 5  foreign key 경우에 참조하는 방식이 다름
            i = 0
            for hl in hall_arr:
                if hl[0] == sl.Hall_no.no:
                    inschedule.append(myrepl(hl[1]))  # 6 hall name, 문자열 속에 대괄호는 괄호로 대체
                    inschedule.append(myrepl(hl[2])) # 7 hall floor,  hl[3] totseat항목은 활용하지 않음
                    inschedule.append(hl[4]) # 8 hall Screen_no
                    inschedule.append(hl[5]) # 9 hall Theater_no
                    i += 1
                    for sa in screen_arr:
                        if hl[4] == sa[0]:
                            inschedule.append(myrepl(sa[1])) # 10 screen name
                            inschedule.append(myrepl(sa[2])) # 11 screen category
                            i += 1
                            break

                    for ta in th_arr:
                        if hl[5] == ta[0]:
                            inschedule.append(myrepl(ta[1])) # 12 thearter name(참고용, 필수 아님)
                            inschedule.append(ta[2]) # 13 thearter Region_no(지역번호)
                            break
                    break;

            # 영화명 매칭(참고용, 필수 아님)
            for ml in movie_list:
                if sl.Movie_no.no == ml['no']:
                    inschedule.append(myrepl(ml['krname'])) # 14 영화명
                    break


            if i == 2:  # 매칭되는 관계 데이터 모두 찾았을 경우
                schedule_arr.append(inschedule)
                # print(schedule_arr)

            else:
                print("error! not matching hall and screen : ")
                print(i)

    except Exception as err:        
        print("error!! : ", err)
        msg = err
        movie_list = None
    else:
        msg = 'ok'
        # print('ok : ')
        # print(movie_list)
    

    context = {
        "movie_list" : movie_list,
        "region_list" : region_arr,  
        "th_list" : th_arr,
        "date_list1" : date_arr1,
        "date_list2" : date_arr2,
        "schedule_list" : schedule_arr,
        "msg" : msg,
        'login' : login
    }
    return render(request,'all_list.html', context)


