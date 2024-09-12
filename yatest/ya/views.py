
from django.shortcuts import redirect, render
from .forms import LinkForm
import requests

BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
params = {'type': 'dir',}

def index(request):
    if request.method == "POST":
        linkForm = LinkForm(request.POST)
        if linkForm.is_valid():
            try:
                key = linkForm.cleaned_data['link']
                headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {key}'}
                responseAllFiles = requests.get(f'{BASE_URL}/resources?path=%2F&limit=100', headers=headers, params=params).json()

                items = responseAllFiles["_embedded"]["items"]
                return render(request, 'index.html', {"form": linkForm, "all_files": items})
            except:
                print("Ошибка")
    else:
        linkForm = LinkForm(request.POST)
    return render(request, 'index.html', {"form": linkForm})
