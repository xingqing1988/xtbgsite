from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from subject.models import SubjectLevelOne,SubjectLevelTwo,SubjectType
from ckeditor.widgets import CKEditorWidget #引入富文本小部件

class LoginForm(forms.Form):

    username = forms.CharField(label='',
                               widget=forms.TextInput(attrs={'class':'username','placeholder':'请输入用户名'}))
    password = forms.CharField(label='',
                               widget=forms.PasswordInput(attrs={'class':'password','placeholder':'请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class SubForm(forms.Form):

    title = forms.CharField(label='主题名称:',max_length=20,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入主题名称'}))

    choice_one = SubjectLevelOne.objects.all().values_list('id','type_name')

    level_one = forms.CharField(label='请选择一级类:',
                               widget=forms.Select(choices=choice_one,attrs={'class':'form-control'}))
    choice_two = SubjectLevelTwo.objects.all().values_list('id','type_name')

    level_two = forms.CharField(label='请选择二级级类:',
                               widget=forms.Select(choices=choice_two,attrs={'class':'form-control'}))

    choice_type = SubjectType.objects.all().values_list('id','type_name')

    subject_type = forms.CharField(label='请选择类型:',
                               widget=forms.Select(choices=choice_type,attrs={'class':'form-control'}))

    text = forms.CharField(label='',
                          widget=CKEditorWidget(config_name='comment_ckeditor'),
                          error_messages={'required':'评论内容不能为空'})#这里采用富文本评论框

    image = forms.ImageField(label='上传图片(上传多张图片请一次性选择多个)',required=False,     #这里注意：form表单里，enctype="multipart/form-data" 为必须填写项，否则上传的文件将不给予保存
                            widget=forms.ClearableFileInput(
                              attrs={'multiple': True,'class':'file-loading'})) 

    file = forms.FileField(label='上传文件(上传多个文件请一次性选择多个)',required=False,        #这里注意：form表单里，enctype="multipart/form-data" 为必须填写项，否则上传的文件将不给予保存
                          widget=forms.ClearableFileInput(
                          attrs={'multiple': True,'class':'file-loading'}))  

    #这里魔法方法把request.user传进来
    def __init__(self,*args,**kwargs):
      if 'user' in kwargs:
          self.user = kwargs.pop('user')
      super(SubForm,self).__init__(*args,**kwargs)

    def clean(self):
      #用户登陆验证
      if self.user.is_authenticated:
         self.cleaned_data['user'] = self.user
      else:
          raise ValidationError('用户未登陆')
     #表单对象验证
      level_one_id = self.cleaned_data['level_one']
      level_two_id = self.cleaned_data['level_two']
      try:
          level_one = SubjectLevelOne.objects.get(id=level_one_id)
          level_two = SubjectLevelTwo.objects.get(id=level_two_id)
      except ObjectDoesNotExist:
          raise forms.ValidationError('请正确选择分类')
      return self.cleaned_data

class NoticeForm(forms.Form):
    text = forms.CharField(max_length=100,widget=CKEditorWidget(attrs={'id':'notice_text'},config_name='comment_ckeditor'),
                           error_messages={'required':'评论内容不能为空'})#这里采用富文本评论框

      #这里魔法方法把request.user传进来
    def __init__(self,*args,**kwargs):
      if 'user' in kwargs:
          self.user = kwargs.pop('user')
      super(NoticeForm,self).__init__(*args,**kwargs)

    def clean(self):
      #用户登陆验证
      if self.user.is_authenticated:
          self.cleaned_data['user'] = self.user
      else:
          raise ValidationError('用户未登陆')
      return self.cleaned_data


class InquireForm(forms.Form):

    title = forms.CharField(label='主题名称',max_length=20,required=False,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入名称关键字'}))

    choice_one = SubjectLevelOne.objects.all().values_list('id','type_name')
    level_one = forms.CharField(label='一级类',
                               widget=forms.Select(choices=choice_one,attrs={'class':'form-control','id':'inquire_level_one'}))

    choice_two = SubjectLevelTwo.objects.all().values_list('id','type_name')
    level_two = forms.CharField(label='二级类',
                               widget=forms.Select(choices=choice_two,attrs={'class':'form-control','id':'inquire_level_two'}))

    choice_type = SubjectType.objects.all().values_list('id','type_name')
    subject_type = forms.CharField(label='类型',
                               widget=forms.Select(choices=choice_type,attrs={'class':'form-control','id':'inquire_subject_type'}))

    choice_user = User.objects.all().values_list('id','username')
    sub_author = forms.CharField(label='完成人',
                               widget=forms.Select(choices=choice_user,attrs={'class':'form-control','id':'inquire_sub_author'}))

class InquireMediaForm(forms.Form):

    choice_one = SubjectLevelOne.objects.all().values_list('id','type_name')
    level_one = forms.CharField(label='一级类',
                               widget=forms.Select(choices=choice_one,attrs={'class':'form-control','id':'inquire_level_one'}))

    choice_two = SubjectLevelTwo.objects.all().values_list('id','type_name')
    level_two = forms.CharField(label='二级类',
                               widget=forms.Select(choices=choice_two,attrs={'class':'form-control','id':'inquire_level_two'}))

    choice_type = SubjectType.objects.all().values_list('id','type_name')
    subject_type = forms.CharField(label='类型',
                               widget=forms.Select(choices=choice_type,attrs={'class':'form-control','id':'inquire_subject_type'}))

    choice_user = User.objects.all().values_list('id','username')
    sub_author = forms.CharField(label='完成人',
                               widget=forms.Select(choices=choice_user,attrs={'class':'form-control','id':'inquire_sub_author'}))

class ChangePassword(forms.Form):
    old_password = forms.CharField(label='请输入原密码',
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':''}))
    new_password = forms.CharField(label='请输入新密码',
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':''}))
    new_password_again = forms.CharField(label='请确认新密码',
                               widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':''}))
    
     #这里魔法方法把request.user传进来
    def __init__(self,*args,**kwargs):
      if 'user' in kwargs:
          self.user = kwargs.pop('user')
      super(ChangePassword,self).__init__(*args,**kwargs)

    def clean(self):
        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']
        new_password_again = self.cleaned_data['new_password_again']
        username = self.user.username
        user = auth.authenticate(username=username,password=old_password)
        if user:
          print('原密码正确')
          if new_password_again != new_password:
            print('抛出错误信息')
            raise forms.ValidationError('两次输入密码不一致')
          self.cleaned_data['user'] = self.user
        else:
            print('原密码不正确')
            raise forms.ValidationError('原密码输入不正确')
        return self.cleaned_data
