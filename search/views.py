import csv
from datetime import date
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import *
from django.db.models import Avg
from search.forms import *
from search.models import *

#검색 결과
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

#특정 가수 눌렀을 때 곡 리스트
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
                    'speechiness': int(song.feature.speechiness),
                    'liveness': int(song.feature.liveness),
                    'acousticness': int(song.feature.acousticness),
                    'energy': int(song.feature.energy),
                    'valence': int(song.feature.valence),
                    'danceability': int(song.feature.danceability),
                    'mode': song.feature.mode,
                    'key': song.feature.key,
                    'bpm': song.feature.bpm,
                    'instrumentalness': song.feature.instrumentalness
                }
            }
            queryset.append(song_data)
        return queryset
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist_name = self.kwargs['artist_name']
        artist = Artist.objects.get(name=artist_name)
        artist_features = {
            'speechiness': int(artist.feature.speechiness),
            'liveness': int(artist.feature.liveness),
            'acousticness': int(artist.feature.acousticness),
            'energy': int(artist.feature.energy),
            'valence': int(artist.feature.valence),
            'danceability': int(artist.feature.danceability),
            'bpm': artist.feature.bpm,
            'instrumentalness' : artist.feature.instrumentalness
        }
        context['artist'] = {
            'name': artist.name,
            'feature': artist_features
        }
        return context


#유사 아티스트 추천
class SimilarArtistsView(View):
    def get(self, request, feature, name):
        artist = Artist.objects.get(name=name)
        value = getattr(artist.feature, feature)
        all_artists = Feature.objects.filter(oner=True)
        similarities = []
        for artist in all_artists:
            similarity = abs(value - getattr(artist, feature))
            similarities.append((artist, similarity))

        similarities.sort(key=lambda x: x[1])

        top_10_artists = [artist for artist, _ in similarities[:10]]
        similar = []
        for artist in top_10_artists:
            temp_artist = Artist.objects.filter(name=artist)[0]
            similar.append(temp_artist)

        return render(request, 'similar_artists.html',
                      {'feature': feature, 'value': value, 'similar_artists': similar, 'artist': name})


#DB 삭제
def dele(request):
    artists = Feature.objects.all()
    for artist in artists:
        artist.delete()
    artists = Song.objects.all()
    for artist in artists:
        artist.delete()
    artists = Artist.objects.all()
    for artist in artists:
        artist.delete()
    return redirect('search:search')

#가수 평균 구하기
def match(request):
    artists = Artist.objects.all()
    for artist in artists:
        feature = Feature.objects.filter(name=artist.name).first()
        average_features = Song.objects.filter(artist=artist).aggregate(
            average_speechiness=Avg('feature__speechiness'),
            average_liveness=Avg('feature__liveness'),
            average_acousticness=Avg('feature__acousticness'),
            average_energy=Avg('feature__energy'),
            average_valence=Avg('feature__valence'),
            average_danceability=Avg('feature__danceability'),
            average_bpm=Avg('feature__bpm'),
            average_instrumentalness=Avg('feature__instrumentalness'),
        )
        feature.oner = True
        feature.speechiness = average_features['average_speechiness']
        feature.liveness = average_features['average_liveness']
        feature.acousticness = average_features['average_acousticness']
        feature.energy = average_features['average_energy']
        feature.valence = average_features['average_valence']
        feature.danceability = average_features['average_danceability']
        feature.bpm = average_features['average_bpm']
        feature.instrumentalness = average_features['average_instrumentalness']
        feature.save()
        artist.feature = feature
        artist.save()
        print(artist.feature.key)
    return redirect('search:search')

#csv 파일 입력
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
                release_date = date(int(row['released_year']), int(row['released_month']), int(row['released_day']))
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
                    key = row['key'],
                    instrumentalness = row['instrumentalness_%'],
                    release_date=release_date
                )
                artist = row['artist(s)_name']
                artist_model = Artist.objects.filter(name=artist).first()
                if not artist_model:
                    artist_feature, created = Feature.objects.get_or_create(
                        name = artist,
                        oner = True,
                        speechiness = row['speechiness_%'],
                        liveness = row['liveness_%'],
                        acousticness = row['acousticness_%'],
                        energy = row['energy_%'],
                        valence = row['valence_%'],
                        danceability = row['danceability_%'],
                        mode = row['mode'],
                        bpm = row['bpm'],
                        key = row['key'],
                        instrumentalness = row['instrumentalness_%'],
                        release_date = release_date
                    )
                    artist_model, created = Artist.objects.get_or_create(name=artist, feature=artist_feature)
                song = Song.objects.create(name=feature.name, feature=feature, artist=artist_model)
            return redirect('search:search')
    else :
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})