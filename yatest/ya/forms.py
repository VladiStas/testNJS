from django import forms

class LinkForm(forms.Form):
    link = forms.CharField(label='Укажите ключ:', max_length=500)
