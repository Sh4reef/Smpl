from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import View

# Create your views here.

from .forms import URLForm, MultiURLForm
from .models import Smpl
from analytics.models import Analytic

class SmplHomeCBV(View):
	def get(self, request, *args, **kwargs):
		template = 'home.html'
		urlform = URLForm()
		context = {'title': 'Smpl URL', 'urlform': urlform}
		return render(request, template, context)
	def post(self, request, *args, **kwargs):
		template = 'home.html'
		urlform = URLForm(request.POST or None)
		context = {'title': 'URL Shortener', 'urlform': urlform}
		if request.POST.get('url'):
			if urlform.is_valid():
				user = User.objects.first()
				if request.user.is_authenticated():
					user = request.user
				url = urlform.cleaned_data['url']
				obj, created = Smpl.objects.get_or_create(user=user, url=url)
				analytic_obj, iscreated = Analytic.objects.get_or_create(url=obj)					
				if created:
					# created_list.append(created)														
					messages.add_message(
						request, 
						messages.SUCCESS, 						
						'<a href="%s" target="_blank">%s/%s</a>' % (obj.get_short_url(), get_current_site(request), obj.shortcode),   
						# '<a href="%s/%s" target="_blank">%s/%s</a>' % (get_current_site(request), obj.shortcode, get_current_site(request), obj.shortcode),
						extra_tags='label label-success'
						)
				else:
					messages.info(
						request, 
						'This URL has already been shorten.', 
						extra_tags='label label-info'
						)
					messages.add_message(
						request, 
						messages.INFO, 						
						'<a href="%s" target="_blank">%s/%s</a>' % (obj.get_short_url(), get_current_site(request), obj.shortcode), 
						# '<a href="%s" target="_blank">%s/%s</a><span class="badge">Visited : %i</span>' % (obj.get_short_url(), get_current_site(request), obj.shortcode, int(analytic_obj.count)),
						# '<a href="%s/%s" target="_blank">%s/%s</a>' % (get_current_site(request), obj.shortcode, get_current_site(request), obj.shortcode),
						extra_tags='label label-default text-center'
						)
				# return HttpResponseRedirect(reverse('shortener:home'))
		return render(request, template, context)

class SmplMultiCBV(View):
	def get(self, request, *args, **kwargs):
		template = 'multi.html'
		multiform = MultiURLForm()
		context = {'title': 'Smpl URL', 'multiform': multiform}
		return render(request, template, context)
	def post(self, request, *args, **kwargs):
		template = 'multi.html'
		multiform = MultiURLForm(request.POST or None)
		context = {'title': 'URL Shortener', 'multiform': multiform}
		if request.POST.get('multiurl'):
			if multiform.is_valid():
				urls = multiform.cleaned_data['multiurl']
				obj_list = ['']
				created_list = ['']
				for url in urls:
					user = User.objects.first()
					if request.user.is_authenticated():
						user = request.user
					obj, created = Smpl.objects.get_or_create(user=user, url=url)
					analytic_obj, iscreated = Analytic.objects.get_or_create(url=obj)
					if obj:						
						obj_list.append(obj)
						print(get_current_site(request))				
					if created:
						# created_list.append(created)														
						messages.add_message(
							request, 
							messages.SUCCESS, 
							# '%s/%s' % (get_current_site(request), obj.shortcode),
							'<a href="%s" target="_blank">%s/%s</a>' % (obj.get_short_url(), get_current_site(request), obj.shortcode),
							# '<a href="%s/%s" target="_blank">%s/%s</a>' % (get_current_site(request), obj.shortcode, get_current_site(request), obj.shortcode),
							extra_tags='label label-success'
							)
					else:
						messages.info(
							request, 
							'This URL has already been shorten.', 
							extra_tags='label label-info'
							)
						messages.add_message(
							request, 
							messages.INFO, 	
							'<a href="%s" target="_blank">%s/%s</a>' % (obj.get_short_url(), get_current_site(request), obj.shortcode), 
							# '<a href="%s" target="_blank">%s/%s</a><span class="badge">Vistied : %i</span>' % (obj.get_short_url(), get_current_site(request), obj.shortcode, int(analytic_obj.count)),
							# '<a href="%s/%s" target="_blank">%s/%s</a>' % (get_current_site(request), obj.shortcode, get_current_site(request), obj.shortcode),
							extra_tags='label label-default text-center'
							)					
				# return HttpResponseRedirect(reverse('shortener:multi'))
		return render(request, template, context)

class SmplRedirectCBV(View):
	def get(self, request, shortcode=None, *args, **kwargs):
		if shortcode is not None:
			queryset = Smpl.objects.filter(shortcode__iexact=shortcode)
		if not queryset.exists() and queryset.count() != 1:
			return Http404
		obj = queryset.first()
		url = obj.url
		if 'http' not in url and 'https' not in url:
			url = 'http://' + url
		Analytic.objects.click_count(obj)
		return HttpResponseRedirect(url)
		
		
