from django import forms
from pprint import pprint
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row, Field, Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, InlineCheckboxes
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import pdb

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			raise forms.ValidationError(
				mark_safe(
					('User not found. Register <a href="{0}">Here</a>').format(reverse('signup'))
				)
			)
		return username

	def clean_password(self):
		username = self.cleaned_data.get('username',None)
		password = self.cleaned_data['password']
		try:
			user = User.objects.get(username=username)
		except:
			user = None
		if user is not None and not user.check_password(password):
			raise forms.ValidationError("Invalid Password")
		elif user is None:
			pass
		else:
			return password

	helper = FormHelper()
	# helper.form_tag = False
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.layout = Layout(
  	Field('username', placeholder='Username', css_class='input-lg-4'),
  	Field('password', placeholder='Password', css_class='input-lg-4'),
  	FormActions(Submit('login', 'Login', css_class='btn btn-primary')),
  )

class SignUpForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	password_confirm = forms.CharField(widget=forms.PasswordInput())
	email = forms.EmailField(required=False)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)

	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance', None)
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
		# helper.form_tag = False
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		self.helper.layout = Layout(
		  	Field('first_name'),
		  	Field('last_name'),
		  	Field('email'),
		  	Field('username'),
		  	Field('password'),
		  	Field('password_confirm'),
		  	FormActions(Submit('signup', 'Sign Up', css_class='btn btn-primary')),
		)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.get(username=username)
		except:
			user = None
			
		if user:
			raise forms.ValidationError('Username is not available')
		else:
			return username

	def clean_password_confirm(self):
		username = self.cleaned_data.get('username',None)
		password = self.cleaned_data['password']
		password_confirm = self.cleaned_data['password_confirm']
		try:
			user = User.objects.get(username=username)
		except:
			user = None
		if password != password_confirm :
			raise forms.ValidationError("Password didn't match")
		else:
			return password

	def save(self):
		blogger = self.instance if self.instance else Blogger()
	# 	# pdb.set_trace()
		blogger.first_name = self.cleaned_data['first_name']
		blogger.last_name = self.cleaned_data['last_name']
		blogger.email = self.cleaned_data['email']
		blogger.username = self.cleaned_data['username']
		blogger.password = self.cleaned_data['password']
	# 	# print user_id
	# 	# if commit:
	# 	# 	blogger.save()

		return blogger

class PostForm(forms.Form):
	title = forms.CharField()
	content  = forms.CharField(widget=forms.widgets.Textarea())
	tags = forms.MultipleChoiceField(
		widget=forms.widgets.CheckboxSelectMultiple(), 
		required=False)


	def __init__(self, *args, **kwargs):
		self.instance = kwargs.pop('instance', None)
		# pdb.set_trace()
		# foo = kwargs.get('foo')
		super(PostForm, self).__init__(*args, **kwargs)
		self.fields['tags'].choices = [(tag.id, tag.name) for tag in Tag.objects]

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'
		self.helper.layout = Layout(
			Field('title', css_class='input-lg-4'),
			Field('content'),
			InlineCheckboxes('tags'),
			FormActions(Submit('submit', 'Submit', css_class='btn btn-info')),
		)
		

		if self.instance:
			self.fields['title'].initial = self.instance.title
			self.fields['content'].initial = self.instance.content
			self.fields['tags'].initial = [tag.id for tag in self.instance.tags]

	def save(self):
		post = self.instance if self.instance else Post()
		# pdb.set_trace()
		post.title = self.cleaned_data['title']
		post.content = self.cleaned_data['content']
		# post.is_published = self.cleaned_data['is_published']
		post.tags = Tag.objects(id__in=self.cleaned_data['tags'])
		# post.user = Blogger.objects.get(id=kwargs['user_id'])
		# print user_id
		# if commit:
		# 	post.save()
		return post

class ExampleForm(forms.Form):
    search = forms.CharField()

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
    	Field('search', id='search', placeholder='Search Posts'),
    	# FormActions(HTML("<input class='btn btn-info' type='button' value='Search' name='search' data-toggle='modal' data-target='#myModal' onclick='tes()' />")),
    )


	