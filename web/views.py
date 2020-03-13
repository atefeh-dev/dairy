from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from rest_framework import status
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.views.decorators.http import require_POST
from .models import User, Profile, TempUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .authentication import token_expire_handler, expires_in
from rest_framework.authtoken.models import Token
import python_jwt as jwt, jwcrypto.jwk as jwk
from .models import TempUser
import django
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

# Create your views here.


@csrf_exempt
def register(request):

    if User.objects.filter(email=request.POST['email']).exists():
        return JsonResponse({'status': status.HTTP_403_FORBIDDEN, 'comment': 'this email already registered'})

    if User.objects.filter(email=request.POST['username']).exists():
        return JsonResponse({'status': status.HTTP_403_FORBIDDEN, 'comment': 'this username already registered'})

    if TempUser.objects.filter(email=request.POST['email']).exists():
        return JsonResponse({'status': False,
                             'status_code': status.HTTP_403_FORBIDDEN,
                            'message': 'The activation code has already been sent to your email',
                            })

    if TempUser.objects.filter(user=request.POST['username']).exists():
        return JsonResponse({'status': False,
                             'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                            'message': 'this username already exist',
                             })
    else:
        user = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        join = datetime.now()
        key = jwk.JWK.generate(kty='RSA', size=2048)
        payload = {'email': email, 'wup': str(datetime.now())}
        token = jwt.generate_jwt(payload, key, 'PS256')
        temp_user = TempUser(user=user, email=email, password=password, date=join, code=token)
        temp_user.save()
        send_mail('کد فعال سازی',
                  'برای فعال کردن حساب کاربری خود لطفا روی لینک زیر کلیک کنید {}'.format(
                      request.build_absolute_uri(reverse('active', kwargs={'token': token,
                                                                           'id': temp_user.auto_increment_id}))),
                  settings.EMAIL_HOST_USER,
                  ['atefeh.mohammaddoust@gmail.com'],
                  fail_silently=False,
                  )
        return JsonResponse({'success': True,
                         'status_code': status.HTTP_200_OK,
                         'message': '{} dear please verified your email'.format(user)})


@csrf_exempt
def active(request, id, token):
    if TempUser.objects.filter(auto_increment_id=id, code=token).exists():
        validated = TempUser.objects.get(auto_increment_id=id)
        if validated.active:
            return JsonResponse({
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You have activated the email before'
            })
        else:
            validated.active = True
            validated.save()
            new_user = User.objects.create_user(username=validated.user, email=validated.email)
            new_user.set_password(validated.password)
            new_user.save()
            return JsonResponse({
                'success': True,
                'status_code': status.HTTP_201_CREATED,
                'message': 'Thank you for your email confirmation'
                })

    else:
        return JsonResponse({
            'success': False,
            'status_code': status.HTTP_406_NOT_ACCEPTABLE,
            'message': 'Activation link is invalid!'
        })
