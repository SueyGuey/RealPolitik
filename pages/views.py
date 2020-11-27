from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from django.views.generic import DetailView, FormView, CreateView
from news.models import Article, Comment
from django.db import IntegrityError
from django.db.models import Q
from .forms import AddComment
import requests
from urllib.request import urlopen, Request
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import attrgetter

requests.packages.urllib3.disable_warnings()
def refresh(request):
	foreign_policy_req = requests.get("https://foreignpolicy.com/category/latest/")
	foreign_policy_soup = BeautifulSoup(foreign_policy_req.content, "html.parser")
	foreign_policy = foreign_policy_soup.find_all('div', {'class': 'excerpt-content--list content-block'})
	for headline in foreign_policy[::-1]:
		new_article = Article()
		new_article.title = headline.find_all('h3', {'class':'hed'})[0].text
		new_article.url= headline.find_all('a', {'class':'hed-heading -excerpt'})[0]['href']
		new_article.image_url = headline.find_all('img')[0]['data-src']
		auth = headline.find_all('a', {'class':'author'})
		if len(auth) != 0:
			new_article.author = auth[0].text
		else:
			new_article.author = "FP"
		new_article.site = "Foreign Policy"
		new_article.site_url = "https://foreignpolicy.com"
		try:
			new_article.save() #checks for errors
		except IntegrityError as e: 
   			if 'UNIQUE constraint' in str(e.args): #a repeat article
   				pass

	foreign_affairs_req = requests.get("https://www.foreignaffairs.com")
	foreign_affairs_soup = BeautifulSoup(foreign_affairs_req.content, "html.parser")
	foreign_affairs = foreign_affairs_soup.find_all('div', {'class' : 'magazine-list-item--image-link row'})
	for headline in foreign_affairs[::-1]:
		new_article = Article()
		new_article.title = headline.find_all('h3', {'class':'article-card-title font-weight-bold ls-0 mb-0 f-sans'})[0].text
		new_article.image_url = headline.find_all('img',{'class':'b-lazy b-lazy-ratio magazine-list-item--image d-none d-md-block'})[0]['data-src']
		if len(new_article.image_url) > 199:
			new_article.image_url = 'https://subscribe.foreignaffairs.com/FAF/pub_templates/faf/images/logo.png'
		new_article.url = headline.find_all('a', {'class':'d-block flex-grow-1'})[0]['href']
		new_article.author = headline.find_all('h4', {'class':'magazine-author font-italic ls-0 mb-0 f-serif'})[0].text
		new_article.site = "Foreign Affairs"
		new_article.site_url = "https://www.foreignaffairs.com"
		try: 
			new_article.save()
		except IntegrityError as e: 
	   		if 'UNIQUE constraint' in str(e.args):
	   			pass

	#they give a 403 error for other methods
	china_power_req = Request("https://chinapower.csis.org/podcasts/", headers = {'User-Agent' : 'Mozilla/5.0'})
	china_power_page = urlopen(china_power_req).read()
	china_power_soup = BeautifulSoup(china_power_page, "html.parser")
	china_power = china_power_soup.find_all('article')

	for headline in china_power[::-1]:
		#finding author
		disc = headline.find_all('p')[0].text #description has the author's name
		list_disc = disc.split() #find it in the text
		record = False
		index = 0
		list_auth = []
		while index > -1:
			tmp = list_disc[index]
			if tmp == "joins": #ends the name at the join
				break;
			if record:
				list_auth.append(tmp) #add the name
			if tmp == "episode,": #start at 'episode,'
				record = True;
			index = index + 1

		new_article = Article()
		new_article.title = headline.find_all('h2', {'class':'entry-title'})[0].text
		new_article.image_url = "https://megaphone.imgix.net/podcasts/722b9c2a-e6e1-11ea-a520-3349f6671499/image/uploads_2F1598366366917-v9rdxhpawhc-bee946f884ea9a141d33af2322074d0d_2F_ART_ChinaPower.jpg?ixlib=rails-2.1.2&w=400&h=400"
		new_article.url = headline.find_all('a')[0]['href']
		new_article.author = " ".join(list_auth) + " & Bonnie Glaser"
		new_article.site = "China Power Podcasts"
		new_article.site_url = "https://chinapower.csis.org/podcasts/"
		try: 
			new_article.save()
		except IntegrityError as e: 
	   		if 'UNIQUE constraint' in str(e.args):
	   			pass

	#for war on the rocks, each div class for the articles is different
	warontherocks_req = Request("https://warontherocks.com/", headers = {'User-Agent' : 'Mozilla/5.0'})
	warontherocks_page = urlopen(warontherocks_req).read()
	warontherocks_soup = BeautifulSoup(warontherocks_page, "html.parser")
	warontherocks = warontherocks_soup.find_all('div', {'class' : 'all-posts'})

	#very nice and straight forward html from warontherocks
	header_ = warontherocks[0].find_all('h3')
	link_ = warontherocks[0].find_all('a')
	img_ = warontherocks[0].find_all('img')
	writer_ = warontherocks[0].find_all('h4')

	for i in range(12,1,-1):
		new_article = Article()
		new_article.title = header_[i-1].text
		new_article.image_url = img_[i-1]['src']
		new_article.url = link_[2*i-1]['href']
		new_article.author = writer_[i-1].text
		new_article.site = "War on the Rocks"
		new_article.site_url = "https://warontherocks.com"
		try: 
			new_article.save()
		except IntegrityError as e: 
	   		if 'UNIQUE constraint' in str(e.args):
	   			pass

	"""AP_FP_req = Request("https://apnews.com/hub/foreign-policy", headers = {'User-Agent' : 'Mozilla/5.0'})
	AP_FP_page = urlopen(AP_FP_req).read()
	AP_IL_req = Request("https://apnews.com/hub/international-relations", headers = {'User-Agent' : 'Mozilla/5.0'})
	AP_IL_page = urlopen(AP_IL_req).read()
	AP_FP_soup = BeautifulSoup(AP_FP_page, "html.parser")
	AP_IL_soup = BeautifulSoup(AP_IL_page, "html.parser")
	AP = AP_FP_soup.find_all('div', {'data-key': 'feed-card-wire-story-with-image'}) + AP_IL_soup.find_all('div', {'data-key': 'feed-card-wire-story-with-image'})
	for headline in AP[::-1]:
		new_article = Article()
		new_article.title = headline.find_all('h1')[0].text
		new_article.url= "https://apnews.com" + headline.find_all('a')[0]['href']
		#img machine broke
		img = headline.find_all('img', {'class': 'image-0-2-132'})
		if len(img) == 0:
			new_article.image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Associated_Press_logo_2012.svg/220px-Associated_Press_logo_2012.svg.png"
		else:
			new_article.image_url = img[0]['src']
		list_auth = (headline.find_all('span')[0].text).split(" ")
		if "GMT" in list_auth:
			new_article.author = "AP"
		else:
			new_article.author = headline.find_all('span')[0].text
		new_article.site = "Associated Press"
		new_article.site_url = "https://apnews.com"
		try:
			new_article.save() #checks for errors
		except IntegrityError as e: 
   			if 'UNIQUE constraint' in str(e.args): #a repeat article
   				pass"""

   	#lowy institute
	LI_req = Request("https://www.lowyinstitute.org/the-interpreter/archive", headers = {'User-Agent' : 'Mozilla/5.0'})
	LI_page = urlopen(LI_req).read()
	LI_soup = BeautifulSoup(LI_page, "html.parser")
	LI = LI_soup.find_all('article')

	for headline in LI[::-1]:
		img = headline.find_all('div',{'class':'article-thumb'})[0]
		if len(img) == 0:
			img = headline.find_all('div',{'class':'article-thumb-wrap'})[0]
		word = [] #getting the link into a list of chars
		record = False
		for letter in list(img['style']):
			if record:
				word.append(letter)
			if letter == "'":
				if record:
					word.pop() #revmoving the ' at the end
					break
				record = True

		new_article = Article()
		new_article.title = headline.find_all('h2', {'class':'article-title txt-f4 txt-s6 mv-0 pv-xs'})[0].text
		new_article.url= "https://www.lowyinstitute.org" + headline.find_all('a', {'class':'txt-dn'})[0]['href']
		new_article.image_url = "".join(word)
		new_article.author = headline.find_all('a', {'class':'txt-dn'})[1].text
		new_article.site = "Lowy Institute"
		new_article.site_url = "https://www.lowyinstitute.org/the-interpreter/archive"
		
		try:
			new_article.save()
		except IntegrityError as e: 
   			if 'UNIQUE constraint' in str(e.args):
   				pass

	return redirect("../")

def getQuerySet(query = None): #for searching
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
		query = request.GET.get('q','')
		context['query'] = str(query) #returns post relating to our search

	articles = sorted(getQuerySet(query), key = attrgetter('time_added') , reverse = True) #gives it most recent order

	page_num = request.GET.get('page',1)
	pgntr = Paginator(articles, 10) #divides it into pages of 10 articles

	#error checking
	try:
		articles = pgntr.page(page_num)
	except EmptyPage:
		articles = pgntr.page(pgntr.num_pages) #page doesn't exist so we go to page 1
	except PageNotAnInteger:
		articles = pgntr.page(1) #page not an int

	context['articles'] = articles

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

def contact(request):
	return render(request,"contact.html")

def about(request):
	return render(request,"about.html")