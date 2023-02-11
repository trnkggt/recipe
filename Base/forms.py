from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User

from .models import Recipe, Profile, Comment


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['user', 'created']
        widgets = {'title':forms.TextInput(
                                   attrs={'class':'form-control form-control-lg',
                                          'id':"typeEmailX-2",
                                          'placeholder':'title'}
                               ),
                    'content':forms.Textarea(attrs={'class':'form-control form-control-lg',
                                          'id':"typeEmailX-2",
                                          'placeholder':'content'}),
                    'dish_type':forms.Select(attrs={'class':'form-select form-control-lg',
                                          'id':"typeEmailX-2",
                                          'placeholder':'select'}),
                    'image':forms.FileInput(attrs={'class':'form-control form-control-lg',
                                          'id':"typeEmailX-2",
                                          }),
                    'short_description':forms.TextInput(attrs={'class':'form-control form-control-lg',
                                          'id':"typeEmailX-2",
                                          'placeholder':'short description'})
                    }
class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['user']

class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Username',
                               max_length=100,
                               widget=forms.TextInput(
                                   attrs={'class':'form-control form-control-lg',
                                          'id':"typeEmailX-2",
                                          'placeholder':'username'}
                               ))
    password = forms.CharField(label='Password',
                               max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'class':'form-control form-control-lg',
                                          'placeholder':'password'}
                               ))

class UserRegister(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control form-control-lg',
                                        'id': "typeEmailX-2",
                                        'placeholder': 'email'}
                             ))

    username = forms.CharField(label='Username',
                               max_length=100,
                               widget=forms.TextInput(
                                   attrs={'class':'form-control form-control-lg',
                                          'id':"typeEmailX-2",
                                          'placeholder':'username'}
                               ))
    password1 = forms.CharField(label='Password',
                               max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'class':'form-control form-control-lg',
                                          'placeholder':'password'}
                               ))

    password2 = forms.CharField(label='Repeat Password',
                               max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'class':'form-control form-control-lg',
                                          'placeholder':'password'}
                               ))


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'email', 'username']
        widgets = {'image':forms.FileInput(attrs={'class':'form-control form-control-lg',
                                          'id':"typeEmailX-2",
                                          })}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

class CustomPasswordReset(PasswordResetForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class':'form-control',
                                                            'id':'email'}))