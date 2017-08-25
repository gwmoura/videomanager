from django.utils.timezone import now
from django.test import TestCase

from .models import Theme, Video, Thumb

class VideosTests(TestCase):
    def setUp(self):
        self.theme = Theme.objects.create(name='Games')
        self.video = Video.objects.create(title='God Of War III', date_uploaded=now(), views=100)
        self.video.themes.add(self.theme)
        self.thumb_like = Thumb.objects.create(is_positive=True, time=now(), video=self.video)
        self.thumb_unlike = Thumb.objects.create(is_positive=False, time=now(), video=self.video)

    def test_count_thumbs(self):
        self.assertEquals(2, self.video.thumbs.count())
        self.assertEquals(0, self.video.comments.count())
        self.assertEquals(15.0, self.video.score)
