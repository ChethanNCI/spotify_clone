import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from bs4 import BeautifulSoup as bs1
from django.contrib.auth.decorators import login_required
import requests
from django.contrib import messages
from .models import Subscription
from subscription_libnci import subscribe_user, unsubscribe_user

def top_artists():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/artists/top"

    headers = {
	        "x-rapidapi-key": "bfe779e111msh9d8c3f9891400d2p188405jsn02b3bf2266d8",
	        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    artists_info = []

    if 'artists' in response_data:
        shotrten_response_data = response_data['artists'][:7]

        for artist in shotrten_response_data:
            name = artist.get('name', 'No Name')
            avatar_url = artist.get('visuals', {}).get('avatar', [{}])[0].get('url', 'No URL')
            artist_id = artist.get('id', 'No ID')
            artists_info.append((name, avatar_url, artist_id))

    return artists_info

def top_tracks():
    url = "https://spotify-scraper.p.rapidapi.com/v1/chart/tracks/top"
    headers = {
	            "x-rapidapi-key": "bfe779e111msh9d8c3f9891400d2p188405jsn02b3bf2266d8",
	            "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
        }

    response = requests.get(url, headers=headers)
    data = response.json()
    track_details = []

    if 'tracks' in data:
        shortened_data = data['tracks'][:18]

        # id, name, artist, cover url 
        for track in shortened_data:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name'] if track['artists'] else None
            cover_url = track['album']['cover'][0]['url'] if track['album']['cover'] else None

            track_details.append({
                'id': track_id,
                'name': track_name,
                'artist': artist_name,
                'cover_url': cover_url
            })

    else:
        print("track not foun in response")

    return track_details

def audio_detail(query):
    url = "https://spotify-scraper.p.rapidapi.com/v1/track/download"

    querystring = {"track":query}

    headers = {
        "x-rapidapi-key": "bfe779e111msh9d8c3f9891400d2p188405jsn02b3bf2266d8",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    audio_song = []
    if response.status_code == 200:
        song_data = response.json()
        if 'youtubeVideo' in song_data and 'audio' in song_data['youtubeVideo']:
            song_list = song_data['youtubeVideo']['audio'] 
            song_url = song_list[0]['url']
            duration_text = song_list[0]['durationText']
            
            audio_song.append(song_url)
            audio_song.append(duration_text)
        else:
            print("No audio")
    else:
        print("No Youtube video")

    return audio_song




def music(request, pk):
     track_id = pk
     url = "https://spotify-scraper.p.rapidapi.com/v1/track/metadata"

     querystring = {"trackId": track_id}

     headers = {
	        "x-rapidapi-key": "bfe779e111msh9d8c3f9891400d2p188405jsn02b3bf2266d8",
	        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
     }

     response = requests.get(url, headers=headers, params=querystring)
     if response.status_code == 200:
        track_data = response.json()

        # Write Track name and Artist name in Music.html page
        
        track_name = track_data.get("name")
        artists_list = track_data.get("artists", [])
        first_artist_name = artists_list[0].get("name") if artists_list else "No artist found"
        audio_details_query = track_name + first_artist_name
        audio_details = audio_detail(audio_details_query)
        audio_url = audio_details[0]
        duration_text = audio_details[1]
        trackimage = track_image(track_id,track_name)

        

        context = {
            'track_name': track_name,
            'artist_name': first_artist_name,
            'audio_url': audio_url,
            'duration_text': duration_text,
            'trackimage': trackimage
            
        }
     
     return render(request, 'music.html', context)

def track_image(track_id, track_name):
    url = 'https://open.spotify.com/track/'+track_id
    r = requests.get(url)
    soup = bs1(r.content)
    image_links_html = soup.find('img', {'alt': track_name})
    if image_links_html:
        image_links = image_links_html['srcset']
    else:
        image_links = ''

    match = re.search(r'https:\/\/i\.scdn\.co\/image\/[a-zA-Z0-9]+ 640w', image_links)

    if match:
        url_640w = match.group().rstrip(' 640w')
    else:
        url_640w = ''

    return url_640w

def profile(request, pk):
    artist_id = pk

    url = "https://spotify-scraper.p.rapidapi.com/v1/artist/overview"

    querystring = {"artistId": artist_id}

    headers = {
        "x-rapidapi-key": "bfe779e111msh9d8c3f9891400d2p188405jsn02b3bf2266d8",
        "x-rapidapi-host": "spotify-scraper.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()

        name = data["name"]
        monthly_listeners = data["stats"]["monthlyListeners"]
        header_url = data["visuals"]["header"][0]["url"]

        top_tracks = []

        for track in data["discography"]["topTracks"]:
            trackid = str(track["id"])
            trackname = str(track["name"])
            if track_image(trackid, trackname):
                trackimage = track_image(trackid, trackname)
            else:
                trackimage = "https://imgv3.fotor.com/images/blog-richtext-image/music-of-the-spheres-album-cover.jpg"

            track_info = {
                "id": track["id"],
                "name": track["name"],
                "durationText": track["durationText"],
                "playCount": track["playCount"],
                "track_image": trackimage
            }

            top_tracks.append(track_info)

        artist_data = {
            "name": name,
            "monthlyListeners": monthly_listeners,
            "headerUrl": header_url,
            "topTracks": top_tracks,
        }
    else:
        artist_data = {}
    return render(request, 'profile.html', artist_data)

# Create your views here.
@login_required(login_url='login')
def index(request):
    artists_info = top_artists()
    top_track_list = top_tracks()

    # divide the list into three parts
    first_six_tracks = top_track_list[:6]
    second_six_tracks = top_track_list[6:12]
    third_six_tracks = top_track_list[12:18]

    context = {
        'artists_info' : artists_info,
        'first_six_tracks': first_six_tracks,
        'second_six_tracks': second_six_tracks,
        'third_six_tracks': third_six_tracks,
    }
    return render(request, 'index.html' , context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'User not Found or credential is Invalid')
            return redirect('login')
        
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
                if User.objects.filter(email=email).exists():
                     messages.info(request, 'Mail exists')
                     return redirect('signup')
                elif User.objects.filter(username=username).exists():
                     messages.info(request, 'Username exists')
                     return redirect('signup')
                else:
                     user = User.objects.create_user(username=username, email=email, password=password)
                     user.save()
                     
                     return redirect('login')

                     
                

                
        else:
                messages.info(request, 'Passsword not matches')
                return redirect('signup')

    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def subscription_page(request):
    """Renders the subscription page, or redirects to confirmation if already subscribed."""
    user = request.user
    # Check if user is already subscribed
    subscription = Subscription.objects.filter(user=user, is_subscribed=True).first()
    if subscription:
        # Redirect to confirmation page with already subscribed message
        return render(request, 'confirmation.html', {'message': "You are already subscribed."})
    # Otherwise, render the subscription page for payment details
    return render(request, 'subscription.html')

@login_required
def process_subscription(request):
    """Handles the subscription request and redirects to confirmation page with message."""
    user = request.user
    if request.method == 'POST':
        if subscribe_user(user):
            # Redirect to confirmation page with success message
            return render(request, 'confirmation.html', {'message': "You have successfully subscribed!"})
        else:
            # Redirect to confirmation page with already subscribed message
            return render(request, 'confirmation.html', {'message': "You are already subscribed."})

@login_required
def process_unsubscription(request):
    """Handles the unsubscription request and redirects to confirmation page with message."""
    user = request.user
    if request.method == 'POST':
        if unsubscribe_user(user):
            # Redirect to confirmation page with success message for unsubscription
            return render(request, 'confirmation.html', {'message': "You have successfully unsubscribed!"})
        else:
            # Redirect to confirmation page with error message if not subscribed
            return render(request, 'confirmation.html', {'message': "You are not currently subscribed."})