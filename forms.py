from django import forms

from django.contrib.auth.models import User

from KaiHostel3.models import UserProfile, Article, Comment


__author__ = 'kirill'


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ('user_profile',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    article = forms.ModelChoiceField(Article.objects.all(), widget=forms.HiddenInput)
    parent = forms.ModelChoiceField(Comment.objects.all() or None, widget=forms.MultipleHiddenInput, required=False)
    username = forms.CharField(max_length=100, required=False)
    class Meta:
        model = Comment
        fields = ('article', 'content', 'parent', 'username')
        exclude = ['owner', 'pub_date', ]