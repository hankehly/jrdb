from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """
    Load all fixtures in jrdb.fixtures

    Using this script instead of a simple for loop
    prevents errors due to load-order
    """

    def handle(self, *args, **options):
        exec_order = [
            'horse_gear_code_category',
            'horse_gear_code',

            'race_condition_group_code',
            'race_condition_code',

            'hoof_code',
            'pace_flow_code',
            'race_class',
            'racetrack',
            'special_mention_code'
        ]

        for fixture in exec_order:
            call_command('loaddata', fixture)
