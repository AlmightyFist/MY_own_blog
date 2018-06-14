from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_list(request):# wyświetla listę WSZYSTKICH postów
    posts = Post.objects.filter(status='published')
    return render(request, 'blog/post_list.html', {'posts':posts} )

def main_site(request):
    return render(request, 'blog/main_site.html', {})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})
