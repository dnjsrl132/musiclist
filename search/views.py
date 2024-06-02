from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import *
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


def match(request):
    artists = Feature.objects.all()  # 객체를 가져올 때 .objects.all()을 사용합니다.
    for artist in artists:
        artist.delete()
    return redirect('search:search')