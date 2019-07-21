from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        

