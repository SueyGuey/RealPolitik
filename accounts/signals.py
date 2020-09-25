from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import profile

#creates a profile upon creating an account
@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		profile.objects.create(user = instance) #creates profile

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
	instance.profile.save() #saves profile