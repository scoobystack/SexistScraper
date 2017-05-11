from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render,redirect
from forms import JobProviderForm
from models import Job
from jobsprovider import JobsProvider
import urllib

User = get_user_model()

def index(request):
    form = JobProviderForm()
    return render(request, 'index.html', {'form': form})

def getjobs(request):
    #populate provider with inputs from request
    jp = JobsProvider()
    jp_form = JobProviderForm(request.POST)
    urlparams = {}

    if jp_form.is_valid():
        jp.query = jp_form.cleaned_data['query']
        jp.location = jp_form.cleaned_data['location']
        jp.count = jp_form.cleaned_data['count']
        jp.getJobs()
        urlparams['query'] = jp.query
    else:
        request.session['is_jp_valid'] = False

    return redirect('jobs/?' + urllib.urlencode(urlparams))


def jobs(request):
    query = request.GET.get('query', '')
    latest_job_list = Job.objects.filter(query=query).order_by('-date_posted')[:]
    context = {
        'latest_job_list': latest_job_list,
        'is_jp_valid': request.session.pop('is_jp_valid', True)
    }
    return render(request, 'jobs/index.html', context)

def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('user_list'))
        else:
            print(form.errors)
    return render(request, 'log_in.html', {'form': form})

@login_required(login_url='/log_in/')
def log_out(request):
    logout(request)
    return redirect(reverse('log_in'))

def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('log_in'))
        else:
            print(form.errors)
    return render(request, 'sign_up.html', {'form': form})

@login_required(login_url='/log_in/')
def user_list(request):
    users = User.objects.select_related('logged_in_user')
    for user in users:
        user.status = 'Online' if hasattr(user, 'logged_in_user') else 'Offline'
    return render(request, 'user_list.html', {'users': users})