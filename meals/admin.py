from django.contrib import admin
from .models import Meal, MealRating


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country_of_origin",
        "typical_meal_time",
        "average_rating",
        "number_of_votes",
    )
    list_filter = ("typical_meal_time", "country_of_origin")
    search_fields = ("name", "country_of_origin")


@admin.register(MealRating)
class MealRatingAdmin(admin.ModelAdmin):
    list_display = (
        "meal",
        "rating",
        "date_of_rating",
    )
    list_filter = ("rating", "date_of_rating")
    search_fields = ("meal__name", "comment")