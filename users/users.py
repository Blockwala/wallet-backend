from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json


##Generate new user if not exists and return the token

@csrf_exempt
def create_user(request):
	request = json.loads(request.body.decode('utf-8'))
	user = None

	try:
		#exists
		user = User.objects.get(username=request["username"])
	except User.DoesNotExist:
		#NEW
		user = User(
		    # email = request["email"],
		    username = request["username"]
		)
		user.set_password(request["password"])
		user.save()

	if user is not None:
	# the password verified for the user
		if user.is_active:
			token, created = Token.objects.get_or_create(user=user)
			return JsonResponse({"auth": token.key}, status=200)

	return JsonResponse({"error": "error retrieving the token"}, status=500)


@csrf_exempt
def get_auth_token(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({"auth": token.key}, status=200)

    return JsonResponse({"error": "user not found"}, status=500)