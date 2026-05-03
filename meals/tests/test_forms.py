from django.test import TestCase
from meals.forms import MealRatingForm
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image

class FormTests(TestCase):
    def setUp(self):
        # 1. メモリ上にダミーの有効な画像を作成する
        image_file = BytesIO()
        image = Image.new('RGB', (100, 100), color='white') # 100x100の真っ白な画像
        image.save(image_file, 'JPEG')
        image_file.seek(0) # ファイルポインタを先頭に戻す
        
        # 2. 生成した有効な画像データをSimpleUploadedFileに渡す
        self.image = SimpleUploadedFile(
            name="test.jpg",
            content=image_file.read(),
            content_type="image/jpeg",
        )
        
    def test_valid_data_is_valid_in_MealRatingForm(self):
        form_data = {
            "rating": "5", 
            "comment": "Delicious meal!",
        }
        
        form = MealRatingForm(data=form_data, files={"image": self.image})
        self.assertTrue(form.is_valid(), form.errors)
        
    def test_invalid_data_is_not_valid_in_MealRatingForm(self):
        form_data = {
            "rating": "6",  # Invalid rating (should be between 1 and 5)
            "comment": "Too good to be true!",
        }
        
        form = MealRatingForm(data=form_data, files={"image": self.image})
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)
        
    def test_empty_data_is_not_valid_in_MealRatingForm(self):
        form = MealRatingForm(data={}, files={"image": self.image})
        self.assertFalse(form.is_valid())
        self.assertIn("rating", form.errors)
        
    def test_image_field_is_optional_in_MealRatingForm(self):
        form_data = {
            "rating": 4, 
            "comment": "Pretty good meal.",
        }
        
        form = MealRatingForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_comment_field_is_optional_in_MealRatingForm(self):
        form_data = {
            "rating": 3, 
        }
        
        form = MealRatingForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    