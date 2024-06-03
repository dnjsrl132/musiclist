import csv
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from django.db.models import Avg
from search.forms import *
from search.models import *

def hello_world(request):
    return HttpResponse('Hello world!')

class SearchView(TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            results = []
            features = Feature.objects.filter(name__icontains=query)
            for feature in features:
                if feature.oner:
                    results.append({'artist': feature.name, 'feature': feature})
                else:
                    song = Song.objects.filter(feature=feature).first()
                    if song:
                        results.append({'artist': song.artist.name, 'feature': feature})
            context['results'] = results
        context['query'] = query
        return context

class SongView(ListView):
    model = Song
    template_name = 'song_list.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        artist_name = self.kwargs['artist_name']
        artist = Artist.objects.get(name=artist_name)
        songs = Song.objects.filter(artist=artist)
        queryset = []
        for song in songs:
            song_data = {
                'song': song,
                'artist': artist,
                'feature': {
                    'speechiness': song.feature.speechiness,
                    'liveness': song.feature.liveness,
                    'acousticness': song.feature.acousticness,
                    'energy': song.feature.energy,
                    'valence': song.feature.valence,
                    'danceability': song.feature.danceability,
                    'mode': song.feature.mode,
                    'key': song.feature.key,
                    'bpm': song.feature.bpm,
                }
            }
            queryset.append(song_data)

        return queryset


def add_feature(request):
    if request.method == 'POST':
        form = FeatureForm(request.POST)
        if form.is_valid():
            feature = form.save(commit=False)

            artist = form.cleaned_data['artist']
            if not form.cleaned_data['oner']:
                feature.save()
                artist_model = Artist.objects.filter(name=artist).first()
                if not artist_model:
                    artist_model, created = Artist.objects.get_or_create(name=artist, feature=feature)
                song = Song.objects.create(name=feature.name, feature=feature,artist=artist_model)
            else:
                feature.save()
                artist_model, created = Artist.objects.get_or_create(name=feature.name, feature=feature)
            return redirect('search:search')
    else:
        form = FeatureForm()
    return render(request, 'add_feature.html', {'form': form})


def dele(request):
    artists = Feature.objects.all()  # 객체를 가져올 때 .objects.all()을 사용합니다.
    for artist in artists:
        artist.delete()
    return redirect('search:search')

def match(request):
    artists = Artist.objects.all()
    for artist in artists:
        average_features = Song.objects.filter(artist=artist).aggregate(
            average_speechiness=Avg('feature__speechiness'),
            average_liveness=Avg('feature__liveness'),
            average_acousticness=Avg('feature__acousticness'),
            average_energy=Avg('feature__energy'),
            average_valence=Avg('feature__valence'),
            average_danceability=Avg('feature__danceability'),
            average_bpm=Avg('feature__bpm'),
        )
        artist.feature.speechiness = average_features['average_speechiness']
        artist.feature.liveness = average_features['average_liveness']
        artist.feature.acousticness = average_features['average_acousticness']
        artist.feature.energy = average_features['average_energy']
        artist.feature.valence = average_features['average_valence']
        artist.feature.danceability = average_features['average_danceability']
        artist.feature.bpm = average_features['average_bpm']
        artist.save()
    return redirect('search:search')

def add_new(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_data = TextIOWrapper(file, encoding='utf-8')
            reader = csv.DictReader(file_data)

            for row in reader:
                name = row['track_name']
                new_feature = Feature.objects.filter(name=name)
                if new_feature:
                    continue
                feature = Feature.objects.create(
                    name = row['track_name'],
                    oner = False,
                    speechiness = row['speechiness_%'],
                    liveness = row['liveness_%'],
                    acousticness = row['acousticness_%'],
                    energy = row['energy_%'],
                    valence = row['valence_%'],
                    danceability = row['danceability_%'],
                    mode = row['mode'],
                    bpm = row['bpm'],
                    key = row['key']
                )
                artist = row['artist(s)_name']
                artist_model = Artist.objects.filter(name=artist).first()
                if not artist_model:
                    artist_model, created = Artist.objects.get_or_create(name=artist, feature=feature)
                song = Song.objects.create(name=feature.name, feature=feature, artist=artist_model)
            return redirect('search:search')
    else :
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})