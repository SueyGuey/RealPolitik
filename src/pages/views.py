from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from django.views.generic import DetailView, FormView, CreateView
from news.models import Article, Comment
from django.db import IntegrityError
from django.db.models import Q
from .forms import AddComment
import requests
from django.urls import reverse
from django.contrib.auth.decorators import login_required

requests.packages.urllib3.disable_warnings()
def refresh(request):
	foreign_policy_req = requests.get("https://foreignpolicy.com/category/latest/")
	foreign_policy_soup = BeautifulSoup(foreign_policy_req.content, "html.parser")
	foreign_policy = foreign_policy_soup.find_all('div', {'class': 'excerpt-content--list content-block'})
	for headline in foreign_policy[::-1]:
		header = headline.find_all('h3', {'class':'hed'})[0].text
		link = headline.find_all('a', {'class':'hed-heading -excerpt'})[0]['href']
		img = headline.find_all('img')[0]['data-src']
		writer = headline.find_all('a', {'class':'author'})[0].text

		new_article = Article()
		new_article.title = header
		new_article.image_url = img
		new_article.url = link
		new_article.author = writer
		new_article.site = "Foreign Policy"
		new_article.site_url = "https://foreignpolicy.com"
		try:
			new_article.save()
		except IntegrityError as e: 
   			if 'UNIQUE constraint' in str(e.args): #a repeat article
   				pass
   			else:
   				new_article.save()
	foreign_affairs_req = requests.get("https://www.foreignaffairs.com")
	foreign_affairs_soup = BeautifulSoup(foreign_affairs_req.content, "html.parser")
	foreign_affairs = foreign_affairs_soup.find_all('div', {'class' : 'magazine-list-item--image-link row'})
	for headline in foreign_affairs:
		header = headline.find_all('h3', {'class':'article-card-title font-weight-bold ls-0 mb-0 f-sans'})[0].text
		link = headline.find_all('a', {'class':'d-block flex-grow-1'})[0]['href']
		img = headline.find_all('img',{'class':'b-lazy b-lazy-ratio magazine-list-item--image d-none d-md-block'})[0]['data-src']
		writer = headline.find_all('h4', {'class':'magazine-author font-italic ls-0 mb-0 f-serif'})[0].text

		new_article = Article()
		new_article.title = header
		new_article.image_url = img
		new_article.url = link
		new_article.author = writer
		new_article.site = "Foreign Affairs"
		new_article.site_url = "https://www.foreignaffairs.com"
		try:
			new_article.save()
		except IntegrityError as e: 
	   		if 'UNIQUE constraint' in str(e.args):
	   			pass
	   		else:
	   			new_article.save()


	return redirect("../")

def getQuerySet(query = None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = Article.objects.filter(Q(title__icontains = q)).distinct()
		for post in posts:
			queryset.append(post)

	return list(set(queryset))

def home(request, *args, **kwargs):
	query = ""
	context = {}
	if request.GET:
		query = request.GET['q']
		context['query'] = str(query)

	articles = getQuerySet(query)[::-1]
	context = {
		'articles': articles
	}

	return render(request,"home.html",context)

#viewing each article with its comments
class HomeDetailView(DetailView):
	model = Article
	template_name = 'detail_article.html'

class CommentView(CreateView):
	model = Comment
	template_name = 'add_comment.html'
	form_class = AddComment

	def form_valid(self,form):
		#automatically have the post id
		form.instance.post_id = self.kwargs['pk']
		#automatically add username
		form.instance.user = self.request.user
		return super().form_valid(form)

	def get_success_url(self):#goes back to page
		return reverse('ArticleDetail', kwargs={'pk': self.kwargs['pk']})


"""
#viewing each article with its comments
class HomeDetailView(FormView, DetailView):
	model = Article
	form_class = AddComment
	template_name = 'detail_article.html'

	def get_context_data(self, **kwargs):
		context = super(HomeDetailView, self).get_context_data(**kwargs)
		context['form'] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		return FormView.post(self, request, *args, **kwargs)

	def get_success_url(self): #goes back to page
		return reverse('ArticleDetail', kwargs={'pk': self.kwargs['pk']})

class ArticleFormView(FormView):
	form_class = AddComment

	def get_success_url(self):#goes back to page
		return reverse('ArticleDetail', kwargs={'pk': self.kwargs['pk']})

class HomeDetailView(DetailView):
	model = Article
	template_name = 'detail_article.html'

	def get_context_data(self, **kwargs):
		context = super(HomeDetailView, self).get_context_data(**kwargs)
		context['form'] = ArticleFormView
		return context"""


def contact(request):
	return render(request,"contact.html")

def about(request):
	return render(request,"about.html")