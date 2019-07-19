from .models import Page
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from .forms import PageForm
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
# Create your views here.
#Retornar una lista de intsacoas de un modelo

class StaffRequiredMixin(object):
    """
        Este mixin requeriria que el usrio sea mimbro del staff
    """
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_staff: de esto e encarga el decorador ya
        #   return redirect(reverse_lazy('admin:login'))
        return super(StaffRequiredMixin,self).dispatch(request,*args,**kwargs)

class PageListView(ListView):
    model = Page

class PageDetailView(DetailView):
    model = Page

@method_decorator(staff_member_required,name='dispatch') #Decora el método dispatch del decorador
class PageCreate(CreateView): #La clase StaffRequiredMixin tendrá prioridad
    model = Page
    #Formualrio
    form_class = PageForm
    success_url = reverse_lazy('pages:pages')
    # def get_success_url(self):
    #     return reverse('pages:pages') 
     
@method_decorator(staff_member_required,name='dispatch')
class PageUpdate(UpdateView):
    model = Page
    #Campos que puede editar el usuario al crear la página
    form_class = PageForm
    #fields = ['title','content','order']
    template_name_suffix = '_update_form'
    def get_success_url(self):
        #this rwtruns url with an argument update's id <pk> 
        return reverse_lazy('pages:update',args=[self.object.id]) + '?ok'
        
@method_decorator(staff_member_required,name='dispatch')
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')