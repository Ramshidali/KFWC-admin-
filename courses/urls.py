from django.urls import path,re_path
from . import views

app_name = 'courses'

urlpatterns = [
    re_path(r'^course-description/(?P<pk>.*)/$', views.course_description, name='course_description'),
    re_path(r'^course-details/(?P<pk>.*)/$', views.course_details, name='course_details'),
    
    path('list/', views.courses_list, name='courses_list'),
    re_path(r'^create-course/$', views.create_course, name='create_course'),
    # re_path(r'^tenant-info/(?P<pk>.*)/$', views.tenant_info, name='tenant_info'),
    re_path(r'^edit-course/(?P<pk>.*)/$', views.edit_course, name='edit_course'),
    re_path(r'^delete-course/(?P<pk>.*)/$', views.delete_course, name='delete_course'),
]