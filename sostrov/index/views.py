# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.contrib import auth
from index import models as index_models
from index.email_module import sendEmail
	
def add_to_group(request, pk):
	arg = {}
	user = User.objects.get(id=pk)
	group = Group.objects.get(name='Users') 
	if not user.groups.filter(name = 'Users').exists():
		group.user_set.add(user)
		text = user.first_name+', Вы добавлены в базу данных пользователей страницей кооператва "солнечный остров"'
		link = 'sostrov.com'
		arg['status'] = user.first_name + ' ' + user.last_name + '('+ user.email+ ')' + 'успешно добавлен в пользователи сайтом.'
		try:
			sendEmail(link,text,user.email,'koop.sostrov@gmail.com','soostrov')
		except:
			arg['status']+=' Внимание: Пользователь не был уведомлен о его успешном добавлени на сайт, система не email отправить письмо.'
	else:
		arg['status'] = 'Пользователь уже добавлен. '
	return render(
	 	request, 'added.html', arg
	 	)

def index(request):
	message = {}

	if 'autha' in request.POST:
		sign_in_email = request.POST['sign_in_email']
		sign_in_pass = request.POST['sign_in_pass']
		# user = User.objects.get(email=sign_in_email)
		user = auth.authenticate(username=sign_in_email, password=sign_in_pass)
		if user is not None:
			if user.groups.filter(name = 'Users').exists():
				auth.login(request, user)
				message['status'] = "success"
			else:
				message['status'] = "К сожалению, вы еще не добавлены в пользователи сайтом, обратитесь к администрации сайта"
		else:
			message['status'] = "Не удалось найти email или не правильный пароль" 
		return JsonResponse(message)

	elif 'num_uchastok' in request.POST:
		try:
			name = request.POST['login'].split()
			login = request.POST['email']
			password = request.POST['password']
			email = request.POST['email']
			num_uchastok = request.POST['num_uchastok']
			num_ochered = request.POST['num_ochered']
			try:
				first_name = name[1]
			except:
				first_name = '-'

			try:
				first_name+= ' ' + name[2]
			except:
				pass	
			try:
				user = User.objects.create_user(login, email, password)
				user.last_name = name[0]
				user.first_name = first_name
				user.save()
				admin = User.objects.get(username = 'user')
				text = '  <b>Новый пользователь:</b>' + request.POST['login'] + ', <b>email:</b> ' + email + ', <b>телефон:</b> ' + request.POST['mob_telephone'] +', <b>участок:</b> ' + str(num_uchastok)+', <b>очередь:</b> ' + str(num_ochered)
				link = 'http://sostrov.com/add/'+ str(user.id)
				sendEmail(link,text,admin.email,'koop.sostrov@gmail.com','soostrov')
				message['status'] = 'Регистрация прошла успешно. Необходимо подтверждение администрации'
			except:
				message['status'] = 'Пользователь ' + email + ' уже существует'
		except:
			message['status'] = 'Попробуйте еще раз, ошибка'
		return JsonResponse(message)

	elif 'logout' in request.POST: 
		auth.logout(request)
		message['status'] = "logouted"
		return JsonResponse(message)

	
	if request.user.is_authenticated():
		arg = {}
		arg['docs'] = index_models.doc.objects.all()
		arg['groups'] = index_models.group.objects.all()
		# arg['news'] = index_models.news.objects.all()
		return render(
		 	request, 'index.html', arg
		 	)
	else:
	 	return render(
		 	request, 'registration.html',
		 	)


# def index(request):
#  	return render(
# 	 	request, 'index.html',
# 	 	);