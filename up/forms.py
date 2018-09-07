from django import forms
from .models import Barrage
class AddBarrage(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='Nom')
    BV = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='Bassin Versant')
    O = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='Oued')
    P = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='Province')
    T = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='Type de barrage')
    CP = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='Crue de projet')
    RN = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='RN')
    PHE = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='PHE')

class AddFile(forms.Form):
    fich = forms.FileField()
class datereg(forms.Form):
    start = forms.DateField()
    end = forms.DateField()

class AddTodo(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='Ajouter une Tache')
    date = forms.DateField()

class Addinst(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}),
                               label='Ajouter un instrument')
class SignUp(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='uername')
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='email')
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='password')
    firstname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='firstname')
    lastname = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='lastname')
    phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='phone')
    occup = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='occup')
    company = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}), label='company')
