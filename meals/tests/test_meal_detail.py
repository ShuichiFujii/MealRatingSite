from django.test import TestCase
from django.urls import reverse
from meals.models import Meal, MealRating
from meals.forms import MealRatingForm

class MealDetailViewTests(TestCase):
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
        
    def test_invalid_id_returns_404(self):
        response = self.client.get(reverse('meal_detail', kwargs={'meal_id': 999}))
        self.assertEqual(response.status_code, 404)
        
    def test_valid_id_returns_200(self):
        response = self.client.get(reverse('meal_detail', kwargs={'meal_id': self.meal1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.meal1.name)
        self.assertContains(response, self.meal1.description)
        
    def test_correct_template_used(self):
        response = self.client.get(reverse('meal_detail', kwargs={'meal_id': self.meal1.id}))
        self.assertTemplateUsed(response, 'meals/meal_detail.html')
        
    def test_context_contains_meal(self):
        response = self.client.get(reverse('meal_detail', kwargs={'meal_id': self.meal1.id}))
        self.assertEqual(response.context['meal_detail'], self.meal1)
        self.assertIsInstance(response.context['meal_detail'], Meal)
        
    def test_context_contains_rating_form(self):
        response = self.client.get(reverse('meal_detail', kwargs={'meal_id': self.meal1.id}))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], MealRatingForm)
    
    def test_post_valid_rating_creates_rating(self):
        before_post_count = self.meal1.ratings.count()
        
        form_data = {
            'rating': 5,
            'comment': 'Great meal!'
        }
        
        response = self.client.post(
            reverse('meal_detail', kwargs={'meal_id': self.meal1.id}), 
            data=form_data,
        )
        self.meal1.refresh_from_db()
        after_post_count = self.meal1.ratings.count()
        self.assertEqual(after_post_count, before_post_count + 1)

        new_rating = self.meal1.ratings.last()
        self.assertEqual(new_rating.meal, self.meal1)
        
        self.assertRedirects(
            response, 
            reverse('meal_detail', kwargs={'meal_id': self.meal1.id})
        )


    def test_empty_rating_does_not_create_rating(self):
        before_post_count = MealRating.objects.count()

        response = self.client.post(
            reverse('meal_detail', kwargs={'meal_id': self.meal1.id}),
            data={'rating': ''}
        )

        after_post_count = MealRating.objects.count()

        self.assertEqual(after_post_count, before_post_count)
        self.assertEqual(response.status_code, 200)