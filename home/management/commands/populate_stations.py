import json
from django.core.management.base import BaseCommand
from home.models import Station

class Command(BaseCommand):
    help = 'Populate stations from JSON file'

    def handle(self, *args, **options):
        with open(r'C:\Users\ADMIN\Desktop\django\Railease\station_json.json', 'r') as file:
            data = json.load(file)
            stations_data = data.get('data', [])

        for station_data in stations_data:
            Station.objects.create( 
                station_name=station_data.get('name', ''),
                station_code=station_data.get('code', ''),
            )

        self.stdout.write(self.style.SUCCESS('Stations successfully populated'))