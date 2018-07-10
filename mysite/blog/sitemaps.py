from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly' #częstotliwość zmian stron posta
    priority = 0.9 # związek z witryną internetową, max = 1

    def items(self): #zwraca kolekcję Queryset obiektów mających znaleźć sięw tworzonej witrynie
        return Post.objects.filter(status='published').all()

    def lastmod(self, obj):
        return obj.publish
