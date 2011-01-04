from django.core.management.base import BaseCommand
from browsecap.filehandler import BrowseCapImport

class Command(BaseCommand):
    help = """
        retrieve_browsecap will retrieve the latest ini file from Gary Keith
    """
    
    def handle(self, *args, **options):
        BrowseCapImport()