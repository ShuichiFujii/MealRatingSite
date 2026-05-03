from django.shortcuts import render, get_object_or_404, redirect
from .models import Meal
from .forms import MealRatingForm, MealForm
from django.core.paginator import Paginator
from datetime import timezone, timedelta
from django.utils import timezone
import json
    
def _meal_to_dict(meal):
    return {
        "id": meal.id,
        "name": meal.name,
        "average_rating": float(meal.average_rating) if meal.average_rating is not None else None,
        "image": meal.image.url if meal.has_image else None,
    }

def landing_page(request):
    if request.method == "POST":
        meal_form = MealForm(request.POST, request.FILES)
        if meal_form.is_valid():
            meal_form.save()
            return redirect("landing")
    else:
        meal_form = MealForm()

    morning_all   = list(Meal.objects.filter(typical_meal_time=1).order_by("-average_rating"))
    afternoon_all = list(Meal.objects.filter(typical_meal_time=2).order_by("-average_rating"))
    evening_all   = list(Meal.objects.filter(typical_meal_time=3).order_by("-average_rating"))
    recent_all    = list(Meal.objects.order_by("-date_added"))
    top_rated_all = list(Meal.objects.order_by("-average_rating"))

    sections = [
        {"category": "morning_meals",   "label": "Morning",        "meals": morning_all[:3]},
        {"category": "afternoon_meals", "label": "Afternoon",      "meals": afternoon_all[:3]},
        {"category": "evening_meals",   "label": "Evening",        "meals": evening_all[:3]},
        {"category": "recent_meals",    "label": "Recently Added", "meals": recent_all[:3]},
        {"category": "top_rated_meals", "label": "Top Rated",      "meals": top_rated_all[:3]},
    ]

    section_data = {
        "morning_meals":   [_meal_to_dict(m) for m in morning_all],
        "afternoon_meals": [_meal_to_dict(m) for m in afternoon_all],
        "evening_meals":   [_meal_to_dict(m) for m in evening_all],
        "recent_meals":    [_meal_to_dict(m) for m in recent_all],
        "top_rated_meals": [_meal_to_dict(m) for m in top_rated_all],
    }

    data = {
        "sections": sections,
        "section_data_json": json.dumps(section_data),
        "morning_meals": morning_all[:3],
        "afternoon_meals": afternoon_all[:3],
        "evening_meals": evening_all[:3],
        "recent_meals": recent_all[:3],
        "top_rated_meals": top_rated_all[:3],
        "meal_form": meal_form,
    }

    return render(request, "meals/index.html", data)

def _get_meals_by_category(category):
    category_map = {
        "morning": 1,
        "afternoon": 2,
        "evening": 3
    }
    
    if category in category_map:
        return Meal.objects.filter(
            typical_meal_time=category_map[category]
        ).order_by("-average_rating")

    elif category == "recent":
        now = timezone.now()
        return Meal.objects.filter(
            date_added__gte=now - timedelta(days=90)
        ).order_by("-date_added")

    elif category == "top_rated":
        return Meal.objects.filter(
            average_rating__gte=4.0
        ).order_by("-average_rating")

    else:
        return Meal.objects.none()

def _get_sort_options(sort, meals):
    if sort == "recent":
        return meals.order_by("-date_added")
        
    elif sort == "rating":
        return meals.order_by("-average_rating")
        
    elif sort == "country":
        return meals.order_by("country_of_origin")
    
    else:
        return meals

def category_list(request, category):
    meals = _get_meals_by_category(category)
    sort = request.GET.get("sort")
    sorted_meals = _get_sort_options(sort, meals)

    page_number = request.GET.get("page", 1)
    paginator = Paginator(sorted_meals, 6)
    page_obj = paginator.get_page(page_number)

    data = {
        "meals": page_obj,
        "page_obj": page_obj,
        "category": category,
        "current_sort": sort or "",
    }

    return render(request, "meals/category_list.html", data)


def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    
    if request.method == "POST":
        form = MealRatingForm(request.POST, request.FILES)
        if form.is_valid():
            meal_rating = form.save(commit=False) 
            meal_rating.meal = meal
            meal_rating.save()
            
            meal.update_rating_stats()
            
            return redirect("meal_detail", meal_id=meal.id)
            
    else:
        # 空のフォームを作成する
        form = MealRatingForm()
    
    send_data = {
        "meal_detail": meal,
        "form": form
    }
    
    return render(request, "meals/meal_detail.html", send_data)