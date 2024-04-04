from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User



class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=50,help_text="Please add a valid Email")

    class Meta:
        model = User #so that it can write to the user model in database
        fields = ["email","username","password1","password2"]  #type fields in the order that you want them to appear

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # remove labels
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].label = ''

        #add placeholders
        self.fields['username'].widget.attrs.update({'placeholder':('Username')})
        self.fields['email'].widget.attrs.update({'placeholder':('Email')})
        self.fields['password1'].widget.attrs.update({'placeholder':('Password')})        
        self.fields['password2'].widget.attrs.update({'placeholder':('Repeat password')})



