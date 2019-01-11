from django.shortcuts import render,redirect,get_object_or_404  
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from .forms import LoginForm,SubForm,NoticeForm,ChangePassword
from subject.models import Subject,SubjectLevelOne,SubjectLevelTwo,SubjectType,Image,File,Notice,SupFile,SupFileType
from subject.views import get_subject_common_data,get_image_common_data,get_file_common_data

# Create your views here.
def login(request):
    if request.method == 'POST':    #判断请求方式
        login_form = LoginForm(request.POST)  #创建带有请求数据的表单实例
        if login_form.is_valid():   #对表单实例进行验证
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect('index')  
    else:      
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request,'login.html',context)

def logout(request):
    auth.logout(request)
    return redirect('login')

def user_info(request):
    context = {}
    return render(request,'user_info.html',context)

def personal_sub_summary(request):
    author = request.user
    subjects = Subject.objects.filter(author=author,subject_type=get_object_or_404(SubjectType,pk=1))
    context = get_subject_common_data(request,subjects) 
    return render(request,'personal_sub.html',context) 

def personal_sub_plan(request):
    author = request.user
    subjects = Subject.objects.filter(author=author,subject_type=get_object_or_404(SubjectType,pk=2))
    context = get_subject_common_data(request,subjects) 
    return render(request,'personal_sub.html',context)

def personal_sub_image(request):
    author = request.user
    subjects = Subject.objects.filter(author=author)
    images = []
    for subject in subjects:
        image = Image.objects.filter(image_sub=subject)
        for image_one in image:
            images.append(image_one) 
    context = get_image_common_data(request,images) 
    return render(request,'image.html',context) 

def personal_sub_file(request):
    author = request.user
    subjects = Subject.objects.filter(author=author)
    files = []
    for subject in subjects:
        file = File.objects.filter(file_sub=subject)
        for file_one in file:
            files.append(file_one) 
    context = get_file_common_data(request,files) 
    return render(request,'file.html',context)   

def update_sub(request):
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    sub_form = SubForm(request.POST,request.FILES,user=request.user)

    if sub_form.is_valid():

        #检查通过，保存数据
        sub = Subject()
        sub.author = request.user
        sub.title = sub_form.cleaned_data['title']
        sub.content = sub_form.cleaned_data['text']
        sub.subject_level_one = SubjectLevelOne.objects.get(id=sub_form.cleaned_data['level_one'])
        sub.subject_level_two = SubjectLevelTwo.objects.get(id=sub_form.cleaned_data['level_two'])
        sub.subject_type = SubjectType.objects.get(id=sub_form.cleaned_data['subject_type'])
        sub.save()

        #保存文件数据
        if request.FILES.getlist('file'):
            subject_get = get_object_or_404(Subject,pk=sub.pk)
            files_get = request.FILES.getlist('file')
            #循环保存文件数据
            for file_get in files_get:
                file = File()
                file.file_sub = subject_get
                file.file = file_get
                file.save()

        #保存图片数据
        if request.FILES.getlist('image'):
            subject_get = get_object_or_404(Subject,pk=sub.pk)
            images_get = request.FILES.getlist('image')
            #循环保存
            for image_get in images_get:
                image = Image()
                image.image_sub = subject_get
                image.image = image_get
                image.save()
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':list(sub_form.errors.values())[0][0],'redirect_to':referer})

def update_notice(request):
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    notice_form = NoticeForm(request.POST,user=request.user)

    if notice_form.is_valid():
        #检查通过，保存数据
        notice = Notice()
        notice.text = notice_form.cleaned_data['text']
        notice.author = request.user
        notice.save()
        return redirect(referer)
    else:
        return render(request,'error.html',{'message':list(notice_form.errors.values())[0][0],'redirect_to':referer})


@csrf_exempt
def change_level_one(request):
    data = {}
    sbo_id = request.POST.get('sbo_id')
    sbo_object = get_object_or_404(SubjectLevelOne,pk=int(sbo_id))
    sbt = SubjectLevelTwo.objects.filter(level_two_for_one=sbo_object).values_list('id','type_name')
   
    data['choice_two'] = list(sbt)
    return JsonResponse(data)

def supfile(request):
    if request.method == 'POST':
        created_time_start = request.POST.get('start_date')
        created_time_end = request.POST.get('end_date')
        q = {}
        if (created_time_start !='') and (created_time_end != ''):
            q['created_time__range'] = (created_time_start,created_time_end)
        files = SupFile.objects.filter(**q)
    else:
        files = SupFile.objects.all()
    context = get_file_common_data(request,files)
    return render(request,'sup_file.html',context)
   
def supfile_one(request):
    files = SupFile.objects.filter(file_type=get_object_or_404(SupFileType,pk=1))
    context = get_file_common_data(request,files)
    return render(request,'sup_file.html',context)

def supfile_two(request):
    files = SupFile.objects.filter(file_type=get_object_or_404(SupFileType,pk=2))
    context = get_file_common_data(request,files)
    return render(request,'sup_file.html',context)

def change_password(request):
    if request.method == 'POST':
        cpform = ChangePassword(request.POST,user=request.user)
        if cpform.is_valid():
            new_password = cpform.cleaned_data['new_password']
            user = cpform.cleaned_data['user']
            user.set_password(new_password)
            user.save()
            context = {}
            context['message'] = '修改成功,3秒后重新登陆'
            return render(request,'message.html',context) 
    else:      
        cpform = ChangePassword()
    context = {}
    context['cpform'] = cpform
    return render(request,'change_password.html',context) 
