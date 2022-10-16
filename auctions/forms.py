from django import forms
from .models import Listing, Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'description', 'image', 'starting_bid']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control mb-3'}),
                    'category' : forms.Select(choices=Category.objects.all(), attrs={'class' : 'form-control mb-3'}),
                    'description': forms.TextInput(attrs={'class': 'form-control mb-3'}),
                    'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
                    'starting_bid': forms.NumberInput(attrs={'class': 'form-control mb-3'})}

