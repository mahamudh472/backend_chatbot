from django.core.management.base import BaseCommand
from chat.views import get_vector_store

class Command(BaseCommand):
    help = 'Test vectorstore loading behavior'

    def handle(self, *args, **options):
        self.stdout.write("Testing vectorstore loading...")
        
        vector_store = get_vector_store()
        
        if vector_store is None:
            self.stdout.write(
                self.style.WARNING("Vectorstore is None - this is expected for management commands that don't need it")
            )
        else:
            stats = vector_store.get_stats()
            self.stdout.write(
                self.style.SUCCESS(f"Vectorstore loaded successfully! Stats: {stats}")
            )
