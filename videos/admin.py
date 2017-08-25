from django.conf.urls import url
from django.contrib import admin
from django.template.response import TemplateResponse

from .models import Theme, Video, Comment, Thumb
from .forms import VideoForm, CommentForm, ThumbForm

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'popularity')
    list_filter = ('name',)

admin.site.register(Theme, ThemeAdmin)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    form = CommentForm

class ThumbInline(admin.TabularInline):
    model = Thumb
    extra = 0
    form = ThumbForm

class VideoAdmin(admin.ModelAdmin):
    form = VideoForm
    inlines = (ThumbInline, CommentInline)
    list_display = ('title', 'views', 'date_uploaded',  'score', 'thumbs_up', 'good_comments')
    list_filter = ('views', 'date_uploaded')

    def get_urls(self):
        urls = super(VideoAdmin, self).get_urls()
        video_urls = [
            url(r'^popular-themes/$', self.popular_themes_view, name='get_popular_themes')
        ]
        return video_urls + urls

    def popular_themes_view(self, request):
        themes = Theme.by_popularity()
        opts = self.model._meta
        app_label = opts.app_label
        context = dict(
            self.admin_site.each_context(request),
            themes = themes,
            opts = opts,
            app_label = opts.app_label
        )
        return TemplateResponse(request, "videos/popular_themes.html", context)

admin.site.register(Video, VideoAdmin)
