from django.db import models
from datetime import datetime
# from django.contrib.auth.models import AbstractBaseUser
from mongoengine import *
from mongoengine.django.auth import *
from slugify import slugify
from django.core.urlresolvers import reverse


class Blogger(User):
	email = StringField(max_length=200, required=True)
	first_name = StringField(max_length=255, required=True)
	last_name = StringField(max_length=255, required=True)

	def __unicode__(self):
		return self.username

	# def save(self, *args, **kwargs):
	# 	self.password = self.set_password(self.password).save()
	# 	return super(Blogger, self).save(*args, **kwargs)

class Category(Document):
	name = StringField(max_length=200,required=True)
  
	def __unicode__(self):
		return self.name

class Tag(Document):
	name = StringField(max_length=200,required=True)

	def __unicode__(self):
		return self.name

class Post(Document):
	user = ReferenceField(Blogger, reverse_delete_rule=CASCADE)
	title = StringField(max_length=200, required=True)
	content = StringField(required=True)
	date_modified = DateTimeField(default=datetime.now)
	is_published = BooleanField()
	slug = StringField(max_length=200)
	image_url = StringField(max_length=200)
	categories = ListField(ReferenceField(Category), default=list)
	tags = ListField(ReferenceField(Tag),default=list)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		return super(Post, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('post:detail',args=[self.id])

	def get_edit_url(self):
		return reverse('post:update', args=[self.id])

class Comment(Document):
	user = ReferenceField(User,reverse_delete_rule=CASCADE)
	post = ReferenceField(Post, reverse_delete_rule=CASCADE)
	text = StringField(required=True)
	date = DateTimeField(default=datetime.now)

	def __unicode__(self):
		return self.text



