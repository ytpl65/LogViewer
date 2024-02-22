import re 
import os 
from .models import Mobileservices_logs,Youtility_logs,Reports_logs,Error_logs
from django.db.models import Count,Case,When,Value,IntegerField
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
import pytz 


def get_file_names(dir_path:str)->[list,list,list]:
    """ 
    This function takes directory path and return 3 list which contains files of respective logs
    list1 : reports_log_files arr 
    list2 : mobileservice_log_files_arr 
    list3 : youtility_log_files_arr

    return lists
    """
    file_names = os.listdir(path=dir_path)
    mobileservice_log_files =[]
    reports_log_files = []
    youtility4_log_files = []
    for x in file_names:
        if x.startswith('you'):
            youtility4_log_files.append(x)
        if x.startswith('mob'):
            mobileservice_log_files.append(x)
        if x.startswith('repo'):
            reports_log_files.append(x)
    return reports_log_files,mobileservice_log_files,youtility4_log_files


def get_respective_log_of_files(reports_log_file_arr:list,mobile_services_log_file_arr:list,youtility_log_file_arr:list)->list:
    """ 
    This takes as input 3 log files arrays name and return list which contains the following data
    normal_log_data -> [INFO,DEBUG,WARNING]
    error_log_data  -> [CRITICAL, ERROR]
    It return this list of each of the log report type
    """
    mobileservices_normal_log_data, mobileservices_error_log_data =get_mobileservices_log(mobile_services_log_file_arr)
    reports_normal_log_data, reports_error_log_data = get_reports_log(reports_log_file_arr)
    youtility_normal_log_data , youtility_error_log_data = get_youtility_log(youtility_log_file_arr)
    return [mobileservices_normal_log_data,mobileservices_error_log_data,reports_normal_log_data,reports_error_log_data,youtility_normal_log_data,youtility_error_log_data]



def get_mobileservices_log(log_file_name_arr:list)->[list,list]:
    """ 
    This takes as input mobile_service_log_file_arr and
    return mobileservices_normal_log_data, mobileservices_error_log_data
    """
    mobileservices_normal_log_data,mobileservices_error_log_data = pass_single_file(log_file_name_arr=log_file_name_arr)
    return mobileservices_normal_log_data,mobileservices_error_log_data



def get_reports_log(log_file_name_arr:list)->[list,list]:
    """ 
    This takes as input reports_log_file_arr and
    return report_normal_log_data, report_error_log_data
    """
    reports_normal_log_data, report_error_log_data = pass_single_file(log_file_name_arr=log_file_name_arr)
    return reports_normal_log_data,report_error_log_data

def get_youtility_log(log_file_name_arr:list)->[list,list]:
    """ 
    This takes as input youtility_log_file_arr and
    return youtility_normal_log_data, youtility_error_log_data
    """
    youtility_normal_log_data , youtility_error_log_data = pass_single_file(log_file_name_arr=log_file_name_arr)
    return youtility_normal_log_data,youtility_error_log_data

def pass_single_file(log_file_name_arr:list)->[list,list]:
    """
    This takes as input log_file_name_arr and 
    returns complete_normal_file_data, complete_error_file_data
    """

    complete_normal_file_data = []
    complete_error_file_data = []
    for file in log_file_name_arr:
        normal_data, error_data =extract_log_data(file_path=file)
        complete_normal_file_data.extend(normal_data)
        complete_error_file_data.extend(error_data)
    return complete_normal_file_data, complete_error_file_data

def get_log_file_name_type(filename:str)->str:
    return filename.split('.')[0]


def get_exception_name(traceback:str)->str:
    exception_name = traceback.split('\n')[-2]
    return exception_name

def extract_log_data(file_path:str)->[list,list]:
    """
    This takes as input file_path and 
    returns log_normal_arr, log_error_arr

    log_normal_arr -> All the log data except Traceback includes logs of [INFO,DEBUG,WARNING]
    log_error_arr -> All the log data with Traceback includes logs of [CRITICAL, ERROR]
    """
    log_file_name_type = get_log_file_name_type(file_path)
    with open(f'/home/satyam/Downloads/youtility4_logs/{file_path}', "r") as file:
        timestamp_regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}"
        error_level_regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\s+(\w+)"
        function_name_regex = r"from method: ([a-zA-Z_]+)"
        log_message_regex = r"<< (.+?) >>"
        content = file.read()
        expression = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(ERROR|CRITICAL)\s+from\smethod:\s[a-zA-Z_]+\s+<<\s.+?\s>>((?:(?!\d{4}-\d{2}-\d{2}).)*)(?=\d{4}-\d{2}-\d{2}|\Z)"
        traceback = re.findall(expression,content,flags=re.DOTALL)
        timestamps = re.findall(timestamp_regex, content, flags=re.DOTALL)
        function_names = re.findall(function_name_regex, content, flags=re.DOTALL)
        log_messages = re.findall(log_message_regex, content, flags=re.DOTALL)
        log_levels   = re.findall(error_level_regex,content,flags=re.DOTALL)
        log_normal_arr = []
        log_error_arr = []

        for x in zip(timestamps,function_names,log_messages,log_levels):
            if x[3]=='CRITICAL' or x[3]=='ERROR':
                for y in traceback:
                    if y[0]==x[0] and y[1]==x[3]:
                        exception_name = get_exception_name(y[2])
                        cleaned_log_data = x[2].replace('\x00','')
                        log_error_arr.append({'timestamp':x[0],'function_name':x[1],'log_messages':cleaned_log_data,'log_levels':x[3],'traceback':y[2],'log_file_name_type':log_file_name_type,'exception_name':exception_name})
            else:
                cleaned_log_data = x[2].replace('\x00','')
                log_normal_arr.append({'timestamp':x[0],'function_name':x[1],'log_messages':cleaned_log_data,'log_levels':x[3],'log_file_name_type':log_file_name_type})
    return log_normal_arr, log_error_arr

def inserting_into_mobileservices_table(mobileservice_normal_log_arr):
    for entry in mobileservice_normal_log_arr:
        timestamp = parse_datetime(entry['timestamp'])
        timestamp = timezone.make_aware(timestamp, timezone.get_default_timezone())
        log_entry = Mobileservices_logs(
            timestamp = timestamp,
            log_level = entry['log_levels'],
            method_name = entry['function_name'],
            log_message = entry['log_messages'],
            log_file_type_name = entry['log_file_name_type']
        )
        log_entry.save()

def inserting_into_report_table(report_normal_log_arr):
    for entry in report_normal_log_arr:
        timestamp = parse_datetime(entry['timestamp'])
        timestamp = timezone.make_aware(timestamp, timezone.get_default_timezone())
        log_entry = Reports_logs(
            timestamp = timestamp,
            log_level = entry['log_levels'],
            method_name = entry['function_name'],
            log_message = entry['log_messages'],
            log_file_type_name = entry['log_file_name_type']
        )
        log_entry.save()

def inserting_into_youtility_table(youtility_normal_log_arr):
    for entry in youtility_normal_log_arr:
        timestamp = parse_datetime(entry['timestamp'])
        timestamp = timezone.make_aware(timestamp, timezone.get_default_timezone())
        log_entry = Youtility_logs(
            timestamp = timestamp,
            
            log_level = entry['log_levels'],
            method_name = entry['function_name'],
            log_message = entry['log_messages'],
            log_file_type_name = entry['log_file_name_type']
        )
        log_entry.save()    
        print("Record Inserting Youtility logs")


def inserting_into_error_table(error_log):
    for entry in error_log:
        timestamp = parse_datetime(entry['timestamp'])
        timestamp = timezone.make_aware(timestamp, timezone.get_default_timezone())
        log_entry = Error_logs(
            timestamp = timestamp,
            log_level = entry['log_levels'],
            method_name = entry['function_name'],
            log_message = entry['log_messages'],
            traceback = entry['traceback'],
            log_file_type_name = entry['log_file_name_type'],
            exceptionName = entry['exception_name']
        )
        log_entry.save()
        print("Record Inserting Errors logs")


def return_start_end_date(date_str):
    date_str_split = date_str.split(' to ')
    start_date = date_str_split[0]
    end_date = date_str_split[1]
    return start_date,end_date


def convert_string_date_to_date_time(date_str):
    date_format = '%Y-%m-%d %H:%M:%S'
    date_obj = datetime.strptime(date_str,date_format)
    return date_obj


def convert_date_to_utc(date_obj):
    ist = pytz.timezone('Asia/Kolkata')
    date_obj_ist = ist.localize(date_obj)
    date_obj_utc = date_obj_ist.astimezone(pytz.utc) 
    return date_obj_utc

def get_start_and_end_date(date_str):
    start_date , end_date = return_start_end_date(date_str)
    start_date_obj = convert_string_date_to_date_time(start_date)
    end_date_obj = convert_string_date_to_date_time(end_date)
    start_date_utc = convert_date_to_utc(start_date_obj)
    end_date_utc = convert_date_to_utc(end_date_obj)
    return start_date_utc, end_date_utc



def all_logs_date_critical_error_list(log_counts_by_date):
    youtility_date_critical_error = []
    for x in log_counts_by_date:
        ele = []
        date = str(x['log_date'])
        youtility_critical = x['youtility_critical']
        youtility_error = x['youtility_error']
        mobileservice_critical = x['mobileservice_critical']
        mobileservice_error = x['mobileservice_error']
        reports_critical = x['reports_critical']
        reports_error = x['reports_error']
        youtility_date_critical_error.append([date,youtility_critical,youtility_error,mobileservice_critical,mobileservice_error,reports_critical,reports_error])
    return youtility_date_critical_error



def youtility_date_warning_list(youtility_warning_logs_by_date):
    youtility_date_warning = [] 
    for x in youtility_warning_logs_by_date:
        date = str(x['log_date'])
        youtility_warning = x['youtility_warning']
        youtility_date_warning.append([date,youtility_warning])
    return youtility_date_warning


def mobileservices_date_warning_list(mobileservices_warning_logs_by_date):
    mobileservice_date_warning = [] 
    for x in mobileservices_warning_logs_by_date:
        date = str(x['log_date'])
        youtility_warning = x['mobileservices_warning']
        mobileservice_date_warning.append([date,youtility_warning])
    return mobileservice_date_warning



def get_critical_error_warning_data(critical_error_warning_log_date_list_str,date_warning,critical_error_date,log_file,index_dictionary):

    indexes = index_dictionary[log_file]

    critical_data = []
    warning_data = []
    error_data = []

    for x in critical_error_warning_log_date_list_str:
        record_present = False
        for record in critical_error_date:
            if record[0] == x:
                record_present = True
                critical_data.append(record[indexes[0]])
                error_data.append(record[indexes[1]])
        if not record_present:
            critical_data.append(0)
            error_data.append(0)
            
        record_present = False 
        for record in date_warning:
            if record[0] == x:
                record_present = True 
                warning_data.append(record[1])
        if not record_present:
            warning_data.append(0)

    data = []
    data.append(critical_data)
    data.append(error_data)
    data.append(warning_data)

    return critical_error_warning_log_date_list_str,data    



def get_critical_error_date(log_counts_by_date):
    critical_error_date = []
    for record in log_counts_by_date:
        critical_error_date.append(record['log_date'])
    critical_error_date.sort()
    return critical_error_date

def get_youtility_warning_date(youtility_warning_logs_by_date):
    youtility_warning_date = []
    for record in youtility_warning_logs_by_date:
        youtility_warning_date.append(record['log_date'])
    youtility_warning_date.sort()
    return youtility_warning_date


def get_mobileservices_warning_date(mobileservices_warning_logs_by_date):
    mobileservices_warning_date = [] 
    for record in mobileservices_warning_logs_by_date:
        mobileservices_warning_date.append(record['log_date'])
    return mobileservices_warning_date


def get_critical_error_warning_date_in_list(warning_date,all_logs_critical_error_date):
    # print(warning_date,len(warning_date))
    
    # print('########################')
    # print(all_logs_critical_error_date,len(all_logs_critical_error_date))
    critical_error_warning_log_date = warning_date+all_logs_critical_error_date
    critical_error_warning_log_date = set(critical_error_warning_log_date)
    critical_error_warning_log_date_list = (list(critical_error_warning_log_date))
    critical_error_warning_log_date_list.sort()
    # print('################################3')
    # print(critical_error_warning_log_date_list,len(critical_error_warning_log_date_list))
    return critical_error_warning_log_date_list


def convert_critical_error_warning_log_date_in_list_to_str(critical_error_warning_log_date_in_list):
    critical_error_warning_log_date_list_str = []
    for date in critical_error_warning_log_date_in_list:
        critical_error_warning_log_date_list_str.append(str(date))
    return critical_error_warning_log_date_list_str



def get_all_logs_critical_error_count_with_date():
    all_logs_critical_error_count_with_date = (
        Error_logs.objects
        .annotate(log_date=TruncDate('timestamp'))
        .values('log_date')
        .annotate(
            youtility_critical=Count(Case(When(log_level='CRITICAL', log_file_type_name='youtility4', then=Value(1)), output_field=IntegerField())),
            youtility_error=Count(Case(When(log_level='ERROR', log_file_type_name='youtility4', then=Value(1)), output_field=IntegerField())),
            mobileservice_critical=Count(Case(When(log_level='CRITICAL', log_file_type_name='mobileservice', then=Value(1)), output_field=IntegerField())),
            mobileservice_error=Count(Case(When(log_level='ERROR', log_file_type_name='mobileservice', then=Value(1)), output_field=IntegerField())),
            reports_critical=Count(Case(When(log_level='CRITICAL', log_file_type_name='reports', then=Value(1)), output_field=IntegerField())),
            reports_error=Count(Case(When(log_level='ERROR', log_file_type_name='reports', then=Value(1)), output_field=IntegerField())),
        )
        .order_by('log_date')
        )
    return all_logs_critical_error_count_with_date


def get_youtility_warning_logs_count_with_date():
    youtility_warning_logs_count_with_date = (
    Youtility_logs.objects
    .filter(log_level='WARNING')
    .annotate(log_date=TruncDate('timestamp'))
    .values('log_date')  # Group by this date
    .annotate(youtility_warning=Count('id'))  # Count occurrences
    .order_by('log_date')  # Order by the log_date
    )
    return youtility_warning_logs_count_with_date


def get_mobileservices_warning_logs_count_with_date():
    mobileservices_warning_logs_count_with_date = (
    Mobileservices_logs.objects
    .filter(log_level='WARNING')
    .annotate(log_date=TruncDate('timestamp'))
    .values('log_date')  # Group by this date
    .annotate(mobileservices_warning=Count('id'))  # Count occurrences
    .order_by('log_date')  # Order by the log_date
    )
    return mobileservices_warning_logs_count_with_date


def get_reports_warning_logs_count_with_date():
    reports_warning_logs_by_date = (
    Reports_logs.objects
    .filter(log_level='WARNING')
    .annotate(log_date=TruncDate('timestamp'))
    .values('log_date')  # Group by this date
    .annotate(reports_warning=Count('id'))  # Count occurrences
    .order_by('log_date')  # Order by the log_date
    )
    return reports_warning_logs_by_date 

def convert_queryset_to_list(data):
    queryset_list = []
    if len(data)>0:
        method_name = data[0]['method_name']
        no_of_times = data[0]['no_of_times_called']
        queryset_list.append(method_name)
        queryset_list.append(no_of_times)
    else:
        queryset_list.append(0)
        queryset_list.append(0)
    return queryset_list

def get_reports_warning_date(reports_warning_logs_by_date):
    reports_warning_date = []
    for record in reports_warning_logs_by_date:
         reports_warning_date.append(record['log_date'])
    return reports_warning_date


def reports_date_warning_list(reports_warning_logs_by_date):
    reports_date_warning = []
    for x in reports_warning_logs_by_date:
        date = str(x['log_date'])
        reports_warning = x['reports_warning']
        reports_date_warning.append([date,reports_warning])
    return reports_date_warning


def get_top_methods(log_file_type_name):
    return (
        Error_logs.objects
        .filter(log_file_type_name=log_file_type_name)
        .values('method_name')
        .annotate(no_of_times_called=Count('id'))
        .order_by('-no_of_times_called')[:3]
    )

def get_critical_top_method(log_file_type_name):
    queryset = Error_logs.objects \
    .filter(log_file_type_name= log_file_type_name, log_level='CRITICAL') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset

def get_error_top_method(log_file_type_name):
    queryset = Error_logs.objects \
    .filter(log_file_type_name= log_file_type_name, log_level='ERROR') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset


def get_youtility_warning_top_method():
    queryset = Youtility_logs.objects \
    .filter(log_level='WARNING') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset

def get_mobileservices_warning_top_method():
    queryset = Mobileservices_logs.objects \
    .filter(log_level='WARNING') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset

def get_reports_warning_top_method():
    queryset = Reports_logs.objects \
    .filter(log_level='WARNING') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset


def query_filter(request):
    filter = {}
    for i in range(4):
        column_search_value = request.GET.get(f'columns[{i}][search][value]',None)
        if column_search_value:
            if i == 0:
                start_date, end_date = get_start_and_end_date(column_search_value)
                filter['timestamp__range'] = (start_date,end_date)
            elif i == 1:
                filter['log_level__icontains'] = column_search_value
            elif i == 2:
                filter['method_name__icontains'] = column_search_value
            elif i == 3:
                filter['log_message__icontains'] = column_search_value
    return filter



def get_response_data(response):
    method_name = []
    no_of_times_called = []
    for data in response:
        print(data)
        print(data[0],data[1])
        method_name.append(response[data][0])
        no_of_times_called.append(response[data][1])
    return method_name,no_of_times_called