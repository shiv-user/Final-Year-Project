from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from account.models import User,Temp,Visitor_perma
# from .models import Temp,Visitor_perma

class RecepSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    def __init__(self, *args, **kwargs):
        super(RecepSignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email','password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_recep = True
        user.save()
        return user

class AdminSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    def __init__(self, *args, **kwargs):
        super(AdminSignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email','password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_admin = True
        user.save()
        return user

class VisitorForm(forms.ModelForm):
	class Meta:
		fields = ['name', 'pincode','uid','dob','address','purpose','gender']
		model = Temp


class FilterForm(forms.ModelForm):
	class Meta:
		model = Visitor_perma
		fields = ['name', 'pincode','date','uid','dob','address','purpose','phone','whoto']


# class FilterForm(forms.ModelForm):
#     class Meta:
#         model = Visitor_perma
#         fields = ['name','uid','gender','address','purpose','pincode']
