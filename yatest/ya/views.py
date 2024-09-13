
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from .forms import LinkForm
from .config import HEADERS
import requests

BASE_URL = 'https://cloud-api.yandex.net/v1/disk'
params = {'type': 'dir',}

def index(request):
    if request.method == "POST":
        linkForm = LinkForm(request.POST)

        key = make_template_fragment_key("listfiles") 
        cache.delete(key) # Аннулирование кэша 

        if 'reset_token' in request.POST:  # Очистка полей
            linkForm = LinkForm()
            
        elif linkForm.is_valid():
            try:
                key = linkForm.cleaned_data['link']  # Получение ключа
                HEADERS['Authorization'] = f'OAuth {key}' # Добавление ключа в HEADERS
                
                """ Получение данных о папках и файлах на диске и о пользователе"""
                responseAllFiles = requests.get(f'{BASE_URL}/resources?path=%2F&limit=100', headers=HEADERS, params=params).json()
                responseUserDisk = requests.get(f'{BASE_URL}', headers=HEADERS, params=params).json()

                """ Конкретная выборка папок, файлов и имени пользователя """
                items = responseAllFiles["_embedded"]["items"]
                user = responseUserDisk["user"]["display_name"]

                return render(request, 'index.html', {"form": linkForm, "all_files": items, "username": user})
            except Exception as e:
                print(e)
    else:
        linkForm = LinkForm(request.POST)
    return render(request, 'index.html', {"form": linkForm})


# Скачивание конкретного файла
def downloadFile(request, path):
    if request.method == "GET":
        # Получение ссылки на скачивание
        linkDownload = requests.get(f'{BASE_URL}/resources/download?path={path}', headers=HEADERS, params=params).json()['href']
        return HttpResponseRedirect(linkDownload)
    