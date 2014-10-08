from django import template
from fbgallery.views import return_album

register = template.Library()


@register.inclusion_tag('fbgallery/templatetags/small_photos.html')
def timeline_photos():
    return return_album('191210974230781')
