import csv

from django.core.management.base import BaseCommand

from api_yamdb.settings import BASE_DIR
from reviews.models import Category, Comment, Genre, Review, Title, User

CSV_DATA = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


class Command(BaseCommand):
    help = 'Загрузка тестовых файлов .csv в базу sqlite3'

    def handle(self, *args, **options):
        for model, file_csv in CSV_DATA.items():

            with open(
                    f'{BASE_DIR}/static/data/{file_csv}',
                    'r', encoding='utf-8'
            ) as file:
                data = csv.DictReader(file)
                lst = []

                for row in data:
                    if 'category' in row:
                        row['category_id'] = row.pop('category')
                    elif 'author' in row:
                        row['author_id'] = row.pop('author')
                    lst.append(model(**row))

                model.objects.bulk_create(lst)

        return 'Данные успешно загружены'
