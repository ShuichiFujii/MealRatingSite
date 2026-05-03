from django.test import TestCase
from django.urls import reverse
from meals.models import Meal

class LandingPageViewTests(TestCase):
    def setUp(self):
        # テスト用データの作成
        self.meal1 = Meal.objects.create(
            name="Meal 1",
            description="Description for Meal 1",
            country_of_origin="Country A",
            typical_meal_time=1,
        )
        self.meal2 = Meal.objects.create(
            name="Meal 2",
            description="Description for Meal 2",
            country_of_origin="Country B",
            typical_meal_time=2,
        )
        self.meal3 = Meal.objects.create(
            name="Meal 3",
            description="Description for Meal 3",
            country_of_origin="Country C",
            typical_meal_time=3,
        )
        
    # テストケース: ランディングページが正しく表示されることを確認する
    def test_landing_page_returns_200_and_uses_template(self):
        response = self.client.get(reverse("landing"))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "meals/index.html")
        
    # テストケース: 含まれる食事が正しいことを確認する
    def test_meals_are_passed_to_context_by_meal_time(self):
        response = self.client.get(reverse("landing"))
        
        self.assertIn(self.meal1, response.context["morning_meals"])
        self.assertIn(self.meal2, response.context["afternoon_meals"])
        self.assertIn(self.meal3, response.context["evening_meals"])
        
    # テストケース: フォームが正しく表示されることを確認する
    def test_form_displayed(self):
        response = self.client.get(reverse("landing"))
        
        self.assertIn("meal_form", response.context)
        
    # テストケース: フォームの送信が正しく処理されることを確認する
    def test_form_submission(self):
        data = {
            "name": "New Meal", 
            "description": "Description for New Meal", 
            "country_of_origin": "Country D", 
            "typical_meal_time": 1
        }
        
        response = self.client.post(reverse("landing"), data)
        
        self.assertRedirects(response, reverse("landing"))
        self.assertTrue(Meal.objects.filter(name="New Meal").exists())
    
    