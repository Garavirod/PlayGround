from django.shortcuts import render
from .models import Thread, Message
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.http import Http404, JsonResponse
from django.shortcuts import  get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy

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

def add_message(request,pk):
    print(request.GET)
    # Cada vez que se envie un mensaje se devolverá un arespuesta
    # Si el msg se envia conrrectamente se cambiara a True
    jason_response = {'created':False}
    # Comproabamos si el usuario esta idenificado
    if request.user.is_authenticated:
        # Recuperamos el contenido del text area cuyo id es 'content'
        content = request.GET.get('content',None)
        if content:
            thread = get_object_or_404(Thread,pk=pk)
            message = Message.objects.create(user=request.user,conent=content)
            # añadimos el mensaje al hilo
            thread.messages.add(message)
            jason_response['created']=True
            if len(thread.messages.all()) is 1:
                jason_response['first'] = True
    else:
        raise Http404("User is not authenticated")
    return JsonResponse(jason_response) #Retorna un obj Json

# username es al que se le enviará el mensaje
@login_required #Al ser un método no se acrega el adorno al decorador
def start_thread(request,username):
    user = get_object_or_404(User,username=username)
    # Busca o devuleve un hilo si no existe
    # El hilo se inicia con el user y el user que tiene activa la sesión.
    thread = Thread.objects.find_or_create(user, request.user)
    return redirect(reverse_lazy('messenger:detail',args=[thread.pk]))