from django import forms

class LinkForm(forms.Form):
    link = forms.CharField(label='Ссылка на ключ:', max_length=500)
