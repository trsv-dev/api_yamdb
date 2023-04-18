import csv
import sys
import time

from api_yamdb.settings import BASE_DIR
from reviews.models import (Category, Comment, Genre,
                            Review, Title, User, GenreTitle)

CSV_DATA = {

    Category: 'category.csv',
    Genre: 'genre.csv',
    User: 'users.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def sleep_period(sec):
    for i in range(sec, 0, -1):
        sys.stdout.write(str(i) + ' ')
        sys.stdout.flush()
        time.sleep(1)


def load_func(self, *args, **options):

    self.stdout.write(self.style.WARNING(
        'Перед загрузкой тестовых данных БД будет очищена. '
        'Чтобы отменить операцию импорта нажмите Ctrl + C'
    ))
    sleep_period(7)

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

            # очищаем базу от старых данных перед импортом
            model.objects.all().delete()
            # наполняем новыми данными
            model.objects.bulk_create(lst)

            print(f'Файл {file_csv} загружен')
