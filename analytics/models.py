from django.db import models

# Create your models here.
from shortener.models import Smpl

class AnalyticManager(models.Manager):
	def click_count(self, SmplInstance):
		if isinstance(SmplInstance, Smpl):
			obj, iscreated = Analytic.objects.get_or_create(url=SmplInstance)
			obj.count += 1
			obj.save()
			return obj.count
		return None 

class Analytic(models.Model):
	url = models.ForeignKey(Smpl)
	count = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	objects = AnalyticManager()

	def __str__(self):
		return str(self.count)