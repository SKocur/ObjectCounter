from django import forms

class ImageFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()