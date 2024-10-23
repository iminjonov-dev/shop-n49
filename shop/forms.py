from dataclasses import fields

from django import forms
from django.forms import fields
from shop.models import Comment, Order, Product
from django.contrib.auth.models import AbstractUser

class CommentModelForm(forms.ModelForm):
     class Meta:
         model = Comment
         # fields = ['text']
         exclude = ('product',)

     def clean_email(self):
         email = self.data.get('email')
         if Comment.objects.filter(email=email).exists():
             raise forms.ValidationError(f'This {email} is already used')
         return email



def clean_body(self):
    negative_message = ['yomon','omelar', 'negatiflar','maslahar bermiman']
    body = self.data.get('body')
    if negative_message in body.split(''):
        raise
    return body


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)

def clean_email(self):
    email = self.data.get('email')
    if Comment.objects.filter(email=email).exists():
       raise forms.ValidationError(f'This {email} is already used')
    return email


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('product',)

class User(AbstractUser):

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

class AnonymousUser:
    id = None
    pk = None
    username = None
class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    # def clean_username(self):
    #     username = self.data.get('username')
    #     if not User.objects.filter(username=username).exists():
    #
    #       raise forms.ValidationError(f'The user {username} Not Fount')
    #     return username
