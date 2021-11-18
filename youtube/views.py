from django.shortcuts import render, HttpResponse , redirect , HttpResponseRedirect
from pytube import YouTube
import os
import re
from pathlib import Path
from pytube import Playlist
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, "index.html")


def get_video(request):
    global url
    global playlist_url
    url = request.GET.get("url")
    get_type = request.GET.get("type")

    videp = []
    audio = []
    playlist = []

    if get_type == "video" or get_type == "mp3":
        try:     
            regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"
            embed_link = re.sub(regex, r"https://www.youtube.com/embed/\1", url)
            
            try:
                y_video = YouTube(url)
            except:
                messages.warning(request, "Something went wrong , Please check URL or choose right option")
                return redirect('/')

            
            title = y_video.title
            video = y_video.streams.filter(progressive=True).all()
            audio = y_video.streams.filter(only_audio=True).all()
            playlist = Playlist(url)
            
            if get_type == "mp3":
                data = {
                    'title': title,
                    'embed_link': embed_link,
                    'audio': audio,
                }
                return render(request, "result.html", data)

            elif get_type == "video":
                data = {
                    'title': title,
                    'video': video,
                    'embed_link': embed_link,
                }
                return render(request, "result.html", data)
        except:
            messages.warning(request, "Something went wrong , Please check URL or choose right option")
            return redirect('/')
    elif get_type == "playlist":
        try:
            playlist_url = url
            playlist = Playlist(playlist_url)
            download_path = str(Path.home() / "Downloads")
            playlist_folder = playlist.title
            new_path = os.path.join(download_path , playlist_folder)
            counter = 0
            if os.path.exists(new_path):
                playlist_folder = playlist_folder + " (" + str(counter) + ")"
                new_path = os.path.join(download_path , playlist_folder)
                os.mkdir(new_path)
                counter += 1
            for video in playlist.videos:
                video.streams.get_highest_resolution().download(new_path)
                print("downloading"+ str(counter))
                counter += 1 
            messages.warning(request, "Something went wrong , Enter the currect URL")
            return redirect('/')
        except:
            messages.warning(request, "Something went wrong , Enter the currect playlist URL")
            return redirect('/')
    
        


def download_view(request):
    global url
    download_path = str(Path.home() / "Downloads")
    if request.method == "POST":
        get_type = request.POST.get("type")
        get_itag = request.POST.get("itag")
        import pdb; pdb.set_trace()
        if get_type == "video":
            YouTube(url).streams.get_by_itag(get_itag).download(output_path=download_path)
            
            messages.success(request, "Download Successfull")
            return redirect('/')

        elif get_type == "audio":
            download = YouTube(url).streams.get_by_itag(get_itag).download(output_path=download_path)
            base, ext = os.path.splitext(download)
            new_file = base + '.mp3'
            os.rename(download, new_file)
            messages.success(request, "Download Successfull")
            return redirect('/')
        messages.warning(request, "Something went wrong , Enter the currect URL")
        return redirect('/')
