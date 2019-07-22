from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

#Extending form
class UserCreationFormEmail(UserCreationForm):
    email = forms.EmailField(required=True,help_text="Required Field, max 254 characters, and validing")

    class Meta:
        #Already exist a field "email" in Usrer's model, so just we're going to use it
        model = User
        fields = ('username','email','password1','password2')

    #Validaing a field
    def clean_email(self):
        email = self.cleaned_data.get("email") #Recover field fro validating
        #Check if there is already exist the e-mail
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("E-mail already exist") #Error message
        return email
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        #Fields we'e going to edit
        fields = ['avatar','bio','link']
        widgets = {
            #This filed allow us clear the input
            'avatar':forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3,'placeholder':'Biography'}),
            'link':forms.URLInput(attrs={'class':'form-control mt-3','placeholder':'Link'}),
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True,help_text="Required Field, max 254 characters, and validing")
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email") #Recover field fro validating
        #Changed_data is a list which stores all fields which have been edited at the form
        if 'email' in self.changed_data: #Mail has to had changed            
            if User.objects.filter(email=email).exists(): #mail musn't exist in BDD
                raise forms.ValidationError("E-mail already exist") #Error message
        return email