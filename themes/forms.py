# coding=utf-8
from django import forms

from .models import Themes

class BasicElemetsForm(forms.ModelForm):
	MAX_UPLOAD_SIZE = 2*1024*1024

	def clean_favicon(self):
		image = self.cleaned_data.get('favicon', False)

		if image:
			if hasattr(image, '_size'):
				if image._size > self.MAX_UPLOAD_SIZE:
					self._errors['favicon'] = [_("The image is too large. It should have less than 2MB.")]

					return ValueError

		return image

	def clean_small_logo(self):
		image = self.cleaned_data.get('small_logo', False)

		if image:
			if hasattr(image, '_size'):
				if image._size > self.MAX_UPLOAD_SIZE:
					self._errors['small_logo'] = [_("The image is too large. It should have less than 2MB.")]

					return ValueError

		return image

	def clean_large_logo(self):
		image = self.cleaned_data.get('large_logo', False)

		if image:
			if hasattr(image, '_size'):
				if image._size > self.MAX_UPLOAD_SIZE:
					self._errors['large_logo'] = [_("The image is too large. It should have less than 2MB.")]

					return ValueError

		return image
	
	class Meta:
		model = Themes
		fields = ['title', 'favicon', 'small_logo', 'large_logo', 'footer_note']

class CSSStyleForm(forms.ModelForm):

	class Meta:
		model = Themes
		fields = ['css_style']
		widgets = {
			'css_style': forms.RadioSelect
		}