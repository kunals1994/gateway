from django.db import models

# Create your models here.
class Item(models.Model):
	imgurl = models.CharField(max_length=300)
	title = models.CharField(max_length=500)
	itemid = models.CharField(max_length=20)
	price = models.CharField(max_length=50)
	gender = models.IntegerField(default=2)

	def __str__(self):
		return self.title

