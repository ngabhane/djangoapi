from __future__ import unicode_literals

from django.db import models

class Movie(models.Model):
	popularity99 = models.FloatField()
	director 	 = models.CharField(max_length=100)
	genre 		 = models.CharField(max_length=100)
	imdb_score 	 = models.FloatField()
	name 		 = models.CharField(max_length=100)

	def __str__(self):
		return self.name
