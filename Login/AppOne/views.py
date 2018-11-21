from django.shortcuts import render
from AppOne.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	return render(request, 'AppOne/index.html')


def register(request):
	registered = False

	if request.method == "POST":
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileInfoForm(data = request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit = False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()


	data_dict = {'user_form': user_form,
			'profile_form': profile_form,
			'registered': registered}

	return render(request, 'AppOne/register.html', data_dict)


def user_login(request):
	if request.method == "POST":
		# Getting the entered username and password
		username = request.POST['username']
		password = request.POST['password']

		# Tying to authenticate the user based on entered credentials
		user = authenticate(username = username, password = password)

		# If user is authenticated, login the user and redirect to homepage
		if user:
			# If user account is active then login the user
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
				return HttpResponse("Your account is not active")
		else:
			print("Someone tried to login and failed")
			print(f"username: {username} and password: {password}")
			return HttpResponse("Invalid login credentials")

	else:
		return render(request, 'AppOne/login.html')


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))