from django.conf.urls import *
# from django.conf import settings

# fb_id = getattr(settings, 'FB_PAGE_ID', None)

urlpatterns = patterns('fbgallery.views',
    url(r'^$', 'display_albums', name='fb-albums'),
    url(r'^(?P<album_id>[-\w]+)/$', 'display_album', name='fb-album'),
)
