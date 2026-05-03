from django.test import TestCase
from meals.models import Meal
from django.utils import timezone
from datetime import timedelta

from meals.views import (
    _get_meals_by_category, 
    _get_sort_options
)

class CategoryListViewTests(TestCase):
    def setUp(self):
        # テスト用データの作成
        self.meal1 = Meal.objects.create(
            name="Meal 1",
            description="Description for Meal 1",
            country_of_origin="Country A",
            typical_meal_time=1,
            average_rating=3.0, 
            number_of_votes=10
        )
        self.meal2 = Meal.objects.create(
            name="Meal 2",
            description="Description for Meal 2",
            country_of_origin="Country B",
            typical_meal_time=2,
            average_rating=3.0,
            number_of_votes=10
        )
        self.meal3 = Meal.objects.create(
            name="Meal 3",
            description="Description for Meal 3",
            country_of_origin="Country C",
            typical_meal_time=3,
            average_rating=3.0, 
            number_of_votes=10
        )
        
    def test_get_morning_meals(self):
        meals = _get_meals_by_category("morning")
        self.assertIn(self.meal1, meals)
        self.assertNotIn(self.meal2, meals)
        self.assertNotIn(self.meal3, meals)
        
        meal4 = Meal.objects.create(
            name="Meal 4",
            description="Description for Meal 4",
            country_of_origin="Country D",
            typical_meal_time=1,
            average_rating=4.0,
            number_of_votes=15
        )
        
        meals = list(_get_meals_by_category("morning"))
        self.assertEqual(meals[0], meal4)
        self.assertEqual(meals[1], self.meal1)

    def test_get_afternoon_meals(self):
        meals = _get_meals_by_category("afternoon")
        self.assertIn(self.meal2, meals)
        self.assertNotIn(self.meal1, meals)
        self.assertNotIn(self.meal3, meals)
        
        meal4 = Meal.objects.create(
            name="Meal 4",
            description="Description for Meal 4",
            country_of_origin="Country D",
            typical_meal_time=2,
            average_rating=4.0,
            number_of_votes=15
        )
        
        meals = list(_get_meals_by_category("afternoon"))
        self.assertEqual(meals[0], meal4)
        self.assertEqual(meals[1], self.meal2)


    def test_get_evening_meals(self):
        meals = _get_meals_by_category("evening")
        self.assertIn(self.meal3, meals)
        self.assertNotIn(self.meal1, meals)
        self.assertNotIn(self.meal2, meals)
        
        meal4 = Meal.objects.create(
            name="Meal 4",
            description="Description for Meal 4",
            country_of_origin="Country D",
            typical_meal_time=3,
            average_rating=4.0,
            number_of_votes=15
        )
        
        meals = list(_get_meals_by_category("evening"))
        self.assertEqual(meals[0], meal4)
        self.assertEqual(meals[1], self.meal3)

        
    def test_invalid_category_returns_empty_Meal_objects(self):
        meals = _get_meals_by_category("invalid_category")
        self.assertEqual(meals.count(), 0)
        
    def test_top_rated_meals(self):
        top_rated = Meal.objects.create(
            name="Top Rated Meal",
            description="Excellent",
            country_of_origin="Country C",
            typical_meal_time=3,
            average_rating=4.8,
            number_of_votes=20
        )
        
        high_rated = Meal.objects.create(
            name="High Rated Meal",
            description="Good",
            country_of_origin="Country D",
            typical_meal_time=1,
            average_rating=4.5,
            number_of_votes=15
        )

        low_rated = Meal.objects.create(
            name="Low Rated Meal",
            description="Not bad",
            country_of_origin="Country E",
            typical_meal_time=2,
            average_rating=3.5,
            number_of_votes=10
        )

        meals = _get_meals_by_category("top_rated")

        self.assertIn(top_rated, meals)
        self.assertIn(high_rated, meals)
        self.assertNotIn(low_rated, meals)
        self.assertNotIn(self.meal1, meals)
        
        self.assertEqual(meals[0], top_rated)
        self.assertEqual(meals[1], high_rated)
    
    def test_get_recent_meals(self):
        recent_meal = Meal.objects.create(
            name="Recent Meal",
            description="Recent",
            country_of_origin="Country R",
            typical_meal_time=1,
        )

        old_meal = Meal.objects.create(
            name="Old Meal",
            description="Old",
            country_of_origin="Country O",
            typical_meal_time=1,
        )

        # old meal を昔の日付に変更
        Meal.objects.filter(id=old_meal.id).update(
            date_added=timezone.now() - timedelta(days=100)
        )

        old_meal.refresh_from_db()

        meals = list(_get_meals_by_category("recent"))

        self.assertIn(recent_meal, meals)
        self.assertIn(old_meal, meals)

        self.assertLess(
            meals.index(recent_meal),
            meals.index(old_meal)
        )
        
    def test_get_sorted_meals_by_rating(self):
        top_rated = Meal.objects.create(
            name="Top Rated Meal",
            description="Excellent",
            country_of_origin="Country C",
            typical_meal_time=3,
            average_rating=4.8,
            number_of_votes=20
        )
        
        meals = Meal.objects.all()
        sorted_meals = list(_get_sort_options("rating", meals))

        self.assertEqual(sorted_meals[0], top_rated)
        
    def test_get_sorted_meals_by_country(self):
        meals = Meal.objects.all()

        sorted_meals = list(_get_sort_options("country", meals))

        self.assertEqual(sorted_meals[0].country_of_origin, "Country A")
        
    def test_get_invalid_sort_option_returns_original_meals(self):
        meals = Meal.objects.order_by("id")
        sorted_meals = _get_sort_options("invalid", meals)

        self.assertEqual(list(sorted_meals), list(meals))