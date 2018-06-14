from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_list(request):# wyświetla listę WSZYSTKICH postów
    posts = Post.objects.filter(status='published').order_by('-publish')
    return render(request, 'blog/post_list.html', {'posts':posts} )
