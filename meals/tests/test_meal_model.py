from django.test import TestCase
from meals.models import Meal

class MealModelTestCase(TestCase):
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
        
    
    def test_meal_str_method(self):
        self.assertEqual(str(self.meal1), "Meal 1")
        
    def test_update_rating_stats(self):
        # 最初は評価がない状態
        self.assertEqual(self.meal1.average_rating, 0.0)
        self.assertEqual(self.meal1.number_of_votes, 0)

        # 評価を追加
        self.meal1.ratings.create(rating=4)
        self.meal1.ratings.create(rating=5)

        # 評価統計を更新
        self.meal1.update_rating_stats()

        # 平均評価と投票数が正しく更新されているか確認
        self.assertEqual(self.meal1.average_rating, 4.5)
        self.assertEqual(self.meal1.number_of_votes, 2)
    
    def test_rating_zero_votes(self):
        self.assertEqual(self.meal1.average_rating, 0.0)
        self.assertEqual(self.meal1.number_of_votes, 0)