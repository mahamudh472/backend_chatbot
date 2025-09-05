from django.core.management.base import BaseCommand
from django.conf import settings
import os
from chat.vectorstore import VectorStore


class Command(BaseCommand):
    help = 'Rebuild the vector store with chunked documents'

    def add_arguments(self, parser):
        parser.add_argument(
            '--chunk-size',
            type=int,
            default=500,
            help='Size of each chunk in characters (default: 500)'
        )
        parser.add_argument(
            '--chunk-overlap',
            type=int,
            default=50,
            help='Overlap between chunks in characters (default: 50)'
        )
        parser.add_argument(
            '--show-stats',
            action='store_true',
            help='Show statistics about the vector store after building'
        )

    def handle(self, *args, **options):
        chunk_size = options['chunk_size']
        chunk_overlap = options['chunk_overlap']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Building vector store with chunk_size={chunk_size}, chunk_overlap={chunk_overlap}'
            )
        )

        # Create new vector store with specified parameters
        vector_store = VectorStore(
            dim=768, 
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )

        # Load documents from the documents folder
        docs_folder = os.path.join(settings.BASE_DIR, 'documents')
        
        if not os.path.exists(docs_folder):
            self.stdout.write(
                self.style.ERROR(f'Documents folder not found: {docs_folder}')
            )
            return

        self.stdout.write('Loading and chunking documents...')
        vector_store.load_from_folder(docs_folder)

        if options['show_stats']:
            stats = vector_store.get_stats()
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nVector Store Statistics:\n'
                    f'- Total chunks: {stats["total_chunks"]}\n'
                    f'- Total files: {stats["total_files"]}\n'
                    f'- Files processed: {", ".join(stats["files"])}'
                )
            )

        self.stdout.write(
            self.style.SUCCESS('Vector store rebuilt successfully!')
        )
        
        # Test search functionality
        self.stdout.write('\nTesting search functionality...')
        test_results = vector_store.search("API documentation", top_k=2)
        
        for i, result in enumerate(test_results, 1):
            metadata = result.get('metadata', {})
            filename = metadata.get('filename', 'Unknown')
            chunk_idx = metadata.get('chunk_index', 'N/A')
            distance = result.get('distance', 'N/A')
            
            self.stdout.write(
                f'  {i}. {filename} (chunk {chunk_idx}, distance: {distance:.4f})'
            )
