from django.urls import path
from pages.views import home, refresh

urlpatterns = [
	path('', home, name='home'),
	path('refresh/', refresh, name='refresh'),
]