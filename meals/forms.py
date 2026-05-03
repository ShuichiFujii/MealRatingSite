from django import forms
from .models import MealRating, Meal


class MealRatingForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label="Your rating"
    )
    
    comment = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={
            "placeholder": "Share your thoughts about this meal", 
            "maxlength": 300
        })
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "image-input"
        })
    )
    
    class Meta:
        model = MealRating
        fields = ["rating", "comment", "image"]
        
class MealForm(forms.ModelForm):
    
    class Meta:
        model = Meal
        fields = ["name", "description", "image", "country_of_origin", "typical_meal_time"]
        