from django import forms
from .models import Listing, Comment


class ListingForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "width": 10})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "width": 10})
    )

    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "price", "category", "image"]


class CommentForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "width": 10})
    )

    class Meta:
        model = Comment
        fields = ["description"]
