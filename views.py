from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import View, DetailView, FormView, ListView
from django.views.generic import CreateView
from django.contrib.auth import authenticate, logout, login

from KaiHostel3.forms import ArticleForm, UserForm, UserProfileForm, CommentForm
from KaiHostel3.models import Article, Comment


# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('KaiHostel3:all_article', kwargs={'page': 1}))


class Login(FormView):
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, "KaiHostel3/login.html", {'form': form})

    def post(self, request, *args, **kwargs):
        print('YES')
        form = UserForm(request.POST)
        if form.is_valid:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    print('NO')
                    login(request, user)
                    return HttpResponseRedirect(reverse('KaiHostel3:all_article', kwargs={'page': 1}))
                else:
                    print('Http response forbidden')
                    return HttpResponseForbidden('Your account is not active')
            else:
                print('BAD_CREDENTIALS')
                return render(request, "KaiHostel3/login.html", {'form': form})

        return render(request, "KaiHostel3/login.html", {'form': form})


class Logout(DetailView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('KaiHostel3:login', args=args, kwargs=kwargs))


class Register(FormView):
    is_registered = False

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            self.is_registered = True
            print('All done')
            return render(request, 'KaiHostel3/register.html', {'user_form': user_form,
                                                                'profile_form': profile_form,
                                                                'is_registered': self.is_registered})
        print("That's wrong")
        return render(request, 'KaiHostel3/register.html', {'user_form': user_form,
                                                            'profile_form': profile_form,
                                                            'is_registered': self.is_registered})


    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, 'KaiHostel3/register.html', {'user_form': user_form,
                                                            'profile_form': profile_form,
                                                            'is_registred': self.is_registered})


class AllArticle(ListView):
    model = Article
    paginate_by = 10
    template_name = 'KaiHostel3/all_article.html'

    context_object_name = 'article_list'


class GetArticle(DetailView):
    model = Article
    template_name = 'KaiHostel3/article.html'
    context_object_name = 'article'
    queryset = Article.objects.all()

    def get_object(self, queryset=None):
        object = get_object_or_404(self.queryset, id=self.kwargs['pk'])
        return object

    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs['pk'])
        form = CommentForm(initial={'article': article,
                                    'parent': None,
                                    })
        return render(request, 'KaiHostel3/article.html', {'article': article,
                                                           'form': form})


class AddArticle(ListView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.userprofile:
            form = ArticleForm()
            return render(request, "KaiHostel3/add_article.html", {'form': form})
        else:
            return HttpResponseRedirect(reverse('KaiHostel3:login'))


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.userprofile:
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.user_profile = request.user.userprofile
                article.save()
                for tag in form.cleaned_data['tags']:
                    article.tags.add(tag)
            return HttpResponseRedirect(reverse("KaiHostel3:all_article", kwargs={'page': 1}))
        return HttpResponse("You haven't permission")


class DeleteArticle(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():

            article_id = kwargs['article_id']
            article = get_object_or_404(Article, pk=article_id)

            if request.user.has_perm('KaiHostel3.delete_article'):

                if request.user.userprofile == article.user_profile:
                    print('Yes')
                    article.delete()
                else:
                    return HttpResponseForbidden("You are not the user who has created this article")
            else:
                return HttpResponseForbidden(
                    "You are owner of the one,but you have not permission to do that.Please,contact to administrator for extra information")

        else:
            return HttpResponseForbidden("You have not permission to do that")
        return HttpResponseRedirect(reverse("KaiHostel3:all_article", kwargs={'page': 1}))


class AllComment(ListView):
    def get(self, request, *args, **kwargs):
        error = False;
        if not request.user.is_authenticated() or request.user.is_staff:
            error = True
            return render(request, 'KaiHostel3/all_comment.html', {'error': error})
        list = Comment.objects.filter(owner=request.user.userprofile).order_by('pub_date')
        return render(request, 'KaiHostel3/all_comment.html', {'error': error,
                                                               'list': list})


class AddComment(CreateView):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, "KaiHostel3/add_comment.html", {'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid() and not form.cleaned_data['content'] == '':
            print('Yes')
            comment = form.save(commit=False)

            if request.user.is_authenticated():
                owner = request.user.userprofile
                print(owner)
                username = ''
            else:
                print('There is a error!')
                owner = None
                username = request.POST.get('username')
            comment.owner = owner
            comment.username = username
            comment.save()
            print('Saved')
            return HttpResponseRedirect(reverse('KaiHostel3:detail_article', kwargs={'pk': request.POST['article']}))
        print(form.errors)
        return render(request, "KaiHostel3/add_comment.html", {"form": form})

