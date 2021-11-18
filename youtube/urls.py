from django.urls import path , include
from .views import *

app_name = 'yt_download'

urlpatterns = [
    path('', index , name="index" ),
    path('result/', get_video , name="get_video" ),
    path('download/', download_view , name="download" ),
]