from django.http import HttpResponse
from django.shortcuts import render,redirect
from models import Job


def index(request):
    return render(request, 'index.html')

def jobs(request):
    latest_job_list = Job.objects.order_by('-date_scraped')[:5]
    context = {
        'latest_job_list': latest_job_list,
    }
    return render(request, 'jobs/index.html', context)

def getjobs(request):
    #call to scrape data and populate db with jobs
    return redirect('jobs')