from django.db import models
from .managers import LogManager
# Create your models here.
class Youtility_logs(models.Model):

   timestamp = models.DateTimeField()
   log_level = models.CharField(max_length = 20)
   method_name = models.CharField(max_length = 255)
   log_message = models.TextField()
   log_file_type_name = models.CharField(max_length=20,null=True)
   objects = models.Manager()
   log_manager = LogManager()

   def __str__(self):
      return f"{self.timestamp} + {self.log_level}"
   
   class Meta:
      db_table= "youtility_logs"


class Reports_logs(models.Model):

   timestamp = models.DateTimeField()
   log_level = models.CharField(max_length = 20)
   method_name = models.CharField(max_length = 255)
   log_message = models.TextField()
   log_file_type_name = models.CharField(max_length=20,null=True)
   objects = models.Manager()
   log_manager = LogManager()
   

   def __str__(self):
      return f"{self.timestamp} + {self.log_level}"
   
   class Meta:
      db_table= "reports_logs"


class Mobileservices_logs(models.Model):

   timestamp = models.DateTimeField()
   log_level = models.CharField(max_length = 20)
   method_name = models.CharField(max_length = 255)
   log_message = models.TextField()
   log_file_type_name = models.CharField(max_length=20,null=True)
   objects = models.Manager()
   log_manager = LogManager()
   

   def __str__(self):
      return f"{self.timestamp} + {self.log_level}"
   
   class Meta:
      db_table= "mobileservices_logs"


class Error_logs(models.Model):

   timestamp = models.DateTimeField()
   log_level = models.CharField(max_length = 20)
   method_name = models.CharField(max_length = 255)
   log_message = models.TextField()
   traceback = models.TextField()
   exceptionName = models.TextField()
   log_file_type_name = models.CharField(max_length=20,null=True)
   objects = models.Manager()
   log_manager = LogManager()
   

   def __str__(self):
      return f"{self.timestamp} + {self.log_level}"
   
   class Meta:
      db_table= "error_logs"