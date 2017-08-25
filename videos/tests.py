from django.test import TestCase

from .models import Theme, Video, Thumb

class VideosTests(TestCase):
    def setUp(self):
        self.theme = Theme.objects.create(name='Games')
        self.video = Video.objects.create(title='God Of War III', date_uploaded='2017-02-01', views=100)
        self.video.themes.add(self.theme)
        self.thumb_like = Thumb.objects.create(is_positive=True, time='2017-02-01 05:20', video=self.video)
        self.thumb_unlike = Thumb.objects.create(is_positive=False, time='2017-02-01 05:27', video=self.video)

    def test_count_thumbs(self):
        self.assertEquals(2, self.video.thumbs.count())
