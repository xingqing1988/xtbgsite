from django.contrib import admin
from .models import Subject,SubjectType,SubjectLevelTwo,SubjectLevelOne,Image,File,Notice,SupFileType,SupFile


# Register your models here.

@admin.register(SubjectLevelOne)
class SubjectLevelOneAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
    ordering = ('id',)

@admin.register(SubjectLevelTwo)
class SubjectLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('id','type_name','level_two_for_one')
    ordering = ('id',)

@admin.register(SubjectType)
class SubjectTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
    ordering = ('id',)

@admin.register(Subject)    
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id','title','subject_type','subject_level_one','subject_level_two','author','created_time')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id','image','image_sub','created_time')
    ordering = ('id',)

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id','file','file_sub','created_time')
    ordering = ('id',)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id','text','author','created_time')
    ordering = ('id',)

@admin.register(SupFileType)
class SupFileTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')
    ordering = ('id',)

@admin.register(SupFile)
class SupFileAdmin(admin.ModelAdmin):
    list_display = ('id','file','file_type','created_time')
    ordering = ('id',)