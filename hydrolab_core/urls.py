from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hydrolab.urls')), # Подключаем наше приложение
    path('accounts/', include('django.contrib.auth.urls')), # Стандартная авторизация (вход/выход)
]