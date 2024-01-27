from django import forms 
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

 
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder':' Enter your username', 
            'id': 'username_inp', 

            }) 
        
        self.fields['password1'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder': 'Enter your password', 

            }) 
        
        self.fields['password2'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder':'Confirm your password', 

            }) 
        
        self.fields['my_city'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder':'Enter your city', 

            }) 
    
    username = forms.CharField(max_length=20, label=False) 


    class Meta:
        model= CustomUser
        fields= ('username','password1','password2','my_city')
        help_texts = {
            'password2': 'Enter the same password as above, for verification.',
        }