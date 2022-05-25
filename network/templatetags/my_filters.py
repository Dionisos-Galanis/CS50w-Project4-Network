from django import template

register = template.Library()

@register.filter
def is_like_post(post, user):
    from ..models import Like
    try:
        Like.objects.get(user=user, post=post)
        return True
    except:
        return False
