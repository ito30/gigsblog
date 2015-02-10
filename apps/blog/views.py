from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, TemplateView, DetailView, View, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.blog.forms import *
from apps.blog.models import *
from mongoengine.queryset import DoesNotExist
from mongoengine.django.auth import MongoEngineBackend
from lib.mixin import *
import lib
from django.core.urlresolvers import reverse
import pdb

# Create your views here.

class Login(FormView):
  template_name = 'login.html'
  form_class = LoginForm

  def dispatch( self, request, *args, **kwargs ):
    if self.request.user.is_authenticated():
      return redirect('index')

    return super( Login, self ).dispatch( request, *args, **kwargs )

  def form_valid(self, form):
    if self.request.method == 'POST':
      user = authenticate(username=self.request.POST['username'], password=self.request.POST['password'])
      if user is not None:
        login(self.request, user)
        message = 'Logged in as %s' % user.username
      else:
        message = "Error"

    messages.success(self.request, message)

    return super(Login, self).form_valid(form)

  def get_success_url(self):
    return self.request.GET.get('next','/')

  def get_context_data(self, **kwargs):
    context = super(Login, self).get_context_data(**kwargs)
    return context

class SignUp(CreateView):
  model = Blogger
  form_class = SignUpForm
  template_name = 'signup.html'

  def form_valid(self, form):
    blogger = form.save()
    # pdb.set_trace()
    asd = blogger.password
    blogger.password = blogger.set_password(asd).save()
    # blogger.password = asd
    blogger.save()
    
    messages.success(self.request, "User created.")
    return super(SignUp, self).form_valid(form)  

  def get_success_url(self):
    return reverse('index')

class Index(LoggedInMixin, TemplateView):
  template_name = 'index.html'

  def get_context_data(self,**kwargs):
    context = super(Index, self).get_context_data(**kwargs)
    posts = Post.objects
    context['form'] = LoginForm
    
    tag = self.request.GET.get('tag', None)
    if tag:
      context['posts'] = posts.filter(tags=tag)
    else:
      context['posts'] = posts.all()
    return context

class PostCreate(LoggedInMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = 'post_create.html'

  def form_valid(self, form):
    # pdb.set_trace()
    post = form.save(commit=False)
    post.user = Blogger.objects.get(pk=self.request.user.id)
    post.save()
    
    messages.success(self.request, "Post created.")
    return super(PostCreate, self).form_valid(form)  

  def get_success_url(self):
    return reverse('index')

class PostUpdate(LoggedInMixin, UpdateView):
  model = Post
  form_class = PostForm
  context_object_name = 'post'

  def get_template_names(self):
      return ["post_create.html"]

  def get_success_url(self):
    return reverse('index')

  def form_valid(self, form):
    post = form.save()
    post.save()
    messages.success(self.request, "Post updated.")
    return super(PostUpdate, self).form_valid(form)

  def get_object(self):
      return Post.objects.get(id=self.kwargs['pk'], slug=self.kwargs['slug'])

class PostDelete(LoggedInMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return reverse('index')

    def get(self, *args, **kwargs):
        """ Skip confirmation page """
        return self.delete(self.request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, "Post removed.")
        return redirect(self.get_success_url())        

    def get_object(self):
        return Post.objects.get(id=self.kwargs['pk'], slug=self.kwargs['slug'])

class PostDetail(LoggedInMixin,DetailView):
  model = Post
  context_object_name = "post"

  def get_template_names(self):
      return ["detail.html"]

  def get_context_data(self, **kwargs):
    context = super(PostDetail, self).get_context_data(**kwargs)
    return context

  def get_object(self):
      return Post.objects.get(id=self.kwargs['pk'], slug=self.kwargs['slug'])


  

