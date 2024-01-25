from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
 
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
    
    username = forms.CharField(max_length=20, label=False) 


    class Meta:
        model= User
        fields= ('username','password1','password2',)
        help_texts = {
            'password2': 'Enter the same password as above, for verification.',
        }