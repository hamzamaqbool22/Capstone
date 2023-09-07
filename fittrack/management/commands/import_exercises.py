import csv
from django.core.management.base import BaseCommand
from fittrack.models import Exercise

class Command(BaseCommand):
    help = 'Import exercises from csv files'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='fittrack\csv\exercises.csv')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row if it exists

                for row in reader:
                    exercise_name = row[0]  # Assuming the exercise name is in the first column
                    created = Exercise.objects.get_or_create(name=exercise_name)
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created Exercise: {exercise_name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Exercise already exists: {exercise_name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))