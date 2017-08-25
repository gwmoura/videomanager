from datetime import datetime

from django.utils.timezone import now
from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=200)

    @classmethod
    def by_popularity(self):
        return sorted(self.objects.all(),  key=lambda m: m.popularity, reverse=True)

    @property
    def popularity(self):
        popularity = 0
        for video in self.videos.all():
            popularity += video.score

        return popularity

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=200)
    date_uploaded = models.DateTimeField()
    views = models.IntegerField(null=True, blank=True, default=0)
    themes = models.ManyToManyField(Theme, related_name='videos')
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')

    @property
    def score(self):
        """
        Score = views * TimeFactor * PositivityFactor
        """
        return self.views * self._time_factor() * self._positivity_factor()

    def good_comments(self):
        """
        GoodComments = positive_comments/(positive_comments+negative_comments)
        """
        positive_comments = self.comments.filter(is_positive=True).count()
        negative_comments = self.comments.filter(is_positive=False).count()
        try:
            return positive_comments/(positive_comments+negative_comments)
        except ZeroDivisionError:
            return 0

    def thumbs_up(self):
        """
        ThumbsUp = thumbs_up/(thumbs_up+thumbs_down)
        """
        thumbs_up = self.thumbs.filter(is_positive=True).count()
        thumbs_down = self.thumbs.filter(is_positive=False).count()
        try:
            return thumbs_up/(thumbs_up+thumbs_down)
        except ZeroDivisionError:
            return 0

    def _time_factor(self):
        """
        TimeFactor = max(0, 1 - (days_since_upload/365))
        """
        today = now()
        days_since_upload = (today - self.date_uploaded).days
        return max(0, 1 - (days_since_upload/365))

    def _positivity_factor(self):
        """
        PositivityFactor = 0.7 * GoodComments + 0.3 * ThumbsUp
        """
        return 0.7 * self.good_comments() + 0.3 * self.thumbs_up()

    def __str__(self):
        return self.title

class ThumbsUpManager(models.Manager):
    def get_queryset(self):
        return super(ThumbsUpManager, self).get_queryset().filter(is_positive=True)

class ThumbsDownManager(models.Manager):
    def get_queryset(self):
        return super(ThumbsDownManager, self).get_queryset().filter(is_positive=False)

class Thumb(models.Model):
    is_positive = models.BooleanField()
    time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='thumbs')

    up_objects = ThumbsUpManager()
    down_objects = ThumbsDownManager()

    def __str__(self):
        return "%s - %i" % (self.video.title, self.is_positive)

class CommentsPositiveManager(models.Manager):
    def get_queryset(self):
        return super(CommentsPositiveManager, self).get_queryset().filter(is_positive=True)

class CommentsNegativeManager(models.Manager):
    def get_queryset(self):
        return super(CommentsNegativeManager, self).get_queryset().filter(is_positive=False)

class Comment(models.Model):
    text = models.TextField()
    is_positive = models.BooleanField()
    time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')

    positive_objects = CommentsPositiveManager()
    negative_objects = CommentsNegativeManager()

    def __str__(self):
        return self.text
