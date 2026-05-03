from django.core.management.base import BaseCommand
from django.db.models import Avg, Count

from meals.models import Meal


class Command(BaseCommand):
    help = "Update average_rating and number_of_votes for all meals"

    def handle(self, *args, **options):
        meals = Meal.objects.all()

        for meal in meals:
            stats = meal.ratings.aggregate(
                avg_rating=Avg("rating"),
                vote_count=Count("id")
            )

            meal.average_rating = stats["avg_rating"] or 0
            meal.number_of_votes = stats["vote_count"] or 0
            meal.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully updated meal rating stats.")
        )