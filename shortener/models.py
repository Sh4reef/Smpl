from django.db import models
from django.conf import settings
from django.utils.encoding import smart_text
from django.urls import reverse

import string
from random import choice

# Create your models here.

def generate_code(size=6, chars=string.ascii_lowercase + string.digits):
	return ''.join(choice(chars) for char in range(size))

def create_shortcode(instance, size=6):
	new_shortcode = generate_code(size=size)
	if instance.__class__.objects.filter(shortcode=new_shortcode).exists():
		return create_shortcode(size=size)
	return new_shortcode

class Smpl(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	url = models.CharField(max_length=120)
	shortcode = models.CharField(max_length=6, unique=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return smart_text(self.url)

	def save(self, *args, **kwargs):
		if self.shortcode is None or self.shortcode == '':
			self.shortcode = create_shortcode(self)
		super(Smpl, self).save(*args, **kwargs)

	def get_short_url(self):
		return reverse('shortener:redirect', kwargs={'shortcode': self.shortcode})