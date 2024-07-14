# myapp/forms.py
from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()

class SearchForm(forms.Form):
    Food = forms.CharField(max_length=100, required=True)