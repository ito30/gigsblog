from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, TemplateView, DetailView, View, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404
from mongoengine.queryset import DoesNotExist
from mongoengine.django.auth import MongoEngineBackend
from apps.blog.forms import *
from apps.blog.models import *
from lib.mixin import *
import pdb
from django_ajax.mixin import AJAXMixin

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
    blogger.password = blogger.set_password(blogger.password)
    # pdb.set_trace()
    
    messages.success(self.request, "User created.")
    return super(SignUp, self).form_valid(form)  

  def get_success_url(self):
    return reverse('index')

class Index(LoggedInMixin, TemplateView):
  template_name = 'index.html'  

  def get_context_data(self,**kwargs):
    context = super(Index, self).get_context_data(**kwargs)
    ITEMS_PER_PAGE = 2
    context['home'] = self.request.get_full_path()
    
    tag = self.request.GET.get('tag', None)
    if tag:
      context['tag'] = tag;
      context['posts'] = Post.objects.filter(tags=tag)
    else:
      context['posts'] = Post.objects.all()
      paginator = Paginator(context['posts'], ITEMS_PER_PAGE)

      page = self.request.GET.get('page')
      try:
          context['posts'] = paginator.page(page)
      except PageNotAnInteger:
          # If page is not an integer, deliver first page.
          context['posts'] = paginator.page(1)
          # raise Http404("Question does not exist")
      except EmptyPage:
          # If page is out of range (e.g. 9999), deliver last page of results.
          context['posts'] = paginator.page(paginator.num_pages)
          raise Http404("Question does not exist")

      posts = context['posts']
      # context['page'] = 'class=active' if page else ''
      context['previous'] = '' if posts.has_previous() else 'class=disabled'
      context['next'] = '' if posts.has_next() else 'class=disabled'
      context['indexes'] = posts.paginator.page_range

    # search = self.request.GET.get('search', None)
    # if search:
    #   context['search'] = search
    #   context['posts'] = posts.filter(title__icontains=search)

    return context

class AjaxPostSearchResult(AJAXMixin, TemplateView):
  template_name = 'ajax_post_list.html'

  def get_context_data(self, **kwargs):
      context = super(AjaxPostSearchResult, self).get_context_data(**kwargs)
      if self.request.GET:
        title = self.request.GET.get('search', None)

        # if title == '':
        #   posts = Post.objects.all()
        # else:
        posts = Post.objects.filter(title__icontains=title)

        if posts:
          context['posts'] = posts
          context['found'] = True
        else:
          context['found'] = False
      else:
        context['posts'] = False

      return context

# class Search(FormView):
#   template_name = 'post_search.html'
#   form_class = SearchForm

# class PostList(AJAXMixin, TemplateView):
#   template_name = 'ajax_post_list.html'

#   def get_context_data(self, **kwargs):
#       context = super(PostList, self).get_context_data(**kwargs)
#       if self.request.GET:
#         title = self.request.GET.get('search', None)
#         posts = Post.objects.filter(title__icontains=title)

#         if posts:
#           context['posts'] = posts
#         else:
#           context['posts'] = 'Posts not found..'
#       else:
#         context['posts'] = 'Posts not found..'

#       return context

class FileTest(TemplateView):
    template_name = 'file_test.html'

    def get_context_data(self, **kwargs):
        context = super( FileTest, self ).get_context_data( **kwargs )
        context['accepted_mime_types'] = ['image/*']
        return context



class PostCreate(LoggedInMixin, CreateView):
  model = Post
  form_class = PostForm
  template_name = 'post_create.html'

  def form_valid(self, form):
    # pdb.set_trace()
    post = form.save()
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


  

