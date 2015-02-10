from django import forms
from pprint import pprint
from models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Div,Submit,HTML,Button,Row, Field, Hidden
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, InlineCheckboxes
import pdb

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())


	helper = FormHelper()
	# helper.form_tag = False
	helper.form_method = 'POST'
	helper.form_class = 'form-horizontal'
	helper.layout = Layout(
  	Field('username', css_class='input-lg-4'),
  	Field('password', css_class='input-lg-4'),
  	FormActions(Submit('login', 'Login', css_class='btn btn-primary')),
  )

class SignUpForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()
	email = forms.EmailField()
	first_name = forms.CharField()
	last_name = forms.CharField()

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
		  	FormActions(Submit('signup', 'Sign Up', css_class='btn btn-primary')),
		)

	def save(self):
		blogger = self.instance if self.instance else Blogger()
		# pdb.set_trace()
		blogger.first_name = self.cleaned_data['first_name']
		blogger.last_name = self.cleaned_data['last_name']
		blogger.email = self.cleaned_data['email']
		blogger.username = self.cleaned_data['username']
		blogger.password = self.cleaned_data['password']
		# blogger.is_published = self.cleaned_data['is_published']
		# blogger.tags = Tag.objects(id__in=self.cleaned_data['tags'])
		# blogger.user = Blogger.objects.get(id=kwargs['user_id'])
		# print user_id
		# if commit:
		# 	blogger.save()

		return blogger

	

# class SignUpForm(forms.Form):

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

	def save(self, commit=True):
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