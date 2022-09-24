from django.core.management.base import BaseCommand, CommandError
from currency.models import Rate


class Command(BaseCommand):
    help = 'Get rate by rate_id and print to console'

    def add_arguments(self, parser):
        parser.add_argument('rate_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for rate_id in options['rate_ids']:
            try:
                rate = Rate.objects.get(pk=rate_id)
            except Rate.DoesNotExist:
                raise CommandError('Rate "%s" does not exist' % rate_id)

            currency_type = rate.currency_type

            self.stdout.write(self.style.SUCCESS(f'Object {rate_id} has currency_type = {currency_type}'))