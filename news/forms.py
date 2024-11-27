from django import forms
from .models import Post
from django.contrib.auth.models import User
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('パスワードが一致しません')

        return cleaned_data
    
    from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='名前', max_length=100, required=True)
    email = forms.EmailField(label='メールアドレス', required=True)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea, required=True)

class SearchForm(forms.Form):
    query = forms.CharField(label='検索', max_length=100, required=False)

    
class ContactForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=100) #名前の入力　１００文字まで
    email = forms.EmailField(label='メールアドレス') #メールアドレス入力
    message = forms.CharField(label='お問い合わせ内容', widget=forms.Textarea) #内容の入力
