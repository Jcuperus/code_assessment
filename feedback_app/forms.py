from django import forms

class CodeUploadForm(forms.Form):
    code_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))