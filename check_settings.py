# blogsite/yourapp/management/commands/checksettings.py

from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Check Django settings'

    def handle(self, *args, **kwargs):
        # 1. Check Django Settings
        if hasattr(settings, 'CSRF_FAILURE_VIEW'):
            # CSRF_FAILURE_VIEW is defined
            csrf_failure_view = settings.CSRF_FAILURE_VIEW
            self.stdout.write(f"CSRF failure view is set to: {csrf_failure_view}")
        else:
            # CSRF_FAILURE_VIEW is not defined
            self.stdout.write("CSRF failure view is not defined in Django settings.")

        # 2. Set Environment Variable (this should be done outside of the script)
        # 3. Call settings.configure() (if necessary, depending on where you run the script)
