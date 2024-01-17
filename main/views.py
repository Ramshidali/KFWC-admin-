#standerd
import json
import datetime
from datetime import date, timedelta
#django
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User,Group
from main.forms import PasswordChangeForm
# third party
#local
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

        if form.is_valid():
            usr = User.objects.get(pk=request.user.pk)
            usr.set_password(form.cleaned_data['password'])
            usr.save()
            
            response_data = {
                "status": "true",
                "title": "Successful",
                "message": "Password Updated Successfully",
                'redirect': 'true',
                'redirect_url': reverse("main:index")
            }
            status_code = "200"
        else:
            message = generate_form_errors(form, formset=False)
            status_code = "400"
            response_data = {
                "status": "false",
                "message": message,
            }
            
        return HttpResponse(json.dumps(response_data),status=status_code, content_type="application/json")
        
    else :
        form = PasswordChangeForm()

        context = {
            'form': form,
        }
    
        return render(request,'registration/change_password.html', context)