from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm ,UserChangeForm, PasswordChangeForm

 
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
    
    


    class Meta:
        model= CustomUser
        fields= ('username','password1','password2','my_city')
        help_texts = {
            'password2': 'Enter the same password as above, for verification.',
        }


class CityUpdate(UserChangeForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        
        self.fields['username'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder':' Enter your username',

            }) 
        
    
        
        self.fields['my_city'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder':'Enter your city', 

            }) 
    
    


    class Meta:
        model= CustomUser
        fields= ('username','password','my_city')
       

class PasswordUpdate(PasswordChangeForm):
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        
        self.fields['old_password'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder': 'Enter your password', 

            }) 

        self.fields['new_password1'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder': 'Enter your password', 

            }) 
        
        self.fields['new_password2'].widget.attrs.update({ 
            'class': 'form-control', 
            'placeholder': 'Enter your password', 

            }) 
    
    
    class Meta:
        model= CustomUser
        fields= ('old_password','new_password1','new_password2')
       