from django.db import models

# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    oner = models.BooleanField()
    speechiness = models.IntegerField()
    liveness = models.IntegerField()
    acousticness = models.IntegerField()
    energy = models.IntegerField()
    valence = models.IntegerField()
    danceability = models.IntegerField()
    mode = models.CharField(max_length=10)
    key = models.CharField(max_length=10)
    bpm = models.IntegerField()
    instrumentalness = models.IntegerField()
    release_date = models.DateField()

    def __str__(self):
        return self.name

class Artist(models.Model):
    id = models.AutoField(primary_key=True)
    feature = models.ForeignKey('Feature', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    feature = models.ForeignKey('Feature', on_delete=models.CASCADE)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name