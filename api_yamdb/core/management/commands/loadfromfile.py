import csv
import os
from typing import Any, List

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from reviews.models import Category, Comment, Genre, Review, Title, User

model_by_filename = [
    ('category', Category),
    ('genre', Genre),
    ('titles', Title),
    ('users', User),
    ('review', Review),
    ('comments', Comment),
]


class Command(BaseCommand):
    help = 'Load data from csv files into database.'

    @staticmethod
    def is_related(model_object: Any, field_name: Any) -> bool:
        """Model field is related to foreign key."""
        field = model_object._meta.get_field(field_name)
        return field.is_relation

    @staticmethod
    def add_suffix_for_related(model: Any, keys: List[str]) -> None:
        """Add id suffix for all related fields."""
        instance = model()
        for count, field_name in enumerate(keys):
            if 'id' in field_name:
                continue
            if Command.is_related(instance, field_name):
                keys[count] += "_id"

    def handle(self, *args, **options):
        """Load data from csv files to database."""
        error_stream = self.stderr.write
        output_stream = self.stdout.write

        for filename, model in model_by_filename:
            filename += '.csv'
            path = os.path.join(settings.STATIC_DATA, filename)
            try:
                with open(path, encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=',')
                    keys = reader.fieldnames
                    Command.add_suffix_for_related(model, keys)
                    update, error = False, False
                    for row in reader:
                        object, created = model.objects.update_or_create(**row)
                        if not object:
                            error = True
                        elif not created:
                            update = True
            except IntegrityError:
                error_stream(self.style.ERROR(
                    f'Not load {model.__name__}.'
                    'Integrity error. Ensure order of loading files '
                    'or succesful previously models load')
                )
                continue

            except FileNotFoundError:
                error_stream(self.style.ERROR(
                    f'Not load. File {path} not found.')
                )
                continue

            if error:
                error_stream(self.style.ERROR(f'Not load {model.__name__}'))
            elif update:
                output_stream(self.style.SUCCESS(f'Update {model.__name__}'))
            else:
                output_stream(self.style.SUCCESS(f'Created {model.__name__}'))
