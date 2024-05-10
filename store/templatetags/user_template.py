from django import template

register = template.Library() # tag library를 만들기 위한 모듈 레벨의 인스턴스 객체


@register.filter
def mul(value:object,num:object):

    mul = int(value) * int(num)

    return mul

@register.filter
def minus(value:object,num:object):

    minus = int(value) - int(num)

    return minus
