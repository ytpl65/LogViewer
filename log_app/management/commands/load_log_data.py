

from django.core.management.base import BaseCommand
from ... import load_log_data_script

class Command(BaseCommand):
    help = 'Extract Log data from the log files and insert the data into database'

    def handle(self,*args,**options):
        load_log_data_script.load_data()