from .forms import UserCreationFormEmail, ProfileForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Profile

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

@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_form.html'

    def get_object(self):
        #Get the object we're going to edit
        #We get the object from the user that is at the request
        #get_or_create retunr a tuple, if there not exist a profile, it creates one
        profile, create =  Profile.objects.get_or_create(user=self.request.user)
        return profile