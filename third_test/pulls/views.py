from django.shortcuts import render, get_object_or_404

from .models import Questions

# Create your views here.

def index(request):
    latest_que = Questions.objects.order_by('-pub_date')[:5]
    context = {'latest_que': latest_que}
    return render(request, 'pulls/index.html', context)

def detail(request, q_id):
    que = get_object_or_404(Questions, pk = q_id)
    return render(request, 'pulls/detail.html', {'que':que})

def results(request, q_id):
    return None

def vote(request, q_id):
    return None