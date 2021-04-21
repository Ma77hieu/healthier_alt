from django.core.management.base import BaseCommand, CommandError
from substitution.models import Product, Categories, Favorites


class Command(BaseCommand):
    help = "Erase all data from the database's tables except the user table"

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        # for poll_id in options['poll_ids']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)

        #     poll.opened = False
        #     poll.save()

        favorite = Favorites.objects.all()
        favorite.delete()
        product = Product.objects.all()
        product.delete()
        category = Categories.objects.all()
        category.delete()
        self.stdout.write(self.style.SUCCESS(
            ' Successfully erased databases '))
