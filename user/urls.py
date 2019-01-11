from django.urls import path
from .views import login,logout,user_info,personal_sub_summary,personal_sub_plan,update_sub,personal_sub_image,personal_sub_file,update_notice,change_level_one,supfile,supfile_one,supfile_two,change_password

urlpatterns = [
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('user_info/',user_info,name='user_info'),
    path('personal_sub_summary',personal_sub_summary,name='personal_sub_summary'),
    path('personal_sub_plan',personal_sub_plan,name='personal_sub_plan'),
    path('personal_sub_image',personal_sub_image,name='personal_sub_image'),
    path('personal_sub_file',personal_sub_file,name='personal_sub_file'),
    path('update_sub',update_sub,name='update_sub'),
    path('update_notice',update_notice,name='update_notice'),
    path('change_level_one',change_level_one,name='change_level_one'),
    path('supfile',supfile,name='supfile'),
    path('supfile_one',supfile_one,name='supfile_one'),
    path('supfile_two',supfile_two,name='supfile_two'),
    path('change_password',change_password,name='change_password'),
]
