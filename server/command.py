from django.core.management.base import BaseCommand
from myapp.views.index.models import Activity

class Command(BaseCommand):
    help = 'Initialize database tables'

    def handle(self, *args, **options):
        Activity.init_table()
        self.stdout.write(self.style.SUCCESS('Database tables created'))