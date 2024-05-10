from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse,JsonResponse
from SEEGV.models import Movie,ViewableAge,MovieCountryMap,MoviePersonMap,Person,MovieGenreMap,Stillcut,Person,Theater,Region,Hall,HallSchedule,Screen,Members,Bookmark,MoviePreview,MovieReview,Genre,Ticket,RecommandCount,Emotion,Charm,Profile,Country,MovieType
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.exceptions import ObjectDoesNotExist



def index(request:HttpRequest):
    login = request.session.get("login")
    login_type = request.session.get("login_type")

    if login:
        member = Members.objects.get(member_no=login).memberType_no.member_type
    else:
        member = None
    movieList = Movie.objects.filter(status=None)
    
    Age = ViewableAge.objects.all()
    currentdate = timezone.now().date()
    ft = request.GET.get('ft')
    if ft == 'false':
        movieList = Movie.objects.filter(status=None)
    elif ft == 'true':
        movieList = Movie.objects.filter(opendate__lte=currentdate,status=None)
    
    for movie in movieList: 
        days_opening = (movie.opendate - currentdate).days
        movie.d_day = days_opening
    
    context = {
        'ml':movieList,
        'age':Age,
        'currentdate':currentdate,
        'login':login,
        'member':member,
        'login_type':login_type,
    }
    return render(request,'first.html',context)

def detailview(request:HttpRequest):
    no = request.GET.get('no')
    login = request.session.get("login")
    login_id = request.session.get("login_id")
    currentdate = timezone.now().date()
    if login != None:
        member = Members.objects.get(member_id=login_id)
        member_no = Members.objects.get(member_no=login).member_no
        viewer = Ticket.objects.filter(HallSchedule_no__Movie_no=no,vipps_no__member_no=member_no, ticket_date__lt=timezone.now())
        reviews = MovieReview.objects.filter(ticket_no__HallSchedule_no__Movie_no_id=no, profile_no__member_no=member_no)
        
    else:
        member = ""
        member_no = ""
        viewer = ""
        reviews =""
    if viewer != "":
        if viewer.exists():
            viewers = True
        else:
            viewers = False
    else:
        viewers = ""
    
    if reviews != "":
        if reviews.exists():
            reviews = True
        else:
            reviews = False
    recounts = []
    rvs = MovieReview.objects.all()
    for review in rvs:
        review_count = RecommandCount.objects.filter(MovieReview_no=review).count()
        recounts.append(review_count)
    print(recounts)

    movie = Movie.objects.get(no=no)
    person = Person.objects.all()
    mp = MoviePersonMap.objects.filter(Movie_no_id=no)
    mc = MovieCountryMap.objects.filter(Movie_no_id=no)
    mg = MovieGenreMap.objects.filter(Movie_no_id=no)
    
    ms = Stillcut.objects.filter(Movie_no_id=no)
    open = (movie.opendate - currentdate).days
    mpall = MoviePersonMap.objects.all()
    pre = MoviePreview.objects.filter(Movie_no=no)
    pre_good = MoviePreview.objects.filter(PreEgg_no_id=1, Movie_no=no)
    
    if pre.count() != 0:
        preper = int((pre_good.count() / pre.count())*100)
    else:
        preper = 0
    re = MovieReview.objects.all()
    re = MovieReview.objects.filter(ticket_no__HallSchedule_no__Movie_no_id=no)
    re_good = MovieReview.objects.filter(GoldenEgg_no_id=1, ticket_no__HallSchedule_no__Movie_no_id=no)
    if re.count() != 0:
        reper = int((re_good.count() / re.count())*100)
    else:
        reper = 0
    context={
        'movie':movie,
        'mp':mp,
        'mc':mc,
        'person':person,
        'mg':mg,
        'currentdate':currentdate,
        'ms':ms,
        'open':open,
        'mpall':mpall,
        'login':login,
        'member_no':member_no,
        'member_id':member,
        'preper':preper,
        'reper':reper,
        'rv':re,
        'viewer':viewers,
        'reviews':reviews,
        'reccount':recounts,
        'no':no,
    }
    return render(request,'detailview.html',context)

def previewSave(request):
    if request.method == 'POST':
        movie_no = request.POST.get('movie_no')
        member_id = request.POST.get('login_id')
        value = request.POST.get('value')
        try:
            member = Members.objects.get(member_id=member_id)
            member_no = member.member_no
            
        except Members.DoesNotExist:
            return JsonResponse({'error': 'Member does not exist'}, status=400)

        if MoviePreview.objects.filter(Movie_no_id=movie_no, member_no=member):
            movie_preview = MoviePreview.objects.get(Movie_no_id=movie_no, member_no=member)
            movie_preview.PreEgg_no_id = int(value)
            movie_preview.save()
        else:
            MoviePreview.objects.create(Movie_no_id=movie_no, member_no=member, PreEgg_no_id=value)
            
        return JsonResponse({'message': 'Preview saved successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def arthouse(request:HttpRequest):
    login = request.session.get("login")
    artList = Movie.objects.filter(MovieType_no_id=2)
    currentdate = timezone.now().date()
    for movies in artList:
        days_opening = (movies.opendate - currentdate).days
        movies.d_day = days_opening

    context={
        'al':artList,
        'currentdate':currentdate,
        'login':login,
    }
    return render(request, 'arthouse.html',context)
    
def person(request: HttpRequest):
    login = request.session.get("login")
    no = request.GET.get('no')
    person = Person.objects.get(no=no)
    
    movie_person_maps = MoviePersonMap.objects.filter(Person_no_id=no)
    movies = Movie.objects.filter(pk__in=[movie_person_map.Movie_no_id for movie_person_map in movie_person_maps])
    
    context = {
        'p': person,
        'm': movies,
        'login':login,
    }

    return render(request, 'person.html', context)


def theater(request: HttpRequest):
    login = request.session.get("login")

    theaterList = Theater.objects.all()
    regionList = Region.objects.all()
    no = request.GET.get('no')
    mg = MovieGenreMap.objects.all()
    currentdate = timezone.now().date()
    rundate = request.GET.get('ondate')
    login_id = request.session.get("login_id")
    bookmark = None
    date_list = [currentdate + timedelta(days=i) for i in range(7)]
    
    if login_id:
        try:
            member = Members.objects.get(member_id=login_id)
            bookmark = Bookmark.objects.filter(member_no=member).values('th_no__name','th_no')
        except Members.DoesNotExist:
            pass
    
    if rundate:
        hs = HallSchedule.objects.filter(Hall_no__Theater_no_id=no, ondate=rundate)
    else:
        hs = HallSchedule.objects.filter(Hall_no__Theater_no_id=1, ondate=currentdate)
    
    if no:
        th = Theater.objects.get(no=no)
        hallList = Hall.objects.filter(Theater_no_id=no)
    else:
        no = '1'
        th = Theater.objects.get(no=no)
        hallList = Hall.objects.filter(Theater_no_id=no)
        
    context = {
        'tl': theaterList,
        'rl': regionList,
        'hl': hallList,
        'hs': hs,
        'th': th,
        'mg': mg,
        'currentdate': currentdate,
        'no': no,
        'bm': bookmark,
        'login' : login,
        'datelist':date_list,
    }
    return render(request, 'theater.html', context)



def get_bookmark(request):
    login_id = request.session.get("login_id")
    if login_id:
        try:
            member = Members.objects.get(member_id=login_id)
            bookmark = Bookmark.objects.filter(member_no=member).values('th_no__name','th_no')
            bm_list = list(bookmark)
            return JsonResponse({'bm': bm_list})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Member does not exist'})
    else:
        return JsonResponse({'error': 'Login ID is not provided'})
    
def get_theaters(request):
    if request.method == 'GET' and 'region_id' in request.GET:
        region_id = request.GET.get('region_id')
        theaters = Theater.objects.filter(Region_no_id=region_id).values('no', 'name') 
        theaters_list = list(theaters)
        return JsonResponse({'theaters': theaters_list})
    else:
        return JsonResponse({'error': 'Invalid request'})
    
def premovie(request:HttpRequest):
    login = request.session.get("login")
    ml = Movie.objects.all()
    currentdate = timezone.now().date()
    e = 0
    for m in ml:
        days_opening = (m.opendate - currentdate).days
        m.d_day = days_opening
    context = {
        'ml':ml,
        'currentdate':currentdate,
        'e':e,
        'login':login,
    }
    return render(request, 'premovie.html',context)

def special(request:HttpRequest):
    login = request.session.get("login")
    sc = Screen.objects.all()
    context= {
        'sc':sc,
        'login':login,
    }
    return render(request, 'special.html',context)

def specialcate(request:HttpRequest):
    login = request.session.get("login")
    no = request.GET.get('no')
    sc = Screen.objects.get(no=no)
    hl = Hall.objects.filter(Screen_no=no)
    sc1 = Screen.objects.filter(no__in=[2,3,4,5,6,7])
    sc2 = Screen.objects.filter(no__in=[8,9,10,11,12,13])
    sc3 = Screen.objects.filter(no__in=[14,14,15,16,17])
    

    context={
        'sc':sc,
        'hl':hl,
        'sc1':sc1,
        'sc2':sc2,
        'sc3':sc3,
        'login':login,
    }

    return render(request, 'category.html', context)
def get_schedule(request):
    if request.method == "GET":
        ondate_str = request.GET.get('ondate')
        no = request.GET.get('no')

        ondate = datetime.strptime(ondate_str, '%Y%m%d').strftime('%Y-%m-%d')
        hs = HallSchedule.objects.filter(ondate=ondate,Hall_no__Theater_no=no).values('no','stime','Movie_no','ondate','Hall_no','etime','Movie_no__krname','Hall_no__name','Movie_no__ViewableAge_no__name','Movie_no__runtime','Movie_no__opendate','Hall_no__Screen_no__name','Hall_no__floor','Hall_no__totseat')
        hs_list = list(hs)
        genre = MovieGenreMap.objects.filter(Movie_no__in=hs.values_list('Movie_no', flat=True))
        gen_list = list(genre)
        
        for item in hs_list:
            item['Movie_no'] = item['Movie_no__krname']
            item['Hall_no'] = item['Hall_no__name']
            item['Movie_view'] = item['Movie_no__ViewableAge_no__name']
            item['Movie_runtime'] = item['Movie_no__runtime']
            item['Movie_opendate'] = item['Movie_no__opendate']
            item['Screen_name'] = item['Hall_no__Screen_no__name']
            item['Floor'] = item['Hall_no__floor']
            item['Totseat'] = item['Hall_no__totseat']
        genre_data = [{'Movie_no': item.Movie_no.krname, 'Genre_name': item.Genre_no.name} for item in gen_list]

        

        context = {
            'hslist': hs_list,
            'genre':genre_data,
        }
        return JsonResponse(context)
    else:
        return JsonResponse({'error':'Invalid request'})
    
from django.http import JsonResponse

def recommandcount(request):
    if request.method == 'GET':
        review_no = request.GET.get('review_no')
        member_no = request.GET.get('member_no')
        print(review_no)
        print(member_no)
        rec = RecommandCount.objects.filter(member_no_id=member_no, MovieReview_no_id=review_no)
        print(rec)
        
        if rec.exists():
            rec.delete()
            rec = False
        else:
            RecommandCount.objects.create(member_no_id=member_no, MovieReview_no_id=review_no)
            rec = True

        return JsonResponse({'rec':rec})


def write_review(request:HttpRequest):
    login = request.session.get('login')
    movie_no = request.GET.get('Movie_no')
    member_no = request.GET.get('member_no')
    emotion = Emotion.objects.all()
    charm = Charm.objects.all()

    ticket = Ticket.objects.filter(HallSchedule_no__Movie_no_id=movie_no,vipps_no__member_no_id=login).first()
    
    movie = Movie.objects.get(no=movie_no)

    context= {
        'ticket':ticket,
        'movie':movie,
        'emotion':emotion,
        'charm':charm,
    }

    return render(request, 'review.html', context)

def checkwrite(request):
        movie_no = request.POST.get('Movie_no')
        print(movie_no)
        ticket_no = request.POST.get('ticket_no')
        goldenegg_no = request.POST.get('rating')
        review_content = request.POST.get('review_content')

        ticket = Ticket.objects.get(ticket_no=ticket_no)
        member_no = ticket.vipps_no.member_no
        profile_no = Profile.objects.get(member_no_id=member_no)

        emotions = request.POST.getlist('emotions[]')
        charms = request.POST.getlist('charms[]')

        MovieReview.objects.create(
            uploadtext=review_content,
            uploaddate=timezone.now(),
            recommand=0,
            GoldenEgg_no_id=goldenegg_no,
            Emotion_1=emotions[0] if emotions else 0,
            Emotion_2=emotions[1] if len(emotions) > 1 else 0,
            Emotion_3=emotions[2] if len(emotions) > 2 else 0,
            Emotion_4=emotions[3] if len(emotions) > 3 else 0,
            Emotion_5=emotions[4] if len(emotions) > 4 else 0,
            Charm_1=charms[0] if charms else 0,
            Charm_2=charms[1] if len(charms) > 1 else 0,
            Charm_3=charms[2] if len(charms) > 2 else 0,
            Charm_4=charms[3] if len(charms) > 3 else 0,
            Charm_5=charms[4] if len(charms) > 4 else 0,
            ticket_no_id=ticket_no,
            profile_no=profile_no,
        )
        return HttpResponse("리뷰작성에 성공했습니다.")

def movieCreate(request:HttpRequest):
    login = request.session.get('login')
    member = Members.objects.get(member_no=login).memberType_no.member_type
    if member != '관리자':
        return HttpResponse('잘못된 접근입니다.')
    Viewable = ViewableAge.objects.all()
    country = Country.objects.all()
    genre = Genre.objects.all()
    movietype = MovieType.objects.all()

    context = {
        'Viewable':Viewable,
        'country':country,
        'genre':genre,
        'type':movietype,
    }

    return render(request, 'moviecreate.html', context)

def checkCreate(request:HttpRequest):
    Movie_krname = request.POST.get('krname')
    Movie_ername = request.POST.get('ername')
    Movie_genre = request.POST.getlist('genre')
    Movie_country = request.POST.getlist('country')
    Movie_story = request.POST.get('story')
    Movie_runtime = request.POST.get('runtime')
    Movie_opendate = request.POST.get('opendate')
    Movie_site = request.POST.get('site')
    Movie_viewable = request.POST.get('viewable')
    Movie_image = request.POST.get('movie_image')
    Movie_type = request.POST.get('type')


    Movie.objects.create(krname=Movie_krname,ername=Movie_ername,story=Movie_story,runtime=Movie_runtime,opendate=Movie_opendate,site=Movie_site,ViewableAge_no_id=Movie_viewable,image=Movie_image,MovieType_no_id=Movie_type)
    movie = Movie.objects.get(krname=Movie_krname).no
    for i in Movie_genre:
        MovieGenreMap.objects.create(Movie_no_id=movie,Genre_no_id=i)
    for i in Movie_country:
        MovieCountryMap.objects.create(Movie_no_id=movie,Country_no_id=i)
    msg = "생성에 성공했습니다."
    url = "/movies/"
    context = {
        'msg':msg,
        'url':url
    }
    return render(request, 'movieresult.html', context)

    
def movieUpdate(request:HttpRequest):
    login = request.session.get('login')
    member = Members.objects.get(member_no=login).memberType_no.member_type
    if member != '관리자':
        return HttpResponse("잘못된 접근입니다.")
    Viewable = ViewableAge.objects.all()
    country = Country.objects.all()
    genre = Genre.objects.all()
    movietype = MovieType.objects.all()
    onmovie = Movie.objects.filter(status=None)

    context = {
        'Viewable':Viewable,
        'country':country,
        'genre':genre,
        'type':movietype,
        'onmovie':onmovie
    }

    return render(request, 'movieupdate.html', context)

def checkUpdate(request:HttpRequest):
    
    no = request.POST.get('movie_no')
    Movie_status = request.POST.get('status')
    Movie_krname = request.POST.get('krname')
    Movie_ername = request.POST.get('ername')
    Movie_genre = request.POST.getlist('genre')
    Movie_country = request.POST.getlist('country')
    Movie_story = request.POST.get('story')
    Movie_runtime = request.POST.get('runtime')
    Movie_opendate = request.POST.get('opendate')
    
    Movie_site = request.POST.get('site')
    Movie_viewable = request.POST.get('viewable')
    Movie_image = request.FILES.get('movie_image')
    Movie_type = request.POST.get('type')

    movie = Movie.objects.get(no=no)
    movie.status = Movie_status
    movie.krname = Movie_krname
    movie.ername = Movie_ername
    movie.story = Movie_story
    movie.runtime = Movie_runtime
    movie.opendate = Movie_opendate
    movie.site = Movie_site
    movie.ViewableAge_no_id = Movie_viewable
    movie.image = Movie_image
    movie.MovieType_no_id = Movie_type
    movie.save()
    MovieGenreMap.objects.filter(Movie_no_id=no).delete()
    MovieCountryMap.objects.filter(Movie_no_id=no).delete()
    for i in Movie_genre:
        MovieGenreMap.objects.create(Movie_no_id=no,Genre_no_id=i)
    for i in Movie_country:
        MovieCountryMap.objects.create(Movie_no_id=no,Country_no_id=i)
    msg = "수정에 성공했습니다"
    url = "/movies/"
    context={
        'msg':msg,
        'url':url
    }
    return render(request, 'movieresult.html', context)