from django.shortcuts import render
from django.views import View
# Create your views here.
class IndexView(View):
    def get(selef,request):
        '''首页'''
        return render(request,'index.html')