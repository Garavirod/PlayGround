from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = "core/home.html"
    
    #Sobre escribimos el método get
    def get(self,request, *args, **kwargs):
        return render(request,self.template_name, {'title':'Garavirod'})


class SamplePageView(TemplateView):
    template_name = "core/sample.html"   
