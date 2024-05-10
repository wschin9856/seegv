from django import template

register = template.Library() # tag library를 만들기 위한 모듈 레벨의 인스턴스 객체


# @register.filter # 데코레이터 사용시 자동 등록 , 함수랑 필터명이 동일함
# def typeof(data1:object,data2:object):
#     if str is type(data1):
#         return True
#     else:
#         return False
