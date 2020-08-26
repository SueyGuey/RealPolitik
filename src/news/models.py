from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
	title = models.CharField(max_length = 150)
	author = models.CharField(max_length = 150, default = "Author")
	image_url = models.URLField(null = True, blank = True)
	url = models.URLField()
	site = models.CharField(max_length = 150, default = "News")
	site_url = models.URLField(default = "google.com")

	class Meta:
		unique_together = [["title","author"]]

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Article,related_name = "comments", on_delete = models.CASCADE)
	username = models.ForeignKey(User, on_delete = models.CASCADE)
	content = models.TextField()
	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.post.title + '-' + self.username