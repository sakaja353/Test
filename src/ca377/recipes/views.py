from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
  '''View function for home page.'''
  ctx = {}
  return render(request, 'recipes/index.html', context=ctx)
