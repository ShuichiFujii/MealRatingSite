from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
    path("category/<str:category>/", views.category_list, name="category_list"),
    path("meal/<int:meal_id>/", views.meal_detail, name="meal_detail"),
]
