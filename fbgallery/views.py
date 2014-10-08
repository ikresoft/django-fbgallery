import urllib2
import django.utils.simplejson as json
from django.shortcuts import render_to_response
from django.template import RequestContext, defaultfilters
from django.core.cache import cache

from django.conf import settings

graph_url = 'https://graph.facebook.com'
albums_url = '%s/%s/albums?fields=id,name,cover_photo&limit=10000' % (graph_url, settings.FB_PAGE_ID)
cache_expires = getattr(settings, 'CACHE_EXPIRES', 30)


def get_graph_result(url):
    cachename = 'fbgallery_cache_' + defaultfilters.slugify(url)
    data = None
    if cache_expires > 0:
        data = cache.get(cachename)
    if data is None:
        f = urllib2.urlopen(urllib2.Request(url))
        response = f.read()
        f.close()
        data = json.loads(response)
        if cache_expires > 0:
            cache.set(cachename, data, cache_expires*60)
    return data


def display_albums(request, fb_id):
    albums = get_graph_result(albums_url)["data"]
    for i in range(len(albums)):
        album = albums[i]
        cover_photo_url = "%s/%s/picture" % (graph_url, album["id"])
        album["src"] = cover_photo_url
    data = RequestContext(request, {
        'albums': albums,
    })

    return render_to_response('fbgallery/albums.html', context_instance=data)


def display_album(request, album_id, fb_id):
    album = get_graph_result("%s/%s" % (graph_url, album_id))
    photos_url = "%s/%s/photos" % (graph_url, album_id)
    photos = get_graph_result(photos_url)["data"]

    data = RequestContext(request, {
        'album': album,
        'photos': photos,
    })
    return render_to_response('fbgallery/album.html', context_instance=data)


def return_album(album_id, limit=16):
    album = get_graph_result("%s/%s" % (graph_url, album_id))
    photos_url = "%s/%s/photos" % (graph_url, album_id)
    photos = get_graph_result(photos_url)["data"][:limit]

    data = {
        'album': album,
        'photos': photos,
    }
    return data
