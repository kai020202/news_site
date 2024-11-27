from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    # ホーム画面：'home'ビューにアクセス
    path('', views.home, name='home'),  # ホーム画面。トップページに対応するURL。ニュースを取得して表示。

    # 掲示板ページ：'board'ビューにアクセス
    path('board/', views.board, name='board'),  # 掲示板ページの表示。掲示板に投稿された記事を一覧で表示。

    # 投稿作成ページ：'post_create'ビューにアクセス
    path('post_create/', views.post_create, name='post_create'),  # 新規投稿作成ページ。投稿フォームを表示し、新しい投稿を作成できる。

    # 投稿作成後のページ：'post_created'ビューにアクセス
    path('post_created/', views.post_created, name='post_created'),  # 投稿作成後に表示するページ。投稿が保存されたことを通知するページ。

    # 投稿詳細ページ：投稿IDによる詳細表示。'post_id'はURLパラメータとして渡される。
    path('post/<int:post_id>/', views.detail, name='detail'),  

    # マイページ：'mypage'ビューにアクセス。ログインユーザーの情報を表示。
    path('mypage/', views.mypage, name='mypage'),  

    # ログインページ：'login'ビューにアクセス
    path('login/', views.CustomLoginView.as_view(), name='login'),  # ログインページへのアクセス。ユーザーがログインするためのフォームを表示。

    # ログアウト：'logout'ビューにアクセス。ログアウト後はホーム画面へリダイレクト
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # ログアウト処理。ログアウト後にホームページにリダイレクト。

    # ユーザー登録ページ：'register'ビューにアクセス
    path('register/', views.register, name='register'),  # ユーザー登録ページ。新しいユーザーアカウントを作成するためのフォームを表示。

    # お問い合わせフォームページ：'contact'ビューにアクセス
    path('contact/', views.contact, name='contact'),  # お問い合わせフォーム。ユーザーが問い合わせを送信できるページ。

    # 検索結果ページ：'search_results'ビューにアクセス
    path('search/', views.search_results, name='search_results'),  # ニュース記事の検索結果を表示。ユーザーが指定した検索ワードに基づいて記事を表示。

    # ログアウト：'logout'ビューにアクセス。
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),  # 再度ログアウトのURLパターン。ログアウト後にトップページにリダイレクト。


]



