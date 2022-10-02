from django import forms
from .models import Receipts
from django.contrib.auth import get_user_model

class ReceiptRatingForm(forms.Form):
    receipt = forms.ModelChoiceField(queryset=Receipts.objects.all(), disabled=True)
    score = forms.IntegerField()
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), disabled=True)
    text = forms.CharField(widget=forms.Textarea)
