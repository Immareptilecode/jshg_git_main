from django import forms


class date_form(forms.Form):
	date=forms.DateField(widget=forms.DateInput(attrs={ 'type':"date"}))