from .forms import UserCreationFormEmail
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
# Create your views here.
class SignupView(CreateView):
    form_class = UserCreationFormEmail
    template_name = 'registration/signup.html'

    #Modifica en tiempo de ejecucion el enlace
    def get_success_url(self):
        return reverse_lazy('login') + '?ok'

    def get_form(self, form_class=None):
        form =  super(SignupView,self).get_form()
        #Modifying the form in real time
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control bm-2','placeholder':'Username'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control bm-2','placeholder':'E-mail'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control bm-2','placeholder':'Password 1'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control bm-2','placeholder':'Password 2'})
        return form

