from django.shortcuts import render, get_object_or_404
from .models import Post, Score, Comment, Category
from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import PostForm, EmailPostForm, CommentForm, UserRegistrationForm
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Avg
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required


# Create your views here.
"""class PostListView(ListView):
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        posts = Post.objects.filter(status='published').order_by('-publish')
        return posts"""

def post_list(request, tag_slug = None):# wyświetla listę WSZYSTKICH postów
    object_list = Post.objects.filter(status='published').order_by('-publish') #Queryset, wybiera OPUBLIKOWANE POSTY
    page = request.GET.get('page') #Potrzebne do funkcji PAGINATOR
    tag = None

    if tag_slug: #if działajace jeżeli z URL przekazywany jest TAG
        tag = get_object_or_404(Tag, slug=tag_slug) #pobiera odpowiedni obiekt modelu TAG z modułu TAGGIT
        object_list = object_list.filter(tags__in=[tag]) #filtruje wygenerowany QUeryset na podstawie przesłanego TAGu

    paginator = Paginator(object_list,3) # trzy posty na stronie, na podstawie wygenerowanego Querysetu
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'page':page,'posts':posts, 'tag': tag} )

def main_site(request):


    return render(request, 'blog/main_site.html', {})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) #Pobiera objekt posta na podstawie pobranego ID
    comments = Comment.objects.filter(PostComment__id =pk) # Tworzy Queryset komentarzy do pobranego posta

    post_tags_ids = post.tags.values_list('id', flat = True) #pobranie listy Pythona zawierającej identyfikatory dla tagów bieżącego posta. Wartością zwrotną są krotki z wartościami pochodzącymi z danych pól. Przy użyciu flat = True output wygląda tak: [1, 2, 3,...]
    similar_posts = Post.objects.filter(status='published')
    similar_posts = similar_posts.filter(tags__in = post_tags_ids).exclude(id=post.id) # pobranie wszystkich postów zawierajacy dowolny z otrzymanych wcześniej tagów z wyłączeniem bieżącego posta
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4] #funkcja agregacji Count() generuje pole same_tags, zawierające listę tagów współdzielonych ze wszystkimi sprawzanymi tagami. WYniki ułożone w kolejności współdzielonych tagów oraz względem dany opublikowania. Pobieramy jedynie 4 pierwsze posty.
    return render(request, 'blog/post_detail.html', {'post':post, 'comments':comments, 'similar_posts': similar_posts })

"""class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'"""

def post_new(request):
        if request.method == "POST": #Jeżeli formularz został uzupełniony i przesłany za pomocą metody POST, nastepuje wykonanie IF
            form= PostForm(request.POST) #tworzy formularz z danymi pobranymi za pomocą metody POST
            if form.is_valid(): # wykonane jeżeli formualrz jest uzupełniony prawidłowo
                post = form.save(commit=False)
                post.author = request.user #pobranie danych aktualnie zalogowanego użytkownika
                post.publish = timezone.now()
                post.status = 'published'
                post.save()
                return redirect('post_detail', pk=post.pk)

        else: # jeżeli widok jest wywołany bez funkcji POST utworzony zostaje pusty formularz
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
    PostScore = get_object_or_404(Post, pk = pk)# pobranie obiektu POST na podstawie przesłanego ID
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

def add_comment(request, pk): #dodawanie komantarza do POSTu
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

def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = category.post_set.all().order_by('-publish')

    return render (request, 'blog/category_posts.html', {'posts': posts})

#Rejestracja nowego użytkownika

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Utworzenie nowego obiektu użytkownika, bez zapisywania jeszcze w bazie oddanych
            new_user = user_form.save(commit = False)
            #Ustawienie wybranego hasła
            new_user.set_password(user_form.cleaned_data['password']) #specjalna metoda szyfrująca hasło użytkownika
            #Zapisanie obiektu user
            new_user.save()
            return render(request, 'blog/register_done.html',{'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form':user_form})
