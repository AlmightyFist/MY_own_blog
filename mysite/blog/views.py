from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import PostForm, EmailPostForm
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import send_mail


# Create your views here.
class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        posts = Post.objects.filter(status='published').order_by('-publish')
        return posts

"""def post_list(request):# wyświetla listę WSZYSTKICH postów
    object_list = Post.objects.filter(status='published')
    paginator = Paginator(object_list,3) # trzy posty na stronie
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page':page,'posts':posts} )"""

def main_site(request):
    return render(request, 'blog/main_site.html', {})

"""def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})"""

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


def post_new(request):
        if request.method == "POST":
            form= PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.publish = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)

        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    sent = False

    if request.method == 'POST':

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'],cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post':post, 'form':form, 'sent':sent})
