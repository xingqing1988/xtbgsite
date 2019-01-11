import datetime
from django.shortcuts import render,redirect,get_object_or_404 
from django.contrib.auth.models import User
from subject.models import Subject,SubjectLevelOne,SubjectLevelTwo,SubjectType,Notice,SupFile,Image,File
from user.forms import SubForm,InquireForm,NoticeForm
from subject.views import get_subject_common_data
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    context['sbos'] = SubjectLevelOne.objects.all()
    return render(request,'index.html',context)

def home(request):
    if request.method == 'POST':
        inquire_form = InquireForm(request.POST)
        if inquire_form.is_valid():
            inquire_title = inquire_form.cleaned_data['title']
            inquire_sbo = inquire_form.cleaned_data['level_one']
            inquire_sbt = inquire_form.cleaned_data['level_two']
            inquire_type = inquire_form.cleaned_data['subject_type']
            inquire_user = inquire_form.cleaned_data['sub_author']
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            q = {}
            if inquire_title!='':
                q['title__icontains'] = inquire_title
            if inquire_sbo != '0':
                q['subject_level_one'] = get_object_or_404(SubjectLevelOne,pk=inquire_sbo)
            if inquire_sbt != '0':
                q['subject_level_two'] = get_object_or_404(SubjectLevelTwo,pk=inquire_sbt)
            if inquire_type != '0':
                q['subject_type'] = get_object_or_404(SubjectType,pk=inquire_type)
            if inquire_user != '0':
                q['author'] = get_object_or_404(User,pk=inquire_user)
            if (start_date !='') and (end_date !=''):
                q['created_time__range'] = (start_date,end_date)
            subjects =  Subject.objects.filter(**q)
    else:
        subjects = Subject.objects.all()
    context = get_subject_common_data(request,subjects) 
    context['subform'] = SubForm()
    context['inquireform'] =InquireForm()
    context['noticeform'] = NoticeForm()
    context['notices'] = Notice.objects.all()
    context['supfiles'] = SupFile.objects.all() 
    return render(request,'home.html',context)

def level_one(request,sbo_pk):
    sbo_get = get_object_or_404(SubjectLevelOne,pk=sbo_pk)
    subjects = Subject.objects.filter(subject_level_one=sbo_get)
    context = get_subject_common_data(request,subjects)
    context['sbo'] = sbo_get
    return render(request,'level_one.html',context)   

def level_two(request,sbt_pk):
    sbt_get = get_object_or_404(SubjectLevelTwo,pk=sbt_pk)
    subjects = Subject.objects.filter(subject_level_two=sbt_get)

    context = get_subject_common_data(request,subjects)
    context['sbt_get'] = sbt_get
    return render(request,'level_two.html',context)

def chart(request):

    now_year = int(datetime.datetime.now().strftime('%Y'))
    print(now_year)

    sub_summary_count_list = []
    sub_summary_get = get_object_or_404(SubjectType,pk=1)
    a = range(1,13)
    for b in a:
        sub_summary_count_for_month = Subject.objects.filter(subject_type=sub_summary_get,created_time__year=now_year,created_time__month=b).count()
        sub_summary_count_list.append(sub_summary_count_for_month)

    sub_plan_count_list = []
    sub_plan_get = get_object_or_404(SubjectType,pk=2)
    a = range(1,13)
    for b in a:
        sub_plan_count_for_month = Subject.objects.filter(subject_type=sub_plan_get,created_time__year=now_year,created_time__month=b).count()
        sub_plan_count_list.append(sub_plan_count_for_month)

    context = {}
    context['user_count'] = User.objects.all().count()
    context['sub_count'] = Subject.objects.all().count()
    context['image_count'] = Image.objects.all().count()
    context['file_count'] = File.objects.all().count()
    context['sub_summary_count_list'] = sub_summary_count_list
    context['sub_plan_count_list'] = sub_plan_count_list
    return render(request,'chart.html',context)