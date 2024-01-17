#standerd
import json
import datetime
from datetime import date, timedelta
#django
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse

# third party
#local
from main.forms import PasswordChangeForm
from main.decorators import role_required
from main.functions import generate_form_errors

# Create your views here.
@login_required
@role_required(['superadmin'])
def app(request):
  
    return HttpResponseRedirect(reverse('main:index'))

# Create your views here.
@login_required
@role_required(['superadmin'])
def index(request):
    
    today_date = timezone.now().date()
    last_month_start = (today_date - timedelta(days=today_date.day)).replace(day=1)
    
    context = {
        'page_name' : 'Dashboard',
    }
  
    return render(request,'admin_panel/index.html', context)

@login_required
def change_password(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        password_matches = check_password(request.POST.get("current_password"), request.user.password)
        
        if password_matches:
            print("matched")
            if form.is_valid():
                print("valid")
                
                usr = User.objects.get(pk=request.user.pk)
                usr.set_password(form.cleaned_data['password'])
                usr.save()
                
                response_data = {
                    "status": "true",
                    "title": "Successful",
                    "message": "Password Updated Successfully",
                    'redirect': 'true',
                    'redirect_url': reverse("main:profile")
                }
            else:
                print("not valid")
                message = generate_form_errors(form, formset=False)
                response_data = {
                    "status": "false",
                    "title": "Filed",
                    "message": message,
                }
        else:
            print("not match")
            response_data = {
                "status": "false",
                "title": "Filed",
                "message": "current password not match",
            }
            
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    
    
@login_required
def profile(request):
    
    instance = User.objects.get(pk=request.user.pk)
    form = PasswordChangeForm()
    
    context = {
        'instance': instance,
        'form': form,
    }

    return render(request,'admin_panel/pages/profile.html', context)