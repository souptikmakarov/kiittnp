from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from bs4 import BeautifulSoup
import urllib
import mechanize
from datetime import datetime

def test2(request):
	return HttpResponse('This is working')

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
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open('http://kiittnp.in/tnp/usr/index.php')
	br.select_form(predicate=select_form)
	br.form['user_name']='1305394@kiit.ac.in'
	br.form['password']='iammakarov007'
	content = br.submit().read()
	
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
