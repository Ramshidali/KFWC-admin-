#standerd
import json
import datetime
#django
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from django.core.serializers import serialize

from courses.forms import CourseForm, DetailsForm
from courses.models import Course, Details
#local
from main.decorators import role_required
from main.functions import encrypt_message, generate_form_errors, get_auto_id, paginate, randomnumber

# Create your views here.
def course_description(request,pk):
    
    if (instances:=Course.objects.filter(pk=pk,is_deleted=False)).exists():
        description = instances.first().description
        
        status_code = "200"
        response_data = {
            "status": "true",
            "description": mark_safe(description),
        }
    else:
        status_code = "400"
        response_data = {
            "status": "true",
            "description": '',
        }
        
    return HttpResponse(json.dumps(response_data),status=status_code,content_type="application/json")


def course_details(request,pk):
    instances = Details.objects.filter(course__pk=pk,is_deleted=False)
    data = {
        'instances': list(instances.values('id', 'title','description')),
        }
    return JsonResponse(data)


@login_required
@role_required(['superadmin','admin_user'])
def courses_list(request):
    """
    courses listings
    :param request:
    :return: courses list view
    """
    instances = Course.objects.filter(is_deleted=False).order_by("-id")
    
    filter_data = {}
    query = request.GET.get("q")
    
    if query:

        instances = instances.filter(
            Q(title__icontains=query)
        )
        title = "Courses - %s" % query
        filter_data['q'] = query
          

    context = {
        'instances': instances,
        'page_name' : 'Courses',
        'page_title' : 'Courses',
        'filter_data' : filter_data
    }

    return render(request, 'admin_panel/pages/courses/list.html', context)

@login_required
@role_required(['superadmin','admin_user'])
def create_course(request):
    """
    create operation of course
    :param request:
    :return:
    """
    # check pk for getting instance    
    
    courseDetailsFormset = formset_factory(DetailsForm, extra=2)
    
    message = ''
    if request.method == 'POST':
        
        form = CourseForm(request.POST,files=request.FILES)
        course_details_formset = courseDetailsFormset(request.POST,request.FILES,prefix='course_details_formset', form_kwargs={'empty_permitted': False})
        
        if form.is_valid() and course_details_formset.is_valid():
            try:
                with transaction.atomic():
                    #create course
                    data = form.save(commit=False)
                    data.auto_id = get_auto_id(Course)
                    data.creator = request.user
                    data.date_updated = datetime.datetime.today()
                    data.updater = request.user
                    data.user = request.user
                    data.save()
                    
                    if course_details_formset.is_valid():
                        for form in course_details_formset:
                            u_data = form.save(commit=False)
                            u_data.course = data
                            u_data.save()
                    
                    response_data = {
                        "status": "true",
                        "title": "Successfully Created",
                        "message": "course created successfully.",
                        'redirect': 'true',
                        "redirect_url": reverse('courses:courses_list')
                    }
                    
            except IntegrityError as e:
                # Handle database integrity error
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": "Integrity error occurred. Please check your data.",
                }

            except Exception as e:
                # Handle other exceptions
                response_data = {
                    "status": "false",
                    "title": "Failed",
                    "message": str(e),
                }
        else:
            message = generate_form_errors(form,course_details_formset, formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message,
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')

    else:
        form = CourseForm()
        course_details_formset = courseDetailsFormset(prefix='course_details_formset')

        context = {
            'form': form,
            'course_details_formset': course_details_formset,
            
            'page_name' : 'Create Course',
            'page_title' : 'Create Course',
            'is_need_select2' : True,
            'url' : reverse('courses:create_course'),
        }

        return render(request, 'admin_panel/pages/courses/create.html',context)


@login_required
@role_required(['superadmin','admin_user'])
def edit_course(request,pk):
    """
    edit operation of course
    :param request:
    :param pk:
    :return:
    """
    course_instance = get_object_or_404(Course, pk=pk)
    course_details_instances = Details.objects.filter(course=course_instance,is_deleted=False)
        
    if Details.objects.filter(course=course_instance).exists():
        d_extra = 0
    else:
        d_extra = 1 

    courseDetailsFormset = inlineformset_factory(
        Course,
        Details,
        extra=d_extra,
        form=DetailsForm,
    )
        
    message = ''
    
    if request.method == 'POST':
        form = CourseForm(request.POST,files=request.FILES,instance=course_instance)
        course_document_formset = courseDetailsFormset(request.POST,request.FILES,
                                            instance=course_instance,
                                            prefix='course_document_formset',
                                            form_kwargs={'empty_permitted': False})            
        
        if form.is_valid() and course_document_formset.is_valid():
            
            #create course
            data = form.save(commit=False)
            data.date_updated = datetime.datetime.today()
            data.updater = request.user
            data.save()
            
            #create multiple images
            if course_document_formset.is_valid():
                for form in course_document_formset:
                    if form not in course_document_formset.deleted_forms:
                        i_data = form.save(commit=False)
                        if not i_data.course :
                            i_data.course = data
                        i_data.save()

                for f in course_document_formset.deleted_forms:
                    f.instance.delete()
            
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Course Updated Successfully.",
                'redirect': 'true',
                "redirect_url": reverse('courses:courses_list'),
                "return" : True,
            }

            else:
                response_data = {
                "status": "true",
                "title": "Successfully Updated",
                "message": "Course Updated successfully.",
                'redirect': 'true',
                "redirect_url": reverse('courses:courses_list'),
                "return" : False,
            }
    
        else:
            message = generate_form_errors(course_document_formset,formset=True)
            
            response_data = {
                "status": "false",
                "title": "Failed",
                "message": message
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
                        
    else:

        form = CourseForm(instance=course_instance)
        course_document_formset = courseDetailsFormset(queryset=course_details_instances,
                                    prefix='course_document_formset',
                                    instance=course_instance)
        
        context = {
            'form': form,
            'course_document_formset': course_document_formset,
            'message': message,
            'course_instance': course_instance,
            'course_details_instances': course_details_instances,
            'page_name' : 'edit course',
            'url' : reverse('courses:edit_course', args=[course_instance.pk]),            
        }

        return render(request, 'admin_panel/pages/courses/create.html', context)


@login_required
@role_required(['superadmin','admin_user'])
def delete_course(request, pk):
    """
    course deletion, it only mark as is deleted field to true
    :param request:
    :param pk:
    :return:
    """
    Course.objects.filter(pk=pk).update(is_deleted=True)
    Details.objects.filter(course__pk=pk).update(is_deleted=True)
    
    response_data = {
        "status": "true",
        "title": "Successfully Deleted",
        "message": "Course Successfully Deleted.",
        "redirect": "true",
        "redirect_url": reverse('courses:courses_list')
    }

    return HttpResponse(json.dumps(response_data), content_type='application/javascript')