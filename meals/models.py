from django.db import models
from django.db.models import Avg, Count
import os

class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='meals/', 
        blank=True, 
        null=True
    )
    country_of_origin = models.CharField(max_length=100, blank=True)
    typical_meal_time = models.IntegerField(
        choices=[
            (1, "morning"),
            (2, "afternoon"),
            (3, "evening"),
        ]
    )
    date_added = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0.0)
    number_of_votes = models.IntegerField(default=0)

    @property
    def has_image(self):
        return bool(self.image and self.image.name and os.path.isfile(self.image.path))

    def update_rating_stats(self):
        stats = self.ratings.aggregate(
            average_rating=Avg("rating"),
            number_of_votes=Count("id")
        )

        self.average_rating = stats["average_rating"] or 0.0
        self.number_of_votes = stats["number_of_votes"]
        self.save(update_fields=["average_rating", "number_of_votes"])
    
    def __str__(self):
        return self.name
    
class MealRating(models.Model):
    meal = models.ForeignKey(
        Meal, 
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    
    image = models.ImageField(
        upload_to='reviews/meal_ratings/', 
        blank=True, 
        null=True
    )
    
    rating = models.IntegerField(
        choices=[
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ]
    )
    
    date_of_rating = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    
    class Meta:
        ordering = ["-date_of_rating"]
        verbose_name = "Meal Rating"
        verbose_name_plural = "Meal Ratings"