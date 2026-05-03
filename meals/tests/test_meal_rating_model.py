from django.test import TestCase
from meals.models import Meal
from datetime import timedelta
from django.utils import timezone
from meals.models import MealRating

class MealRatingModelTestCase(TestCase):
    def setUp(self):
        self.meal = Meal.objects.create(
            name="Test Meal",
            description="A meal for testing.",
            country_of_origin="Test Country",
            typical_meal_time=1,
        )
        
    def test_related_name_ratings(self):
        self.assertEqual(self.meal.ratings.count(), 0)
        
        rating1 = self.meal.ratings.create(rating=4)
        rating2 = self.meal.ratings.create(rating=5)
        
        self.assertEqual(self.meal.ratings.count(), 2)
        self.assertIn(rating1, self.meal.ratings.all())
        self.assertIn(rating2, self.meal.ratings.all())
    
    def test_ordering_by_date_of_rating(self):
        rating1 = self.meal.ratings.create(rating=3)
        rating2 = self.meal.ratings.create(rating=5)
        
        # 時間を少しずらす
        MealRating.objects.filter(id=rating1.id).update(
            date_of_rating=timezone.now() - timedelta(days=1)
        )
        
        ratings = list(self.meal.ratings.all())
        
        self.assertEqual(ratings[0], rating2)  # 最新の評価が最初に来る
        self.assertEqual(ratings[1], rating1)  # 古い評価が次に来る