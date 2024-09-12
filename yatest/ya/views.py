
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import LinkForm
from .config import HEADERS
import requests

BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
params = {'type': 'dir',}

def index(request):
    if request.method == "POST":
        linkForm = LinkForm(request.POST)
        if 'reset_token' in request.POST:
            linkForm.fields['link'].initial = ''
        elif linkForm.is_valid():
            try:
                key = linkForm.cleaned_data['link']
                HEADERS['Authorization'] = f'OAuth {key}'

                responseAllFiles = requests.get(f'{BASE_URL}/resources?path=%2F&limit=100', headers=HEADERS, params=params).json()
                responseUserDisk = requests.get(f'{BASE_URL}', headers=HEADERS, params=params).json()

                items = responseAllFiles["_embedded"]["items"]
                user = responseUserDisk["user"]["display_name"]

                return render(request, 'index.html', {"form": linkForm, "all_files": items, "username": user})
            except Exception as e:
                print(e)
    else:
        linkForm = LinkForm(request.POST)
    return render(request, 'index.html', {"form": linkForm})


def downloadFile(request, path):
    if request.method == "GET":
        linkDownload = requests.get(f'{BASE_URL}/resources/download?path={path}', headers=HEADERS, params=params).json()['href']
        return HttpResponseRedirect(linkDownload)
    