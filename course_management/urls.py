from django.contrib import admin
from django.views.static import serve
from django.urls import  include, path, re_path

from course_management import settings
from main import views as general_views

urlpatterns = [
    path('',include(('main.urls'),namespace='main')),
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),
    path('super-admin/main/',general_views.app,name='app'),
    path('summernote/', include('django_summernote.urls')),
    
    path('super-admin/course/',include(('courses.urls'),namespace='courses')),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
