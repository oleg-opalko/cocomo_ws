from django.core.management.base import BaseCommand
from main.models import ScaleDriver, CostDriver
from main.constants import RATING_CHOICES, CATEGORY_CHOICES

class Command(BaseCommand):
    help = 'Loads initial data for Scale Drivers and Cost Drivers'

    def handle(self, *args, **kwargs):
        # Scale Drivers
        scale_drivers = [
            {
                'name': 'Precedentedness',
                'description': 'The extent to which the project is similar to previously developed projects',
                'weight': 0.91
            },
            {
                'name': 'Development Flexibility',
                'description': 'The extent to which the project can be developed with flexibility',
                'weight': 0.91
            },
            {
                'name': 'Architecture/Risk Resolution',
                'description': 'The extent to which the architecture and risk resolution is handled',
                'weight': 0.91
            },
            {
                'name': 'Team Cohesion',
                'description': 'The extent to which the team works together',
                'weight': 0.91
            },
            {
                'name': 'Process Maturity',
                'description': 'The extent to which the development process is mature',
                'weight': 0.91
            }
        ]

        # Cost Drivers
        cost_drivers = [
            {
                'name': 'Required Software Reliability',
                'description': 'The extent to which the software must perform its intended function over a period of time',
                'rating': 3,
                'category': 'PRODUCT',
                'effort_multiplier': 1.0
            },
            {
                'name': 'Database Size',
                'description': 'The size of the database that the software will use',
                'rating': 3,
                'category': 'PRODUCT',
                'effort_multiplier': 1.0
            },
            {
                'name': 'Product Complexity',
                'description': 'The complexity of the product being developed',
                'rating': 3,
                'category': 'PRODUCT',
                'effort_multiplier': 1.0
            },
            {
                'name': 'Required Reusability',
                'description': 'The extent to which the software must be reusable',
                'rating': 3,
                'category': 'PRODUCT',
                'effort_multiplier': 1.0
            },
            {
                'name': 'Documentation Match to Life-Cycle Needs',
                'description': 'The extent to which the documentation matches the life-cycle needs',
                'rating': 3,
                'category': 'PRODUCT',
                'effort_multiplier': 1.0
            }
        ]

        # Create Scale Drivers
        for driver_data in scale_drivers:
            ScaleDriver.objects.get_or_create(
                name=driver_data['name'],
                defaults=driver_data
            )
            self.stdout.write(f"Created Scale Driver: {driver_data['name']}")

        # Create Cost Drivers
        for driver_data in cost_drivers:
            CostDriver.objects.get_or_create(
                name=driver_data['name'],
                defaults=driver_data
            )
            self.stdout.write(f"Created Cost Driver: {driver_data['name']}")

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data')) 