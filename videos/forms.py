import os.path, time

from django.utils.timezone import now
from django import forms

from .models import Video, Comment, Thumb

class VideoForm(forms.ModelForm):
    def clean_date_uploaded(self):
        date_uploaded = self.cleaned_data['date_uploaded']
        today = now()
        delta = today - date_uploaded
        if delta.days > 365:
            raise forms.ValidationError("Your video has more than 1 year!")
        return date_uploaded

    class Meta:
        model = Video
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('time',)

class ThumbForm(forms.ModelForm):
    class Meta:
        model = Thumb
        exclude = ('time',)
