from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from bs4 import BeautifulSoup
import urllib
import mechanize
from datetime import datetime

def test(request):
	last_date = request.GET.get('lastDate','01 01 00')
	if (int(last_date[:2]) > 31) or (int(last_date[3:5]) > 12):
		last_date = '01 01 00'

	last_date = datetime.strptime(last_date, '%d %m %y')
	return HttpResponse(last_date)

def select_form(form):
	return form.attrs.get('action', None) == 'indexPage.php'

def index(request):
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.open('http://kiittnp.in/tnp/usr/index.php')
	br.select_form(predicate=select_form)
	br.form['user_name']='1305394@kiit.ac.in'
	br.form['password']='iammakarov007'
	content = br.submit().read()
	# print br.response().geturl()

	# r = urllib.urlopen('http://www.kiittnp.in')
	soup = BeautifulSoup(content)
	posts = soup.find_all('fieldset')
	to_send = {}
	cnt = 1

	last_date = request.GET.get('lastDate','01 01 00')
	if (int(last_date[:2]) > 31) or (int(last_date[3:5]) > 12):
		last_date = '01 01 00'

	last_date = datetime.strptime(last_date, '%d %m %y')
	for post in posts:
		post_date = post.b.get_text()[6:16]
		post_date = datetime.strptime(post_date, '%Y-%m-%d')
		if post_date >= last_date:
			to_send[cnt] = [post.h3.get_text(),'http://kiittnp.in/tnp/' + post.a['href'][3:]]
		cnt = cnt + 1

	# return render(request,'scrape/index.html',{'to_send':to_send})
	return JsonResponse(to_send)