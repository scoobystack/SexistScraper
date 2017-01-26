from django import forms

class JobProviderForm(forms.Form):
    # site = forms.CharField(label='Indeed', max_length=100)
    query = forms.CharField(label='Query', max_length=100)
    location = forms.CharField(label='Location', max_length=100)
    count = forms.IntegerField(label='Count', min_value=25, max_value=500)
