from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			#creates a message on our main page
			messages.success(request, f'Account created successfully!')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, "register.html",{'form':form})

@login_required
def profile(request):
	#viewing your profile and then updating
	if request.method == 'POST':
		userupdate = UserUpdateForm(request.POST, instance=request.user)
		profileupdate = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if userupdate.is_valid() and profileupdate.is_valid():
			userupdate.save()
			profileupdate.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('profile')
	else:
		userupdate = UserUpdateForm(instance=request.user)
		profileupdate = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'userupdate': userupdate,
		'profileupdate': profileupdate
	}

	return render(request, 'profile.html', context)