from django.shortcuts import render, get_object_or_404, redirect

from .utils import increment_view_count
from .models import Post
from .forms import PostForm, UserRegistrationForm, ContactForm, SearchForm
import requests
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# ホーム画面: ニュース取得
def home(request):
    view_count = increment_view_count()

    query = request.GET.get('query', '')  # デフォルトは空文字
    page = request.GET.get('page', 1)  # ページ番号を取得（デフォルトは1）

    try:
        page = int(page)  # ページ番号を整数に変換
    except ValueError:
        page = 1  # 無効なページ番号が渡された場合は1を使用

    NEWS_API_KEY = settings.NEWS_API_KEY
    url = f'https://newsapi.org/v2/everything?q=latest&language=jp&pageSize=100&apiKey={NEWS_API_KEY}'
    #このURLからニュースAPIのニュースを取得

    try:
        response = requests.get(url) #URLの内容を取得
        response.raise_for_status()  # HTTPエラーを検出
        data = response.json() #取得したURLをjson文字列をディクショナリに変換
        articles = data.get('articles', [])#データからニュース記事の情報だけ抽出

        if query: #検索ワードを含まれる記事を見つける
            articles = [
                article for article in articles 
                if (article.get('title') and query.lower() in article['title'].lower()) or
                   (article.get('description') and query.lower() in article['description'].lower())
            ]

        paginator = Paginator(articles, 100)  # 1ページに100件の記事を表示
        articles_page = paginator.get_page(page)

        return render(request, 'news/home.html', {
            'articles': articles_page,
            'query': query,
            'view_count': view_count,
        })

    except requests.exceptions.RequestException as e:
        return render(request, 'news/home.html', {
            'articles': [],
            'query': query,
            'error': f'ニュースの取得に失敗しました: {e}',
            'view_count': view_count,
        })

# 掲示板ページ
def board(request):
    posts = Post.objects.all()
    return render(request, 'news/board.html', {'posts': posts})

# 投稿作成ページ
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_created')
    else:
        form = PostForm()

    return render(request, 'news/post_create.html', {'form': form})

# 投稿作成後のページ
def post_created(request):
    return render(request, 'news/post_created.html')

# 投稿詳細ページ
def detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'news/detail.html', {'post': post})

# マイページ（ログイン必須）
@login_required
def mypage(request):
    return render(request, 'news/mypage.html')

# ユーザー登録
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'ユーザー登録が成功しました！ログインしてください。')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'news/register.html', {'form': form})

# ログインページ
class CustomLoginView(LoginView):
    template_name = 'news/login.html'

    def form_valid(self, form):
        messages.success(self.request, "ログインしました！")
        return super().form_valid(form)

# お問い合わせフォーム（ログイン必須）
@login_required
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                subject=f'お問い合わせ: {name}',
                message=message,
                from_email=email,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )

            messages.success(request, 'お問い合わせ内容を送信しました！')
            return redirect('home')

    else:
        form = ContactForm()

    return render(request, 'news/contact.html', {'form': form})

# 検索結果ページ
def search_results(request):
    query = request.GET.get('query', '')
    page = request.GET.get("page", 1)
    articles = []

    try:
        page = int(page)
    except ValueError:
        page = 1

    if query:
        url = f'https://newsapi.org/v2/everything?q={query}&language=jp&pageSize=12&page={page}&apiKey={settings.NEWS_API_KEY}'
    else:
        url = f'https://newsapi.org/v2/top-headlines?country=jp&pageSize=12&page={page}&apiKey={settings.NEWS_API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])

        paginator = Paginator(articles, 15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'news/search_results.html', {
            'articles': page_obj,
            'search_form': SearchForm(),
            'query': query,
            'page': page,
            'prev_page': page - 1,
            'next_page': page + 1,
        })

    except requests.exceptions.RequestException as e:
        return render(request, 'news/search_results.html', {'error': f'ニュース取得エラー: {e}'})
    
