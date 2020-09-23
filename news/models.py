from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
	title = models.CharField(max_length = 100)
	author = models.CharField(max_length = 100, default = "Author")
	image_url = models.URLField(max_length = 100,null = True, blank = True)
	url = models.URLField(max_length = 100)
	site = models.CharField(max_length = 100, default = "News")
	site_url = models.URLField(max_length = 100,default = "google.com")

	class Meta:
		unique_together = [["title","author"]]

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Article,related_name = "comments", on_delete = models.CASCADE)
	username = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	content = models.TextField(max_length = 100)
	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.post.title + ' - ' + str(self.username)