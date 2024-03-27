from django import forms
from .models import Recipient

class FileUpload(forms.ModelForm):
	file = forms.FileField()

	class Meta:
		model = Recipient
		fields = "__all__"


	def __init__(self,*args,**kwargs):
		super().__init__(*args, **kwargs)

		self.fields['file'].label = ""