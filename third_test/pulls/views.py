from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Choise, Questions

# Create your views here.

def index(request):
    latest_que = Questions.objects.order_by('-pub_date')[:5]
    context = {'latest_que': latest_que}
    return render(request, 'pulls/index.html', context)

def detail(request, q_id):
    que = get_object_or_404(Questions, pk = q_id)
    return render(request, 'pulls/detail.html', {'que':que})

def results(request, q_id):
    que = get_object_or_404(Questions, id = q_id)
    return render(request, 'pulls/results.html', {'que':que})

def vote(request, q_id):
    que = get_object_or_404(Questions, id = q_id)
    try:
        selected_choise = que.choise_set.get(pk=request.POST['choice'])
    except (KeyError, Choise.DoesNotExist):
        return render(request, 'pulls/detail.html', {'que':que})
    else:
        selected_choise.votes +=1
        selected_choise.save()
        return HttpResponseRedirect(reverse('pulls:results', args=(que.id,)))