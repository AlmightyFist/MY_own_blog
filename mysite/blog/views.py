from django.shortcuts import render, get_object_or_404
from .models import Post, Score, Comment
from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import PostForm, EmailPostForm, CommentForm
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Avg


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

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(PostComment__id =pk)
    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments})

"""class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'"""

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
    comments = Comment.objects.filter(PostComment__id =pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments} )
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post':post})

def vote(request,pk):
    PostScore = get_object_or_404(Post, pk = pk)
    try:
        Score.objects.create(PostScore = PostScore, value =int(request.POST['score']) )# Tworzenie instancji modelu Score, request.POST pobiera dane przekazane przez "value" input
    except (KeyError, Score.DoesNotExist):
        return render(request, 'blog/post_detail.html', {'post':PostScore, 'error_message':" Proszę zaznaczyć ocenę postu"})

    PostScore.avr_score  = PostScore.score_set.all().aggregate(Avg('value'))['value__avg'] #wyszukuje średnią wszystkich ocen dla postu
    score_number = Score.objects.filter(PostScore__id =pk).count() # Zlicza sumę Score dla danego Post

    PostScore.save() #zaktualizowanie średniej punktów po każdym wywowałniu oceny
    comments = Comment.objects.filter(PostComment__id =pk)
    return render(request, 'blog/post_detail.html', {'post':PostScore, 'inf_message':"Dziękuję za Twój głos!", 'scores':PostScore.avr_score, 'score_number':score_number, 'comments':comments})



def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    sent = False

    if request.method == 'POST':

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri()
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'],cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post':post, 'form':form, 'sent':sent})

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(PostComment__id =pk)
    if request.method == "POST":
        form = CommentForm(data = request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.PostComment = post
            comment.author = request.user
            comment.publish = timezone.now()
            comment.save()
            return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments} )

    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form':form, 'post':post})
