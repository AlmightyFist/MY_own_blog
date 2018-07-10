from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

from ..models import Post
@register.simple_tag
def total_posts():
    return Post.objects.filter(status='published').count()

@register.inclusion_tag('blog/latest_posts.html') #wraz ze zwróconymi wartosciami wygenerowany ma zostaćszablon latest_posts.html
def show_latest_posts(count=5): #parametr count możemy być zmieniany podczas wywoływania szablonu
    latest_posts = Post.objects.filter(status='published').order_by('-publish')[:count]
    return {'latest_posts':latest_posts} #funkcja zwraca słownik zmiennych zamiast zwykłej wartości

@register.inclusion_tag('blog/highest_scores.html')
def highest_scores(count=5):
    highest_scores = Post.objects.order_by('-avr_score')[:count]
    return {'highest_scores':highest_scores}

@register.filter(name='markdown') #customowy fiiltr tekstu w HTMLu
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
