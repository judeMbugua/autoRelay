from django.db import models
from django.contrib.auth.models import User


class Recipient(models.Model):
		file = models.FileField(max_length=100)


class RecipientOneMany(models.Model):
	file = models.FileField(max_length=100)



class RecipientMany(models.Model):
	file = models.FileField(max_length=100)