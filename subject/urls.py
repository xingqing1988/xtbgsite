from django.urls import path
from .views import sub_detail,image,file

urlpatterns = [
    path('<int:sub_pk>',sub_detail,name='sub_detail'),
    path('image',image,name='image'),
    path('file',file,name='file'),
]
