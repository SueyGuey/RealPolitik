from django import forms
from news.models import Comment

class AddComment(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']
