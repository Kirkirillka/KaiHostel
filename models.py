from django.db import models
from django.contrib.auth.models import User,AnonymousUser
from django.utils import timezone
# Create your models here.


class UserProfile(models.Model):
    user=models.OneToOneField(User)
    website=models.URLField(blank=True,default='')
    photo=models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        if self.user:
             return self.user.username
        else:
            return ''

class Tags(models.Model):
    title=models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Comment(models.Model):
    owner=models.ForeignKey(UserProfile,default=None,null=True,unique=False)
    article=models.ForeignKey('Article',on_delete=models.CASCADE,unique=False,default=None)
    content=models.TextField(max_length=300,default='',unique=False,blank=True)
    pub_date=models.DateTimeField(default=timezone.now)
    parent=models.ForeignKey('self',default=None,null=True,blank=True,unique=False)

    username=models.CharField(max_length=100,default='',blank=True,unique=False)

    def __str__(self):
        if self.owner:
            return self.owner.__str__()
        else:
            return 'By anonyomous: {0}'.format(self.username)

    def get_root_comment(self,comment=None):
        pass

class Article(models.Model):
    article=models.CharField(max_length=200,default='')
    user_profile=models.ForeignKey(UserProfile,unique=False,default=None)
    pub_date=models.DateTimeField(default=timezone.now)
    content=models.TextField(default='')
    tags=models.ManyToManyField(Tags,
                           default=None,
                           blank=True,
                           )

    def __str__(self):
        return self.article

    def get_short_description(self):
        if self.content.__len__()>400:
            return self.content[:400]+'...'
        else:
            return self.content


    class Meta:
        ordering=['-pub_date']

