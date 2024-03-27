from django.db import models

class Recipient(models.Model):
	file = models.FileField(max_length=100)


