from django import forms
from .models import Feature

class FeatureForm(forms.ModelForm):
    artist = forms.CharField()  # oner 필드를 문자열 형태로 받음

    class Meta:
        model = Feature
        fields = '__all__'

class UploadFileForm(forms.Form):
    file = forms.FileField()