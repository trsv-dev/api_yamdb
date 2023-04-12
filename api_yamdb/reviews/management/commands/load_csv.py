from sqlite3 import IntegrityError

from django.core.management.base import BaseCommand, CommandError

from reviews.management.commands._load_cvs_func import load_func


class Command(BaseCommand):
    """
    Наполнение БД тестовыми данными из .csv
    """
    help = 'Загрузка тестовых файлов .csv в базу sqlite3'

    def handle(self, *args, **options):
        try:
            load_func(self)

        except IntegrityError:
            raise CommandError(
                f'База данных нуждается в очистке '
                f'перед импортом. Удалите базу данных '
                f'и выполните "python manage.py migrate"'
            )

        except FileNotFoundError:
            raise CommandError(
                'Файлы формата .csv в static/data не найдены')

        except Exception:
            raise CommandError(
                'Неожиданная ошибка работы импорта load_csv,'
            )

        self.stdout.write(self.style.SUCCESS(
            'Все данные из .csv файлов загружены в базу данных'
        ))
