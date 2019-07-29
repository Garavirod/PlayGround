from django.shortcuts import render
from .models import Thread
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.http import Http404

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
@method_decorator(login_required,name='dispatch')
class ThreadList(TemplateView):
    template_name = "messenger/thread_list.html"
    # Filatrar las conversaciones del usuario identificado
    # model = Thread
    # def get_queryset(self):
    #     queryset =  super(ThreadList,self).get_queryset()
    #     # User identificado en este momento
    #     return queryset.filter(users=self.request.user)
@method_decorator(login_required,name='dispatch')
class ThreadDetail(DetailView):
    model = Thread
    # El usuario puede ver los hilos solo de los que forma parte
    def get_object(self):
        obj = super(ThreadDetail,self).get_object()
        # comporbamos si el usuario no esta en el hilo
        if self.request.user not in obj.users.all():
            raise Http404
        return obj #Todso los mensajes que feoman parte de el