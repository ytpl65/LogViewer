

from django.db import models 
from django.db.models import Count


class LogManager(models.Manager):

    def count_by_level_and_file_type(self,level,file_type=None):
        if file_type:
            return self.filter(log_level=level,log_file_type_name=file_type).count()
        return self.filter(log_level=level).count()
    
    def get_top_warning_method(self):
        return self.filter(log_level='WARNING').values('method_name').annotate(no_of_times_called=Count('method_name')).order_by('-no_of_times_called')[:1]
    
    def get_top_error_method(self,log_file):
        return self.filter(log_file_type_name= log_file, log_level='ERROR').values('method_name').annotate(no_of_times_called=Count('method_name')).order_by('-no_of_times_called')[:1]
    
    def get_top_critical_method(self,log_file):
        return self.filter(log_file_type_name= log_file, log_level='CRITICAL').values('method_name').annotate(no_of_times_called=Count('method_name')).order_by('-no_of_times_called')[:1]

    def get_filtered_data(self,order_by_field=None,**filter):
        if filter:
            return self.filter(**filter).order_by('-timestamp')
        return self.all().order_by(order_by_field).order_by('-timestamp')