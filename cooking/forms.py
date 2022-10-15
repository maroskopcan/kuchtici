from django import forms
from .models import Receipt, ReceiptRating
from django.contrib.auth import get_user_model

class ReceiptRatingForm(forms.Form):
    receipt = forms.ModelChoiceField(queryset=Receipt.objects.all())
    score = forms.IntegerField(min_value=0, max_value=10)
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all())
    text = forms.CharField(widget=forms.Textarea)

class ReceiptRatingUpdateForm(forms.ModelForm):
    class Meta:
        model = ReceiptRating
        fields = ("score", "text")