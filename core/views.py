from django.http import HttpResponse
from django.shortcuts import render,redirect
from forms import JobProviderForm
from models import Job
from jobsprovider import JobsProvider


def index(request):
    form = JobProviderForm()
    return render(request, 'index.html', {'form': form})


def getjobs(request):
    #populate provider with inputs from request
    jp = JobsProvider()
    jp_form = JobProviderForm(request.POST)

    if jp_form.is_valid():
        jp.query = jp_form.cleaned_data['query']
        jp.location = jp_form.cleaned_data['location']
        jp.count = jp_form.cleaned_data['count']
        jp.getJobs()
    else:
        request.session['is_jp_valid'] = False

    return redirect('jobs')


def jobs(request):
    latest_job_list = Job.objects.order_by('-date_posted')[:]
    context = {
        'latest_job_list': latest_job_list,
        'is_jp_valid': request.session.pop('is_jp_valid', True)
    }

    return render(request, 'jobs/index.html', context)