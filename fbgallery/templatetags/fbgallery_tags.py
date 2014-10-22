from django import template
from fbgallery.views import return_album, get_latest_album

register = template.Library()


@register.inclusion_tag('fbgallery/templatetags/small_photos.html')
def timeline_photos():
    try:
        return return_album('191210974230781')
    except:
        pass


@register.inclusion_tag('fbgallery/templatetags/latest_album.html')
def latest_album():
    return get_latest_album()
