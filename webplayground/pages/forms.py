from django import forms
from .models import Page

class PageForm(forms.ModelForm):
    class Meta:
        model = Page #Modelo
        #Campos que se le permite a usuaro editar en este formualrio
        fields = ['title','content','order']
        #Configuraciones vanzadas para el fomulario
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título'}), #Clase de boootraps que añade los estilos
            'content':forms.Textarea(attrs={'class':'form-control'}),
            'order': forms.NumberInput(attrs={'class':'form-control'})
        }

        labels = {'title':'','order':'','content':''} #Las etiquitas las deja vacias
