from django import template
from rest_adv.models import Review,UserProfile

register = template.Library()

@register.inclusion_tag('rest_adv/show_review.html')
def show_review(rev):
    return {'review': rev,
            'user':rev.user}