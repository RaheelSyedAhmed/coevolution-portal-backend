from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from celery.result import AsyncResult
from .tasks import get_msa_task, get_DI_pairs_task
import json

@csrf_exempt
def hello_world(request):
    return HttpResponse('hello world', status=200)

def demo(request):
    return render(request, 'demo.html')

@csrf_exempt
def job_status(request, id):
    task = AsyncResult(id)
    response = {'state': task.state}
    return JsonResponse(response)

@csrf_exempt
def job_result(request, id):
    task = AsyncResult(id)
    if task.state == 'SUCCESS':
        return HttpResponse(task.result)
    
    response = {'state': task.state}
    return JsonResponse(response, status=202)

@csrf_exempt
def get_msa(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        seq = data.get('sequence', '')
        task = get_msa_task.delay(seq)
        return JsonResponse({'task_id': task.id}, status=202)


@csrf_exempt
def get_DI_pairs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        seq = data.get('sequence', '')
        task = get_DI_pairs_task.delay(seq)
        return JsonResponse({'task_id': task.id}, status=202)