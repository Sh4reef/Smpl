from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class URLForm(forms.Form):
	url = forms.CharField(
		required=False,
		label='', 
		widget=forms.TextInput(
			attrs={'class': 'form-control', 'placeholder': 'Long URL'}
			)
		)

	def clean_url(self):
		url = self.cleaned_data.get('url')
		urlvalidator = URLValidator()
		if 'http' not in url and 'https' not in url:
			url = 'http://' + url	
		try:
			urlvalidator(url)
		except:
			raise ValidationError('Invalid URL')
		return url

class MultiURLForm(forms.Form):
	multiurl = forms.CharField(
		required=False,
		label='',
		widget=forms.Textarea(
			attrs={'class': 'form-control', 'placeholder': 'Multi URL'}
			)
		)

	def clean_multiurl(self):
		urls = self.cleaned_data.get('multiurl')
		urlvalidator = URLValidator()
		url_list = urls.rsplit()
		line_count = 0
		new_url_list = []
		for url in url_list:
			line_count += 1
			if 'http' not in url and 'https' not in url:
				url = 'http://' + url	
			try:
				urlvalidator(url)
				new_url_list.append(url)
			except:
				raise ValidationError('Invalid URL #' + url[0:50] + '.... ' + '#line ' + str(line_count))		
		return new_url_list
