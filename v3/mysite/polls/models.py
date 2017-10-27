from django.db import models
import datetime
from django.utils impor timezone

# Create your models here.
class Question(models.Model):
	Question_text = models.CharField(max_length=200)
	pub_data = models.DateTimeField('date published')
	def __str__(self):
		return self.Question_text

class Choice(models.Model):
	Question = models.ForeignKey(Question)
	Choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.Choice_text

						