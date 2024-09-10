from django import forms

class LinkForm(forms.Form):
    link = forms.CharField(label='Ссылка на Яндекс Диск:', max_length=500)
