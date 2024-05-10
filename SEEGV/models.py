from django.db import models
from django.utils import timezone

def id_dir_path(instance,filename):
    return "{}/{}".format(instance.id,filename)
def nickname_dir_path(instance,filename):
    return "user/profile/{}/{}".format(instance.nickname,filename)

# 시퀀스
class PayStep(models.Model): # 결제STEP
    ps_no = models.BigAutoField(primary_key=True)
    ps_name = models.CharField(max_length=50)

class Card(models.Model): # 카드종류
    card_no = models.BigAutoField(primary_key=True)
    Card_name = models.CharField(max_length=50) # 카드종류명

class CancelReason(models.Model): # 예매내역 취소사유 유형
    cr_no = models.BigAutoField(primary_key=True)
    cr_name = models.CharField(max_length=50) # 취소사유 유형명

class VipGrade_option(models.Model):
    vipgo_no = models.BigAutoField(primary_key=True,verbose_name="등급번호seq")
    vipgo_name = models.CharField(max_length=20,verbose_name="고객 등급 이름")
    vipgo_score = models.IntegerField()


class Ocb_option1(models.Model):
    onco_no = models.BigAutoField(primary_key=True,verbose_name="쿠폰 분류 seq")
    onco_name = models.CharField(max_length=30,verbose_name="쿠폰분류")

class Vipstamp_option1(models.Model):
    vso_no = models.BigAutoField(primary_key=True,verbose_name="번호seq")
    vs_name = models.CharField(max_length=20,verbose_name="분류1")


class Vbo_option(models.Model):
    vboo_no = models.BigAutoField(primary_key=True,verbose_name="번호seq")
    vboo_name = models.CharField(max_length=20,verbose_name="분류1")

class Event_Method(models.Model):
    eM_no = models.BigAutoField(primary_key=True,verbose_name="이벤트 응모 방법 번호")
    eM_name = models.CharField(max_length=20,verbose_name="이벤트 응모방법 이름")

class Event_Kind(models.Model):
    eK_no = models.BigAutoField(primary_key=True,verbose_name="이벤트 유형 seq")
    eK_name = models.CharField(max_length=30,verbose_name="이벤트 유형 이름")

class CsOption(models.Model):
    cso_no = models.BigAutoField(primary_key=True,verbose_name="번호seq")
    cso_name = models.CharField(max_length=20,verbose_name="분류1")

class Ca(models.Model):
    ca_no = models.BigAutoField(primary_key=True,verbose_name="상담톡번호")
    ca_content = models.CharField(max_length=500,verbose_name="물어볼 내용")
    ca_file = models.FileField(upload_to="",null=True)


class VipClient(models.Model):
    vigc_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    vipg_title = models.CharField(max_length=150,verbose_name="제목")
    vipg_content = models.CharField(max_length=500,verbose_name="내용")


class Country(models.Model): # 국가 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30,null=False)

class Genre(models.Model): # 장르 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10,null=False)

class ViewableAge(models.Model): # 이용관람가 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20,null=False)

class MovieType(models.Model): # 영화 타입 seq (상업, 예술, 독립, 컨텐츠)
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20,null=True)

class Charm(models.Model): # 매력점수 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)

class Emotion(models.Model): # 감정점수 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)

class GoldenEgg(models.Model): # 실관람평지수 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10)
    image = models.FileField(upload_to=id_dir_path, blank=True, null=True)

class PreEgg(models.Model): # 사전관람지수 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10)


class Report(models.Model): # 리뷰신고 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20)


class Region(models.Model): # 지역 seq (서울 경기 등등)
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)

class TheaterType(models.Model): # 극장 타입 seq (CGV, 아트하우스 등)
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)

class Screen(models.Model): # 스크린 타입 seq (4DX, 2D, ScreenX 등)
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False)
    cate = models.CharField(max_length=20, null=False) # 일반관, 프레스티지, 테크놀로지, 컨셉트

class Dayofweek(models.Model): # 주중/주말/공휴일 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False)


class SeatType(models.Model): # 좌석 타입 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10,null=False) # light, 일반, 장애인, sweetbox 등

class Timezone(models.Model): # 시간대 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10,null=False) # 조조, 브런치, 일반, 심야
    
class PersonType(models.Model): # 인원 타입 seq
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=10, null=False) # 일반, 청소년, 노인, 장애인, 국가유공자 등

# memberType(사용자구분)
class MemberType(models.Model) :
    memberType_no = models.BigAutoField(primary_key=True)
    member_type = models.CharField(max_length=100)

# mainCategory(메인 카테고리)
class MainCategory(models.Model) :
    mainC_no = models.BigAutoField(primary_key=True)
    mainC_category = models.CharField(max_length=100)




# nonmembers(비회원 예매)
class Nonmembers(models.Model) :
    nonmember_no = models.BigAutoField(primary_key=True)
    nonmember_pw = models.CharField(max_length=100)
    nonmember_years = models.IntegerField()
    nonmember_month = models.IntegerField()
    nonmember_day = models.IntegerField()
    nonmember_tel1 = models.IntegerField()
    nonmember_tel2 = models.IntegerField()
    nonmember_tel3 = models.IntegerField()
    nonmember_gender = models.IntegerField()

# terms(약관)
class Terms(models.Model) :
    terms_no = models.BigAutoField(primary_key=True)
    terms_title = models.CharField(max_length=100)
    terms_item = models.CharField(max_length=100)
    terms_purpose = models.TextField()
    terms_period = models.CharField(max_length=100)
    terms_required = models.IntegerField()


# pointCategory(포인트 종류)
class PointCategory(models.Model) :
    pc_no = models.BigAutoField(primary_key=True)
    pointCategory = models.CharField(max_length=100)

# storeCategory(스토어 상품 카테고리)
class StoreCategory(models.Model) :
    sc_no = models.BigAutoField(primary_key=True)
    sc_category = models.CharField(max_length=100)

# CouponCategory(쿠폰 카테고리)
class CouponCategory(models.Model) :
    cc_no = models.BigAutoField(primary_key=True)
    coupon_category = models.CharField(max_length=100)

# movieCoupon(영화관람권)
class MovieCoupon(models.Model) :
    mc_no = models.BigAutoField(primary_key=True)
    mc_name = models.CharField(max_length=100)
    mc_week = models.DateField()

# giftcardPrice(기프트카드 설정 금액)
class GiftcardPrice(models.Model) :
    giftcardPrice_no = models.BigAutoField(primary_key=True)
    giftcardPrice = models.IntegerField()


########################## 주요 참조테이블 #######################
# members(회원정보)
class MemberInfo(models.Model) :
    memberInfo_no = models.BigAutoField(primary_key=True)
    memberInfo = models.CharField(max_length=100)


class Members(models.Model) :
    member_no = models.BigAutoField(primary_key=True)
    member_name = models.CharField(max_length=100)
    member_id = models.CharField(max_length=100)
    member_pw = models.CharField(max_length=100)    
    member_years = models.CharField(max_length=100)
    member_month = models.CharField(max_length=100)
    member_day = models.CharField(max_length=100)
    member_tel1 = models.CharField(max_length=100)
    member_tel2 = models.CharField(max_length=100)
    member_tel3 = models.CharField(max_length=100)
    member_mailId = models.CharField(max_length=100)
    member_mailAddress = models.CharField(max_length=100)
    member_gender = models.IntegerField()
    memberType_no = models.ForeignKey(MemberType, on_delete=models.CASCADE)
    memberInfo_no = models.ForeignKey(MemberInfo, on_delete=models.CASCADE)
    member_vipPoint = models.IntegerField(default=0)
    member_class  = models.ForeignKey(VipGrade_option, on_delete=models.CASCADE)

class Movie(models.Model): # 영화
    no = models.BigAutoField(primary_key=True)
    krname = models.CharField(max_length=100,null=False) # 한국이름
    ername = models.CharField(max_length=100,null=False) # 영문이름
    story = models.CharField(max_length=1000,null=True) # 줄거리
    runtime = models.CharField(max_length=5,null=False) # 상영시간
    image = models.FileField(upload_to=id_dir_path, blank=True, null=True) # 포스터
    opendate = models.DateField() # 개봉일자
    site = models.CharField(max_length=100,null=True) # 영화사이트
    ViewableAge_no = models.ForeignKey(ViewableAge,on_delete=models.CASCADE)
    MovieType_no = models.ForeignKey(MovieType,on_delete=models.CASCADE)
    status = models.CharField(max_length=10,null=True)

# Point(사용 포인트) 
class PointUse(models.Model) :
    pointUse_no = models.BigAutoField(primary_key=True)
    pc_no = models.ForeignKey(PointCategory, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    savepoint = models.IntegerField(default=0)
    usepoint = models.IntegerField(default=0)
    pointUse_place = models.CharField(max_length=100)
    pointUse_date = models.DateField()

class Theater(models.Model): # 극장
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20,null=False) # 이름
    Region_no = models.ForeignKey(Region, on_delete=models.CASCADE) # 지역
    address1 = models.CharField(max_length=100, null=False) # 지번주소
    address2 = models.CharField(max_length=100, null=False) # 도로명주소
    tel = models.CharField(max_length=20, null=False) # 전화번호
    traffic = models.CharField(max_length=1000, null=False) # 교통안내
    parking = models.CharField(max_length=1000, null=False) # 주차안내
    TheaterType_no = models.ForeignKey(TheaterType, on_delete=models.CASCADE) # 극장타입
    tothalls = models.CharField(max_length=10, null=True) # 총 상영관 수
    totseats = models.CharField(max_length=10, null=True) # 총 좌석 수
    info = models.CharField(max_length=200, null=True) # 정보



class Hall(models.Model): # 상영관
    no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=20,null=False) # 이름
    floor = models.CharField(max_length=10, null=True) # 층
    totseat = models.CharField(max_length=10, null=False) # 상영관 좌석 수
    Screen_no = models.ForeignKey(Screen,on_delete=models.CASCADE) # 스크린 타입 seq
    Theater_no = models.ForeignKey(Theater, on_delete=models.CASCADE) # 극장



class HallSchedule(models.Model): # 상영관 스케줄
    no = models.BigAutoField(primary_key=True)
    ondate = models.DateField() # 상영일자
    stime = models.CharField(max_length=20) # 시작시간
    etime = models.CharField(max_length=20) # 종료시간
    Movie_no = models.ForeignKey(Movie, on_delete=models.CASCADE) # 영화
    Hall_no = models.ForeignKey(Hall, on_delete=models.CASCADE) # 상영관


class HallPrice(models.Model): # 관람 가격
    no = models.BigAutoField(primary_key=True)
    # Hall_no = models.ForeignKey(Hall,on_delete=models.CASCADE) # 상영관
    # SeatType_no = models.ForeignKey(SeatType, on_delete=models.CASCADE) # 좌석 타입 seq
    # PersonType_no = models.ForeignKey(PersonType, on_delete=models.CASCADE) # 인원 타입 seq
    # Timezone_no = models.ForeignKey(Timezone, on_delete=models.CASCADE) # 시간대 seq
    Dayofweek_no = models.ForeignKey(Dayofweek, on_delete=models.CASCADE) # 주중/주말/공휴일
    Screen_no = models.ForeignKey(Screen,on_delete=models.CASCADE)
    price = models.CharField(max_length=10, null=False) # 가격


class HallSeat(models.Model): # 상영관 좌석
    no = models.BigAutoField(primary_key=True)
    srow = models.CharField(max_length=2, null=False) # 가로열 1~10?
    scol = models.CharField(max_length=2, null=False) # 세로열 A~J?
    Hall_no = models.ForeignKey(Hall, on_delete=models.CASCADE)
    SeatType_no = models.ForeignKey(SeatType, on_delete=models.CASCADE)



class VipPointSave(models.Model):
    vipps_no = models.BigAutoField(primary_key=True,verbose_name="vip 포인트 적립")
    pc_no = models.ForeignKey(PointCategory, verbose_name="포인트 종류 seq", on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members,verbose_name="사용자 회원정보 seq",on_delete=models.CASCADE)
    vipps_point = models.IntegerField(verbose_name="적립 포인트")
    vipps_date = models.DateField(verbose_name="포인트 적립일")


class Ticket(models.Model): # 예매내역, 2024.4.29 수정 : 컬럼명 및 속성 변경, 외래키 설정, 5.1재수정
    ticket_no = models.BigAutoField(primary_key=True)
    HallSchedule_no = models.ForeignKey(HallSchedule, on_delete=models.CASCADE)
    ticket_date = models.DateTimeField(auto_now_add=True) # 예매일시    
    member_no = models.IntegerField() # 회원 또는 비회원 시퀀스번호(비회원은 pointUse_no, vipps_no null값으로 셋팅)
    ticket_totalcnt = models.IntegerField() # 총관람인원
    ticket_totalprice = models.IntegerField()  # 총구매금액
    ticket_gender = models.IntegerField() # 1: 남자 2 : 여자(통계용)
    ticket_age = models.IntegerField() # 예매자 연령대
    ticket_cancelflag = models.IntegerField()   # 0: 예약유지, 1:에약취소
    pointUse_no = models.ForeignKey(PointUse, on_delete=models.CASCADE, null=True)  # 적립 포인트 seq
    vipps_no = models.ForeignKey(VipPointSave, on_delete=models.CASCADE,null=True)  # VIPPointSave(VIP 포인트 적립) seq

# profile(프로필)
class Profile(models.Model) :
    profile_no = models.BigAutoField(primary_key=True)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, null=True)
    filename = models.CharField(max_length=100, null=True)
    profileimage = models.FileField(upload_to=nickname_dir_path, blank=True, null=True)


############################# 예매(진우석) 관련 테이블 9개 (시작) ##################################### 


class TicketSeat(models.Model): # 예매내역별 좌석정보
    ts_no = models.BigAutoField(primary_key=True)
    ticket_no = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    HallSeat_no = models.ForeignKey(HallSeat, on_delete=models.CASCADE) # 상영관별 좌석세부 정보 seq


class StepDetail(models.Model): # 결제STEP별 세부분류
    sd_no = models.BigAutoField(primary_key=True)
    ps_no = models.ForeignKey(PayStep, on_delete=models.CASCADE)
    sd_name = models.CharField(max_length=50) # 결제STEP별 세부분류 명칭

class TicketCoupon(models.Model): # 결제내역별 세부 사용내역
    tc_no = models.BigAutoField(primary_key=True)
    ticket_no = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    sd_no = models.ForeignKey(StepDetail, on_delete=models.CASCADE) # 결제STEP별 세부분류 seq
    coupon_useno = models.IntegerField() # 기프트콘(giftcarduse_no)/관람권(mcu_no)/쿠폰(ci_no)/포인트(usepoint_no) 사용 seq
    tc_date = models.DateTimeField(auto_now_add=True) # 사용일시
    tc_price = models.IntegerField() # 사용된 할인금액


class PayCard(models.Model): # 신용카드 결제내역, 신용카드 결제 및 할인쿠폰의 경우에만 적용됨	
    pc_no = models.BigAutoField(primary_key=True)
    ticket_no = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    card_no = models.ForeignKey(Card, on_delete=models.CASCADE)	# 카드종류 seq



class TicketCancel(models.Model): # 예매내역 취소
    tcc_no = models.BigAutoField(primary_key=True)
    ticket_no = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    cr_no	= models.ForeignKey(CancelReason, on_delete=models.CASCADE) # 예매 취소사유 유형 번호

############################# 예매(진우석) 관련 테이블(끝) ##################################### 


############################# 혜택(김현교) 관련 테이블(시작) ##################################### 
    


class VipGrade_manage(models.Model):
    vigm_no = models.BigAutoField(primary_key=True,verbose_name="번호 seq")
    member_no = models.ForeignKey(Members,verbose_name="회원 정보",on_delete=models.CASCADE)
    vipgo_no = models.ForeignKey(VipGrade_option,on_delete=models.CASCADE,verbose_name="회원 등급 받기")
    vigm_sd = models.DateField(verbose_name="승급된 년/월",null=True)
    vigm_ed = models.DateField(verbose_name="종료된 년/월",null=True)




class Ocb_option2(models.Model):
    onco2_no = models.BigAutoField(primary_key=True,verbose_name="쿠폰 분류 seq2")
    onco_no = models.ForeignKey(Ocb_option1,on_delete=models.CASCADE,verbose_name="쿠폰북 1 seq")
    onco2_name = models.CharField(max_length=20,verbose_name="쿠폰분류")

class Vmobiec_option(models.Model):
    vmco_no = models.BigAutoField(primary_key=True,verbose_name="번호seq")
    vipgo_no = models.ForeignKey(VipGrade_option,on_delete=models.CASCADE,verbose_name="등급")
    onco2_no = models.ForeignKey(Ocb_option2,on_delete=models.CASCADE,verbose_name="쿠폰seq")
    vmco_score = models.IntegerField(verbose_name="쿠폰당 갯수")
    vmco_op = models.CharField(max_length=20,verbose_name="분류 이름",null=True)



class Vipstamp_option2(models.Model):
    vso2_no = models.BigAutoField(primary_key=True,verbose_name="번호 seq")
    vso_no = models.ForeignKey(Vipstamp_option1,on_delete=models.CASCADE,verbose_name="분류1 번호")
    vos2_name = models.CharField(max_length=20,verbose_name="분류2 이름")

class Vipstamp(models.Model):
    vips_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    vso2_no = models.ForeignKey(Vipstamp_option2,on_delete=models.CASCADE,verbose_name="번호 seq")
    vips_number = models.IntegerField(verbose_name="적립 숫자")
    vipgo_no = models.ForeignKey(VipGrade_option,on_delete=models.CASCADE,verbose_name="등급 받기")



class Vbo(models.Model):
    vbo_no = models.BigAutoField(primary_key=True,verbose_name="번호 seq")
    vboo_no = models.ForeignKey(Vbo_option,on_delete=models.CASCADE,verbose_name="번호seq")
    vbo_price = models.CharField(max_length=30,verbose_name="상품",null=True)
    vipgo_no = models.ForeignKey(VipGrade_option,on_delete=models.CASCADE,verbose_name="등급")

class VIPcouponmemberManager(models.Model):
    vipcm_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    member_no = models.ForeignKey(Members,on_delete=models.CASCADE,verbose_name="회원 번호 받아오기")
    onco2_no = models.ForeignKey(Ocb_option2,on_delete=models.CASCADE,verbose_name="쿠폰 seq")
    vipcm_number = models.IntegerField(verbose_name="수량")
    vipcm_start = models.DateField(verbose_name="이벤트 시작일")
    vipcm_end = models.DateField(verbose_name="이벤트 종료일")
class VIPbenifitmemberManager(models.Model):
    vipbM_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    member_no = models.ForeignKey(Members,on_delete=models.CASCADE,verbose_name="회원 번호 받아오기")
    vso2_no = models.ForeignKey(Vipstamp_option2,on_delete=models.CASCADE,verbose_name="쿠폰 seq")
    vbmm_number = models.IntegerField(verbose_name="수량")
class VIPbenifitotherManager(models.Model):
    vipbo_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    member_no = models.ForeignKey(Members,on_delete=models.CASCADE,verbose_name="회원 번호 받아오기")
    vboo_no = models.ForeignKey(Vbo_option,on_delete=models.CASCADE,verbose_name="쿠폰 seq")
    vipbo_number = models.CharField(max_length=40,verbose_name="수량",null=True)
    vipbo_start = models.DateField(verbose_name="이벤트 시작일")
    vipbo_end = models.DateField(verbose_name="이벤트 종료일")
####################### event 시작 ##################################

class Event(models.Model):
    event_no = models.BigAutoField(primary_key=True,verbose_name="이벤트 번호")
    event_name = models.CharField(max_length=30,verbose_name="이벤트 이름")
    event_winnum = models.IntegerField(verbose_name="이벤트 당첨인원",null=True)
    event_start = models.DateField(verbose_name="이벤트 시작일")
    event_end = models.DateField(verbose_name="이벤트 종료일")
    eM_no= models.ForeignKey(Event_Method,on_delete=models.CASCADE)
    event_Announce = models.DateField(verbose_name="이벤트 당첨자 발표일",null=True)
    eb_type = models.CharField(max_length=30,verbose_name="이벤트 타입",null=True)
    ebc_name = models.CharField(max_length=30,verbose_name="이벤트 게시물 제목",null=True)
    ebc_content = models.FileField(upload_to="eventCimg", blank=True, null=True)
    event_faceimg = models.FileField(upload_to="faceimg", blank=True, null=True)
    vipgo_no = models.ForeignKey(VipGrade_option, verbose_name="가능한 회원 최소 등급 받기", on_delete=models.CASCADE,null=True)



class Event_Kind2(models.Model):
    ek_no2 = models.BigAutoField(primary_key=True,verbose_name="이벤트 유형 seq2")
    ek_no = models.ForeignKey(Event_Kind,verbose_name="이벤트 유형 seq", on_delete=models.CASCADE)
    ek_name2 = models.CharField(max_length=30,verbose_name="이벤트 유형 이름")

class EventCategory(models.Model):
    eventcate_no = models.BigAutoField(primary_key=True,verbose_name="유형 관리 번호")
    event_no = models.ForeignKey(Event,verbose_name="이벤트 번호",on_delete=models.CASCADE)
    ek_no2 = models.ForeignKey(Event_Kind2,verbose_name="이벤트 유형 seq",on_delete=models.CASCADE)

class Apply_Theater(models.Model):
    aT_no = models.BigAutoField(primary_key=True,verbose_name="이벤트 적용하는 극장여부 시퀀스")
    event_no = models.ForeignKey(Event,on_delete=models.CASCADE,verbose_name="",null=True)
    Theater_no = models.ForeignKey(Theater,verbose_name="이벤트 진행 극장",on_delete=models.CASCADE,null=True)

class ApplyMember(models.Model):
    aM_NO = models.BigAutoField(primary_key=True,verbose_name="이벤트 응모자 번호")
    event_no = models.ForeignKey(Event, verbose_name="이벤트 번호 받기", on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members,verbose_name="등급자 번호 받기",on_delete=models.CASCADE)
    aM_date = models.DateField(verbose_name="응모 일시")
    aM_win = models.BooleanField(verbose_name="당첨 여부",null=True)
class ApplyUrl(models.Model):
    no = models.BigAutoField(primary_key=True,verbose_name="시퀀스")
    event_no = models.ForeignKey(Event, verbose_name="이벤트 번호 받기", on_delete=models.CASCADE)
    urlname = models.CharField(max_length=200,verbose_name="url")

####################### serviceCenter 김현교 시작 ##################################





class FQ(models.Model):
    fq_no = models.BigAutoField(primary_key=True,verbose_name="fq번호")
    fq_content = models.CharField(max_length=2000,verbose_name="컨탠츠 내용")
    fq_title = models.CharField(max_length=200,verbose_name="컨탠츠 제목")
    fq_regdate = models.DateField(verbose_name="컨텐츠 등록일",null=True)
    fq_hit = models.IntegerField(verbose_name="컨탠츠 조회수",default=0)
    fqo_name = models.CharField(max_length=30,verbose_name="분류 이름")



class CsOption2(models.Model):
    cso2_no = models.BigAutoField(primary_key=True,verbose_name="번호seq2")
    cso2_name = models.CharField(max_length=20,verbose_name="분류2")
    cso_no = models.ForeignKey(CsOption,on_delete=models.CASCADE)

class CsOption3(models.Model):
    cso3_no = models.BigAutoField(primary_key=True,verbose_name="번호seq3")
    cso3_name = models.CharField(max_length=20,verbose_name="분류3")
    cso2_no = models.ForeignKey(CsOption2,on_delete=models.CASCADE)
class CsOption4(models.Model):
    cso4_no = models.BigAutoField(primary_key=True,verbose_name="번호seq3")
    cso4_name = models.CharField(max_length=30,verbose_name="분류3")
    cso3_no = models.ForeignKey(CsOption3,on_delete=models.CASCADE)


class Cs(models.Model):
    cs_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    cs_url = models.CharField(max_length=100,verbose_name="url 저장 컨탠츠",null=True)
    cs_content = models.CharField(max_length=300,verbose_name="컨탠츠 내용",null=True)
    cso_no = models.ForeignKey(CsOption,on_delete=models.CASCADE)
    cso2_no = models.ForeignKey(CsOption2,on_delete=models.CASCADE)
    cso3_no = models.ForeignKey(CsOption3,on_delete=models.CASCADE)




class Ea(models.Model):
    ea_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    ea_op = models.CharField(max_length=30,verbose_name="유형 분류")
    ea_title= models.CharField(max_length=30,verbose_name="제목")
    ea_content =models.CharField(max_length=2000,verbose_name="내용")
    ea_file = models.FileField(upload_to="support/", blank=True, null=True)
    theater_no = models.ForeignKey(Theater, null=True,blank=True,verbose_name="지역 분류 seq", on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, verbose_name="회원 정보 seq",on_delete=models.CASCADE)
    ea_regdate = models.DateField()
    ea_state = models.CharField(max_length=30,null=True)
    ea_satisfy = models.CharField(max_length=30,null=True)
    ea_mcontent = models.CharField(max_length=2000,null=True)


class GroupAsk(models.Model):
    ga_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    ga_date = models.DateField(verbose_name="관람 희망일")
    ga_time = models.IntegerField(verbose_name="관람 시간")
    ga_person = models.IntegerField(verbose_name="관람 희망 인원")
    ga_content = models.CharField(max_length=100,verbose_name="내용 데이터")
    ga_membername = models.CharField(max_length=15,verbose_name="문의자명")
    ga_tel = models.IntegerField(verbose_name="연락처")
    ga_email = models.CharField(max_length=30,verbose_name="이메일")
    theater_no = models.ForeignKey(Theater,on_delete=models.CASCADE)



class News(models.Model):
    nw_no = models.BigAutoField(primary_key=True,verbose_name="번호")
    nw_title = models.CharField(max_length=300,verbose_name="컨텐츠 제목")
    nw_hit = models.IntegerField(verbose_name = "컨텐츠 조회수")
    nw_content = models.CharField(max_length=2000,verbose_name="컨텐츠 내용")
    nw_date = models.DateField(verbose_name="컨텐츠 등록일")
    nwo_name = models.CharField(max_length=30,verbose_name="컨텐츠 분류 이름")

############################### 김현교 끝 ##################################333
      


############################# 영화, 극장(장민국) 관련 테이블(시작) ##################################### 



class MovieReview(models.Model): # 영화리뷰
    no = models.BigAutoField(primary_key=True)
    GoldenEgg_no = models.ForeignKey(GoldenEgg,on_delete=models.CASCADE)
    uploadtext = models.CharField(max_length=1000,null=False)
    recommand = models.IntegerField()
    uploaddate = models.DateField()
    profile_no = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ticket_no = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    Charm_1 = models.IntegerField(null=True)
    Charm_2 = models.IntegerField(null=True)
    Charm_3 = models.IntegerField(null=True)
    Charm_4 = models.IntegerField(null=True)
    Charm_5 = models.IntegerField(null=True)
    Emotion_1 = models.IntegerField(null=True)
    Emotion_2 = models.IntegerField(null=True)
    Emotion_3 = models.IntegerField(null=True)
    Emotion_4 = models.IntegerField(null=True)
    Emotion_5 = models.IntegerField(null=True)
class RecommandCount(models.Model):
    no = models.BigAutoField(primary_key=True)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)
    MovieReview_no = models.ForeignKey(MovieReview, on_delete=models.CASCADE)

class ReportCount(models.Model): # 리뷰신고 카운트
    no = models.BigAutoField(primary_key=True)
    MovieReview_no = models.ForeignKey(MovieReview,on_delete=models.CASCADE)
    Report_no = models.ForeignKey(Report,on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)




    

class MovieCountryMap(models.Model): # 영화-국가 매핑 테이블
    Movie_no = models.ForeignKey(Movie,on_delete=models.CASCADE)
    Country_no = models.ForeignKey(Country,on_delete=models.CASCADE)

class MovieGenreMap(models.Model): # 영화-장르 매핑 테이블
    Movie_no = models.ForeignKey(Movie,on_delete=models.CASCADE)
    Genre_no = models.ForeignKey(Genre,on_delete=models.CASCADE)

class Stillcut(models.Model): # 영화-스틸컷
    no = models.BigAutoField(primary_key=True)
    Movie_no = models.ForeignKey(Movie,on_delete=models.CASCADE)
    image = models.FileField(upload_to=id_dir_path, blank=True,null=True)

class Person(models.Model): # 인물
    no = models.BigAutoField(primary_key=True)
    krname = models.CharField(max_length=20, null=False) # 한국 이름
    enname = models.CharField(max_length=20, null=True) # 영문 이름
    intro = models.CharField(max_length=1000, null=True) # 소개
    image = models.FileField(max_length=1000, null=True) # 이미지
    birth = models.CharField(max_length=20, null=True) # 출생
    Country_no = models.ForeignKey(Country,on_delete=models.CASCADE) # 국가
    award = models.CharField(max_length=100, null=True) # 수상
    site = models.CharField(max_length=100, null=True) # 인물사이트
    body = models.CharField(max_length=100, null=True) # 신체
    academic = models.CharField(max_length=100, null=True) # 학력
    family = models.CharField(max_length=100, null=True) # 가족
    hobby = models.CharField(max_length=100, null=True) # 취미

class MoviePersonMap(models.Model): # 영화-인물 매핑 테이블
    Movie_no = models.ForeignKey(Movie,on_delete=models.CASCADE)
    Person_no = models.ForeignKey(Person,on_delete=models.CASCADE)
    role = models.CharField(max_length=10, null=False) # 역할






class MoviePreview(models.Model): # 영화 사전평가
    no = models.BigAutoField(primary_key=True)
    Movie_no = models.ForeignKey(Movie,on_delete=models.CASCADE) # 영화
    PreEgg_no = models.ForeignKey(PreEgg,on_delete=models.CASCADE) # 사전평가 seq
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)


####################### 장민국 테이블 끝 ##################################

############################# 메인, 멤버(원유림) 관련 테이블(시작) ##################################### 

# subCategory(서브 카테고리)
class SubCategory(models.Model) :
    subC_no = models.BigAutoField(primary_key=True)
    mainC_no = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    subC_category = models.CharField(max_length=100)

#### members

# memberJoinDate(사용자 가입 일)
class MemberJoinDate(models.Model) :
    mjd_no = models.BigAutoField(primary_key=True)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)
    mjd_date = models.DateField()
    mjd_dormantdate = models.DateField(blank=True, null=True)
    mjd_leave = models.DateField(blank=True, null=True)




# bookmark(자주가는CGV서비스)
class Bookmark(models.Model) :
    bookmark_no = models.BigAutoField(primary_key=True)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)
    th_no = models.ForeignKey(Theater, on_delete=models.CASCADE)




#### terms


# agreement(사용자 동의)
class Agreement(models.Model) :
    agreement_no = models.BigAutoField(primary_key=True)
    terms_no = models.ForeignKey(Terms, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    useragreement = models.IntegerField()

# termsdata1(수집항목1)
class Termsdata1(models.Model) :
    termsdata1_no = models.BigAutoField(primary_key=True)
    terms_no = models.ForeignKey(Terms, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    td_genre1 = models.CharField(max_length=100, null=True)
    td_genre2 = models.CharField(max_length=100, null=True)

# termsdata2(수집항목2)
class Termsdata2(models.Model) :
    termsdata2_no = models.BigAutoField(primary_key=True)
    terms_no = models.ForeignKey(Terms, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    td_weekday = models.CharField(max_length=100, null=True)

# termsdata3(수집항목3)
class Termsdata3(models.Model) :
    termsdata3_no = models.BigAutoField(primary_key=True)
    terms_no = models.ForeignKey(Terms, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    td_time = models.CharField(max_length=100, null=True)

# termsdata4(수집항목4)
class Termsdata4(models.Model) :
    termsdata4_no = models.BigAutoField(primary_key=True)
    terms_no = models.ForeignKey(Terms, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    td_anniversary = models.DateField(null=True)
    td_anniversaryName = models.CharField(max_length=100, null=True)    

# termsdata5(수집항목5)
class Termsdata5(models.Model) :
    termsdata5_no = models.BigAutoField(primary_key=True)
    terms_no = models.ForeignKey(Terms, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    td_zipcode = models.IntegerField(null=True)
    td_address = models.CharField(max_length=100, null=True)    
    td_addressDetail = models.CharField(max_length=100, null=True)    


#### point


# point(현재 포인트)
class Point(models.Model) :
    point_no = models.BigAutoField(primary_key=True)
    pc_no = models.ForeignKey(PointCategory, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)    
    point = models.IntegerField()




# PointRule(포인트 지급기준)
class PointRule(models.Model) :
    PointRule_no = models.BigAutoField(primary_key=True)
    pc_no = models.ForeignKey(PointCategory, on_delete=models.CASCADE)
    pointRule_type = models.IntegerField()
    pointRule = models.IntegerField()
    pointRule_dsc = models.CharField(max_length=100, null=True)

### coupon
# couponCategory(쿠폰 카테고리)

class StoreProductState(models.Model) :
    sps_no = models.BigAutoField(primary_key=True)
    sps = models.CharField(max_length=100) 


# storeProduct(스토어 상품)
class StoreProduct(models.Model) :
    sp_no = models.BigAutoField(primary_key=True)
    sc_no = models.ForeignKey(StoreCategory, on_delete=models.CASCADE)
    sp_name = models.CharField(max_length=100)
    sp_image = models.FileField(upload_to="store/", blank=True, null=True)
    sp_items = models.CharField(max_length=100)
    sp_period = models.CharField(max_length=100)
    sp_periodNumber = models.IntegerField(null=True)
    sp_origin = models.CharField(max_length=100,null=True)
    sp_txt = models.TextField(null=True)
    sp_price = models.IntegerField(null=True)
    sp_discount = models.IntegerField(null=True)
    sps_no = models.ForeignKey(StoreProductState, on_delete=models.CASCADE)

#  packageProduct(패키지상품 구성)
class PackageProduct(models.Model) :
    pp_no = models.BigAutoField(primary_key=True)
    sp_no = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    pp_name = models.CharField(max_length=100)
    pp_price = models.IntegerField()
    pp_count = models.IntegerField()
    pp_periodNumber  = models.IntegerField()
    pp_origin  = models.CharField(max_length=100,null=True)



# movieCouponTheaters(영화관람권 관람 가능 극장)
class MovieCouponTheaters(models.Model) :
    mct_no = models.BigAutoField(primary_key=True)
    mc_no = models.ForeignKey(MovieCoupon, on_delete=models.CASCADE)
    th_no = models.ForeignKey(Theater, on_delete=models.CASCADE)

# movieCouponTheaterType(영화관람권 관람 가능 극장 종류)
class MovieCouponTheaterType(models.Model) :
    mctt_no = models.BigAutoField(primary_key=True)
    mc_no = models.ForeignKey(MovieCoupon, on_delete=models.CASCADE)
    screen_no = models.ForeignKey(Screen, on_delete=models.CASCADE)

# movieCouponInfo(영화관람권 개별 정보)
class MovieCouponInfo(models.Model) :
    mci_no = models.BigAutoField(primary_key=True)
    mc_no = models.ForeignKey(MovieCoupon, on_delete=models.CASCADE)
    mci_number = models.IntegerField()
    mci_date = models.DateField()
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE, null=True)
    mcu_date = models.DateField(null=True)

# coupon(쿠폰)
class Coupon(models.Model) :
    coupon_no = models.BigAutoField(primary_key=True)
    cc_no = models.ForeignKey(CouponCategory, on_delete=models.CASCADE)
    coupon_name = models.CharField(max_length=100)
    coupon_date = models.DateField()
    coupon_discount = models.IntegerField()    
    coupon_txt = models.CharField(max_length=100)
    coupon_type = models.IntegerField()

# couponTheaters(할인쿠폰 사용 가능 극장)
class CouponTheaters(models.Model) :
    ct_no = models.BigAutoField(primary_key=True)
    coupon_no = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    th_no = models.ForeignKey(Theater, on_delete=models.CASCADE)

# couponTheatersType(할인쿠폰 사용 가능 관 종류)
class CouponTheatersType(models.Model) :
    ctt_no = models.BigAutoField(primary_key=True)
    coupon_no = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    screen_no = models.ForeignKey(Screen, on_delete=models.CASCADE)

# couponInfo(할인쿠폰 개별 정보)
class CouponInfo(models.Model) :
    ci_no = models.BigAutoField(primary_key=True)
    coupon_no = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    ci_number = models.IntegerField()    
    mci_date = models.DateField()
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE, null=True)
    cu_date = models.DateField(null=True)

############################# store(원유림) 관련 테이블(시작) ##################################### 
#### storeProduct


#  storeProductUse(스토어 상품 사용가능 지점)
class StoreProductUse(models.Model) :
    spu_no = models.BigAutoField(primary_key=True)
    sp_no = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    th_no = models.ForeignKey(Theater, on_delete=models.CASCADE)

# addList(장바구니)
class AddList(models.Model) :
    addList_no = models.BigAutoField(primary_key=True)
    sp_no = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    addList_count = models.IntegerField()
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)
    addList_date = models.DateField()
    addList_checkde = models.BooleanField(default=0)



# giftconUser(기프트콘 수취자)
class GiftconUser(models.Model) :
    giftconUser_no = models.BigAutoField(primary_key=True)
    order_number = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    userTel = models.CharField(max_length=100)




# storeOrder(스토어주문)
class StoreOrder(models.Model) :
    order_no = models.BigAutoField(primary_key=True)
    order_number = models.CharField(max_length=100)
    order_date = models.DateField()
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE)
    order_price = models.IntegerField()
    order_discount = models.IntegerField(null=True)
    order_payment = models.IntegerField()
    order_method = models.CharField(max_length=100)
    vipps_no = models.ForeignKey(VipPointSave, on_delete=models.CASCADE,null=True)
    order_state = models.IntegerField()
    pointUse_no = models.ForeignKey(PointUse, on_delete=models.CASCADE,null=True)
    giftconUser_no = models.ForeignKey(GiftconUser, on_delete=models.CASCADE,null=True)
    
# ProductOrder(주문상품정보)
class ProductOrder(models.Model) :
    Productorder_no = models.BigAutoField(primary_key=True)
    order_number = models.CharField(max_length=100)
    sp_no = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    order_count = models.IntegerField()
    order_price = models.IntegerField()
    order_discount = models.IntegerField()
    order_no = models.ForeignKey(StoreOrder, on_delete=models.CASCADE, null=True)










#### giftcon


# giftconState(기프트콘 상태)
class GiftconState(models.Model) :
    gs_no = models.BigAutoField(primary_key=True)
    giftcon_state = models.CharField(max_length=100)

# giftconCategory(기프트콘 카테고리)
class GiftconCategory(models.Model) :
    gc_no = models.BigAutoField(primary_key=True)
    sc_no = models.ForeignKey(StoreCategory, on_delete=models.CASCADE,null=True)
    pp_no = models.ForeignKey(PackageProduct, on_delete=models.CASCADE,null=True)
    gc_category = models.CharField(max_length=100)
    gc_categoryNo = models.CharField(max_length=100)


# giftcon(기프트콘)
class Giftcon(models.Model) :
    giftcon_no = models.BigAutoField(primary_key=True)
    sp_no = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    giftcon_number = models.IntegerField(null=True)
    pp_no = models.ForeignKey(PackageProduct, on_delete=models.CASCADE,null=True)
    user_no = models.ForeignKey(Members, on_delete=models.CASCADE, null=True)
    order_no = models.ForeignKey(StoreOrder, on_delete=models.CASCADE, null=True)
    order_day = models.DateField()
    giftcon_period = models.DateField()
    gs_no = models.ForeignKey(GiftconState, on_delete=models.CASCADE)
    gc_categoryNo = models.CharField(max_length=100,null=True)


# giftcard(기프트카드)
class Giftcard(models.Model) :
    giftcard_no = models.BigAutoField(primary_key=True)
    cc_no = models.ForeignKey(CouponCategory, on_delete=models.CASCADE)
    order_no = models.ForeignKey(StoreOrder, on_delete=models.CASCADE)
    member_no = models.ForeignKey(Members, on_delete=models.CASCADE,null=True)
    giftcard_number = models.IntegerField(null=True)
    giftcard_balance = models.IntegerField()
    giftcard_pw = models.CharField(max_length=100)
    giftcard_price = models.IntegerField()
    giftcard_period = models.DateField()
    gs_no = models.ForeignKey(GiftconState, on_delete=models.CASCADE,null=True)
    




# giftcardUse(기프트카드 사용 내역)
class GiftcardUse(models.Model) :
    giftcarduse_no = models.BigAutoField(primary_key=True)
    giftcard_no = models.ForeignKey(Giftcard, on_delete=models.CASCADE)
    giftcarduse_date = models.DateField(null=True)
    giftcarduse_price = models.IntegerField(null=True)









####################### 원유림 테이블 끝 ##################################


