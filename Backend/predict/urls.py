from django.contrib import admin
from django.urls import path, include
from . import views


from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.predict1, name='predict1'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
