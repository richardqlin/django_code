from django import forms

from .models import User,Rental

class RentalForm(forms.ModelForm):
	class Meta:
		model=Rental
		fields='__all__'

