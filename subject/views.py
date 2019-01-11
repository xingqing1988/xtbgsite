from django.shortcuts import render,get_object_or_404 
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Subject,SubjectType,SubjectLevelOne,SubjectLevelTwo,SubjectType,Image,File
from user.forms import InquireMediaForm

# Create your views here.

def get_subject_common_data(request,subjects):
    paginator = Paginator(subjects,10)                  #对所有主题进行分页
    page_num = request.GET.get('page',1)            #获取URL的页码参数（GET请求）
    page_of_subjects = paginator.get_page(page_num)    #获取具体页码对应的主题分页
    current_page_num = page_of_subjects.number         #获取当前页的页码
    #获取当前页前后2页页码范围，并通过算法去掉小于第一个和大于最后一个的页码
    page_range = list(range(max(current_page_num-2,1),current_page_num))+\
                 list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    #加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    #加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages) 
  
    #给具体的日期增加获取相对应主题数量的属性
    subject_dates = {}
    for subject_date in Subject.objects.dates('created_time','month',order='DESC'):
        subject_count = Subject.objects.filter(created_time__year=subject_date.year,
                                                        created_time__month=subject_date.month).count()
        subject_dates[subject_date] = subject_count 
   
    context = {}
    context['subjects'] = page_of_subjects.object_list
    context['page_of_subjects'] = page_of_subjects
    context['page_range'] = page_range
    context['subject_types'] = SubjectType.objects.all()  #这里在models的SubjectType下增加了获取博客数量的方法
    context['subject_dates'] = subject_dates

    return context

def sub_detail(request,sub_pk):
    subject = get_object_or_404(Subject,pk=sub_pk)
    context = {}
    context['subject'] = subject
    context['previous_subject'] = Subject.objects.filter(created_time__gt=subject.created_time).last()
    context['next_subject'] = Subject.objects.filter(created_time__lt=subject.created_time).first()
    response = render(request,'sub_detail.html',context)          #注意这里的render方法的使用
    return response

def get_image_common_data(request,images):
    paginator = Paginator(images,20)                  #对所有主题进行分页
    page_num = request.GET.get('page',1)            #获取URL的页码参数（GET请求）
    page_of_images = paginator.get_page(page_num)    #获取具体页码对应的主题分页
    current_page_num = page_of_images.number         #获取当前页的页码
    #获取当前页前后2页页码范围，并通过算法去掉小于第一个和大于最后一个的页码
    page_range = list(range(max(current_page_num-2,1),current_page_num))+\
                 list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    #加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    #加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages) 
  
    #给具体的日期增加获取相对应主题数量的属性
    image_dates = {}
    for image_date in Image.objects.dates('created_time','month',order='DESC'):
        image_count = Image.objects.filter(created_time__year=image_date.year,
                                                        created_time__month=image_date.month).count()
        image_dates[image_date] = image_count 
   
    context = {}
    context['images'] = page_of_images.object_list
    context['page_of_images'] = page_of_images
    context['page_range'] = page_range
    context['image_dates'] = image_dates

    return context

def get_file_common_data(request,files):
    paginator = Paginator(files,20)                  #对所有主题进行分页
    page_num = request.GET.get('page',1)            #获取URL的页码参数（GET请求）
    page_of_files = paginator.get_page(page_num)    #获取具体页码对应的主题分页
    current_page_num = page_of_files.number         #获取当前页的页码
    #获取当前页前后2页页码范围，并通过算法去掉小于第一个和大于最后一个的页码
    page_range = list(range(max(current_page_num-2,1),current_page_num))+\
                 list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    #加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    #加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages) 
  
    #给具体的日期增加获取相对应主题数量的属性
    file_dates = {}
    for file_date in File.objects.dates('created_time','month',order='DESC'):
        file_count = File.objects.filter(created_time__year=file_date.year,
                                                        created_time__month=file_date.month).count()
        file_dates[file_date] = file_count 
   
    context = {}
    context['files'] = page_of_files.object_list
    context['page_of_files'] = page_of_files
    context['page_range'] = page_range
    context['file_dates'] = file_dates

    return context

def image(request):
    if request.method == 'POST':
        inquire_form = InquireMediaForm(request.POST)
        if inquire_form.is_valid():
            inquire_sbo = inquire_form.cleaned_data['level_one']
            inquire_sbt = inquire_form.cleaned_data['level_two']
            inquire_type = inquire_form.cleaned_data['subject_type']
            inquire_user = inquire_form.cleaned_data['sub_author']
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            q = {}
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
            images = []
            for subject in subjects:
                image = Image.objects.filter(image_sub=subject)
                for image_one in image:
                    images.append(image_one)
    else:
        images = Image.objects.all()
    context = get_image_common_data(request,images)
    context['inquiremediaform'] = InquireMediaForm() 
    return render(request,'image.html',context)

def file(request):
    if request.method == 'POST':
        inquire_form = InquireMediaForm(request.POST)
        if inquire_form.is_valid():
            inquire_sbo = inquire_form.cleaned_data['level_one']
            inquire_sbt = inquire_form.cleaned_data['level_two']
            inquire_type = inquire_form.cleaned_data['subject_type']
            inquire_user = inquire_form.cleaned_data['sub_author']
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            q = {}
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
            files = []
            for subject in subjects:
                file = File.objects.filter(file_sub=subject)
                for file_one in file:
                    files.append(file_one)
    else:
        files = File.objects.all()
    context = get_file_common_data(request,files)
    context['inquiremediaform'] = InquireMediaForm()
    return render(request,'file.html',context)