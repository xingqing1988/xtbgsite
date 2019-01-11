import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SubjectLevelOne(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name
    def sbt_object(self):               
        return self.subjectleveltwo_set.all()

class SubjectLevelTwo(models.Model):
    type_name = models.CharField(max_length=20)
    level_two_for_one = models.ForeignKey(SubjectLevelOne,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.type_name

    #增加一个类型下博客数量的方法，subject_set是反向获取被关联外键的model。模型名称小写加_set
    def subject_count(self):               
        return self.subject_set.count()

class SubjectType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name

    #增加一个类型下博客数量的方法，blog_set是反向获取被关联外键的model。模型名称小写加_set
    def subject_count(self):               
        return self.subject_set.count()

class Subject(models.Model):
    title = models.CharField(max_length=20)
    subject_level_one = models.ForeignKey(SubjectLevelOne,on_delete=models.DO_NOTHING)
    subject_level_two = models.ForeignKey(SubjectLevelTwo,on_delete=models.DO_NOTHING)
    subject_type = models.ForeignKey(SubjectType,on_delete=models.DO_NOTHING)
    content = models.TextField()
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<Blog: %s>" % self.title
    def image_object(self):               
        return self.image_set.all()
    def image_count(self):               
        return self.image_set.count()
    def file_object(self):               
        return self.file_set.all()
    def file_count(self):               
        return self.file_set.count()
    # 按创建时间倒序排序
    class Meta:
        ordering = ['-created_time']


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/image/%Y/%m/%d/',blank=True)
    image_sub = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_name(self):
        s = self.image.name
        path = os.path.dirname(s)
        get_name = s[len(path)+1:]
        return get_name

    # 按创建时间倒序排序
    class Meta:
        ordering = ['-created_time']

class File(models.Model):
    file = models.FileField(upload_to='uploads/file/%Y/%m/%d/',blank=True)
    file_sub = models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_name(self):
        s = self.file.name
        path = os.path.dirname(s)
        get_name = s[len(path)+1:]
        return get_name

    # 按创建时间倒序排序
    class Meta:
        ordering = ['-created_time']

class Notice(models.Model):
    text = models.CharField(max_length=300)
    author = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    # 按创建时间倒序排序
    class Meta:
        ordering = ['-created_time']

class SupFileType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name
    def supfile_object(self):               
        return self.supfile_set.all()
    def supfile_count(self):               
        return self.supfile_set.count()

class SupFile(models.Model):
    file = models.FileField(upload_to='uploads/supfile/%Y/%m/%d/')
    file_type = models.ForeignKey(SupFileType,on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)

    def get_name(self):
        s = self.file.name
        path = os.path.dirname(s)
        get_name = s[len(path)+1:]
        return get_name

    # 按创建时间倒序排序
    class Meta:
        ordering = ['-created_time']
