import re 
import os 
from .models import Mobileservices_logs,Youtility_logs,Reports_logs,Error_logs
from django.db.models import Count,Case,When,Value,IntegerField
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
import pytz 
from django.core.paginator import Paginator
from django.http import JsonResponse
from typing import Dict,Union,List,Any

def get_file_names(dir_path):
    """ 
    Retrieve file names for different types of logs in the specified array/list.

    This function takes a directory path and returns three lists containing file names
    for reports, mobile services, and Youtility logs respectively.

    Parameters:
    - dir_path: A string representing the directory path.

    Returns:
        - List1: List of file names for reports logs.
        - List2: List of file names for mobile services logs.
        - List3: List of file names for Youtility logs.
    """
    try:
        file_names = os.listdir(path=dir_path)
        mobileservice_log_files = [x for x in file_names if x.startswith('mob')]
        reports_log_files = [x for x in file_names if x.startswith('repo')]
        youtility4_log_files = [x for x in file_names if x.startswith('you')]
        
        return reports_log_files, mobileservice_log_files, youtility4_log_files
    
    except Exception as e:
        # Exception handling
        print(f"An error occurred: {e}")
        return [], [], []

def get_respective_log_of_files(reports_log_file_arr:list,mobile_services_log_file_arr:list,youtility_log_file_arr:list)->list:
    """ 
    This takes as input 3 log files arrays name and return list which contains the following data
    normal_log_data -> [INFO,DEBUG,WARNING]
    error_log_data  -> [CRITICAL, ERROR]
    It return this list of each of the log report type
    """
    try:
        youtility_normal_log_data , youtility_error_log_data = get_youtility_log(youtility_log_file_arr)
        mobileservices_normal_log_data, mobileservices_error_log_data =get_mobileservices_log(mobile_services_log_file_arr)
        reports_normal_log_data, reports_error_log_data = get_reports_log(reports_log_file_arr)
        return [mobileservices_normal_log_data,mobileservices_error_log_data,reports_normal_log_data,reports_error_log_data,youtility_normal_log_data,youtility_error_log_data]
    except Exception as e:
        print(f"An error occured:{e}")
        return []



def get_mobileservices_log(log_file_name_arr):
    """ 
    This takes as input mobile_service_log_file_arr and
    return mobileservices_normal_log_data, mobileservices_error_log_data
    """
    try:
        mobileservices_normal_log_data,mobileservices_error_log_data = pass_single_file(log_file_name_arr=log_file_name_arr)
        return mobileservices_normal_log_data,mobileservices_error_log_data
    except Exception as e:
        print(f"An error occured:{e}")
        return [],[]



def get_reports_log(log_file_name_arr):
    """ 
    This takes as input reports_log_file_arr and
    return report_normal_log_data, report_error_log_data
    """
    try:
        reports_normal_log_data, report_error_log_data = pass_single_file(log_file_name_arr=log_file_name_arr)
        return reports_normal_log_data,report_error_log_data
    except Exception as e:
        print(f"An error occured:{e}")
        return [],[]

def get_youtility_log(log_file_name_arr):
    """ 
    This takes as input youtility_log_file_arr and
    return youtility_normal_log_data, youtility_error_log_data
    """
    try:
        youtility_normal_log_data , youtility_error_log_data = pass_single_file(log_file_name_arr=log_file_name_arr)
        return youtility_normal_log_data,youtility_error_log_data
    except Exception as e:
        print(f"An error occured:{e}")
        return [],[]

def pass_single_file(log_file_name_arr):
    """
    This takes as input log_file_name_arr and 
    returns complete_normal_file_data, complete_error_file_data
    """
    try:
        complete_normal_file_data = []
        complete_error_file_data = []
        for file in log_file_name_arr:
            normal_data, error_data =extract_log_data(file_path=file)
            complete_normal_file_data.extend(normal_data)
            complete_error_file_data.extend(error_data)
        print(error_data)
        return complete_normal_file_data, complete_error_file_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], []

def get_log_file_name_type(filename:str)->str:
    """This takes filename and splits at '.' 
    and return logfile name only
    """
    return filename.split('.')[0]


def get_exception_name(traceback):
    """This function takes traceback and return exception name."""
    exception_name = traceback.split('\n')[-2]
    return exception_name

def regular_expression():
    """ 
    This function defines following regular expression pattern for timestamp, error_level, function_name,log_message,expression 
    """
    timestamp_regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}"
    error_level_regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\s+(\w+)"
    function_name_regex = r"from method: ([a-zA-Z_]+)"
    log_message_regex = r"<< (.+?) >>"
    expression = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(ERROR|CRITICAL)\s+from\smethod:\s[a-zA-Z_]+\s+<<\s.+?\s>>((?:(?!\d{4}-\d{2}-\d{2}).)*)(?=\d{4}-\d{2}-\d{2}|\Z)"
    return timestamp_regex,error_level_regex,function_name_regex,log_message_regex,expression

def create_structed_timestamp_dict(traceback):
    structued_timestamp = {}
    for record in traceback:
        timestamp = record[0]
        log_level = record[1]
        traceback_message = record[2]
        structued_timestamp[str(timestamp)] = [log_level, traceback_message]
    return structued_timestamp


def extract_data_from_file_using_regualar_expression(timestamp_regex,error_level_regex,function_name_regex,log_message_regex,expression,content):
    """ 
    This function extract the data from the content and stores in the respect array for traceback,timestamps,function_names,log_messages,log_levels and return the same
    """
    traceback = re.findall(expression,content,flags=re.DOTALL)
    timestamps = re.findall(timestamp_regex, content, flags=re.DOTALL)
    function_names = re.findall(function_name_regex, content, flags=re.DOTALL)
    log_messages = re.findall(log_message_regex, content, flags=re.DOTALL)
    log_levels   = re.findall(error_level_regex,content,flags=re.DOTALL)
    structed_timestamp = create_structed_timestamp_dict(traceback)
    
    return traceback, timestamps,function_names,log_messages, log_levels,structed_timestamp
    


def normal_arr_and_error_arr(timestamps,function_names,log_messages,log_levels,traceback,log_file_name_type,structed_timestamp):

    """ 
    This function takes the timestamps, function_names, log_messages, log_levels array and return two list
    which contains log_normal_arr(IN FO,DEBUG,WARNIGN)
    log_error_arr( CRITICAL,ERROR)
    
    """
    log_normal_arr = []
    log_error_arr = []
    for x in zip(timestamps,function_names,log_messages,log_levels):
        if x[3]=='CRITICAL' or x[3]=='ERROR':
            timestamp = str(x[0])
            if timestamp in structed_timestamp:
                record = structed_timestamp[timestamp]
                exception_name = get_exception_name(record[1])
                cleaned_log_data = x[2].replace('\x00','')
                print({'timestamp':x[0],'function_name':x[1],'log_messages':cleaned_log_data,'log_levels':x[3],'traceback':record[1],'log_file_name_type':log_file_name_type,'exception_name':exception_name})
                log_error_arr.append({'timestamp':x[0],'function_name':x[1],'log_messages':cleaned_log_data,'log_levels':x[3],'traceback':record[1],'log_file_name_type':log_file_name_type,'exception_name':exception_name})
        else:
            cleaned_log_data = x[2].replace('\x00','')
            log_normal_arr.append({'timestamp':x[0],'function_name':x[1],'log_messages':cleaned_log_data,'log_levels':x[3],'log_file_name_type':log_file_name_type})
    return log_normal_arr,log_error_arr


def extract_log_data(file_path):
    """
    This takes as input file_path and 
    returns log_normal_arr, log_error_arr

    log_normal_arr -> All the log data except Traceback includes logs of [INFO,DEBUG,WARNING]
    log_error_arr -> All the log data with Traceback includes logs of [CRITICAL, ERROR]
    """
    log_file_name_type = get_log_file_name_type(file_path)
    with open(f'/home/satyam/Downloads/youtility4_logs/{file_path}', "r") as file:
        timestamp_regex,error_level_regex,function_name_regex,log_message_regex,expression = regular_expression()
        content = file.read()
        traceback, timestamps,function_names,log_messages, log_levels, structed_timestamp =extract_data_from_file_using_regualar_expression(timestamp_regex,error_level_regex,function_name_regex,log_message_regex,expression,content)
        log_normal_arr, log_error_arr = normal_arr_and_error_arr(timestamps,function_names,log_messages,log_levels,traceback,log_file_name_type,structed_timestamp)
    return log_normal_arr, log_error_arr

def inserting_into_table(normal_log_arr,model_name):
    """inserting data into database for normal_logs takes normal log array
    """
    for entry in normal_log_arr:
        timestamp = parse_datetime(entry['timestamp'])
        timestamp = timezone.make_aware(timestamp, timezone.get_default_timezone())
        log_entry = model_name(
            timestamp = timestamp,
            log_level = entry['log_levels'],
            method_name = entry['function_name'],
            log_message = entry['log_messages'],
            log_file_type_name = entry['log_file_name_type']
        )
        log_entry.save()

def inserting_into_error_table(error_log):
    """inserting data into database for error_logs takes error log array
    """
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
    """return start date and end date by from string of whole date range"""
    date_str_split = date_str.split(' to ')
    start_date = date_str_split[0]
    end_date = date_str_split[1]
    return start_date,end_date


def convert_string_date_to_date_time(date_str):
    """ converts the date string into a specific date format"""
    date_format = '%Y-%m-%d %H:%M:%S'
    date_obj = datetime.strptime(date_str,date_format)
    return date_obj


def convert_date_to_utc(date_obj):
    """ converts the date into utc"""
    ist = pytz.timezone('Asia/Kolkata')
    date_obj_ist = ist.localize(date_obj)
    date_obj_utc = date_obj_ist.astimezone(pytz.utc) 
    return date_obj_utc

def get_start_and_end_date(date_str):
    """returns start and end date in UTC format"""
    start_date , end_date = return_start_end_date(date_str)
    start_date_obj = convert_string_date_to_date_time(start_date)
    end_date_obj = convert_string_date_to_date_time(end_date)
    start_date_utc = convert_date_to_utc(start_date_obj)
    end_date_utc = convert_date_to_utc(end_date_obj)
    return start_date_utc, end_date_utc



def all_logs_date_critical_error_list(log_counts_by_date):
    """return all log files critical error date counts"""
    all_logs_date_critical_error = []
    for x in log_counts_by_date:
        ele = []
        date = str(x['log_date'])
        youtility_critical = x['youtility_critical']
        youtility_error = x['youtility_error']
        mobileservice_critical = x['mobileservice_critical']
        mobileservice_error = x['mobileservice_error']
        reports_critical = x['reports_critical']
        reports_error = x['reports_error']
        all_logs_date_critical_error.append([date,youtility_critical,youtility_error,mobileservice_critical,mobileservice_error,reports_critical,reports_error])
    return all_logs_date_critical_error

def date_warning_list(warning_logs_by_date, log_warning):
    """return an array which contains warning and log date"""
    date_warning = []
    for x in warning_logs_by_date:
        date = str(x['log_date'])
        warning = x[log_warning]
        date_warning.append([date,warning])
    return date_warning

def get_critical_error_warning_data(critical_error_warning_log_date_list_str,date_warning,critical_error_date,log_file,index_dictionary):
    """return two lists first list contains log date of critcal,error,warning and second list contains arrary of arrays critical data array, error data array,warning data array"""
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
    """returns list which contains log date of critical,error logs"""
    critical_error_date = []
    for record in log_counts_by_date:
        critical_error_date.append(record['log_date'])
    critical_error_date.sort()
    return critical_error_date

def get_warning_date(warning_logs_by_date):
    """returns list which contains log date of warning logs"""
    warning_date  = []
    for record in warning_logs_by_date:
        warning_date.append(record['log_date'])
    return warning_date

def get_critical_error_warning_date_in_list(warning_date,all_logs_critical_error_date):
    """adds critical error date list and warning date list and returns a combined sorted date array"""
    critical_error_warning_log_date = warning_date+all_logs_critical_error_date
    critical_error_warning_log_date = set(critical_error_warning_log_date)
    critical_error_warning_log_date_list = (list(critical_error_warning_log_date))
    critical_error_warning_log_date_list.sort()
    return critical_error_warning_log_date_list


def convert_critical_error_warning_log_date_in_list_to_str(critical_error_warning_log_date_in_list):
    """ 
    This function converts the critical_error_warning_log date to str and return this
    """
    critical_error_warning_log_date_list_str = []
    for date in critical_error_warning_log_date_in_list:
        critical_error_warning_log_date_list_str.append(str(date))
    return critical_error_warning_log_date_list_str



def get_all_logs_critical_error_count_with_date():
    """ 
    This function retrieves youtility,mobile,reports critical error data count grouped by date and return queryset
    """
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

def get_warning_logs_count_with_date(modelName):
    """ 
    This function return warning log count grouped by date
    This function takes modelName as input and uses this to retrieve the data from model
    """
    warning_logs_count_with_date = (
    modelName.objects
    .filter(log_level='WARNING')
    .annotate(log_date=TruncDate('timestamp'))
    .values('log_date')  # Group by this date
    .annotate(youtility_warning=Count('id'))  # Count occurrences
    .order_by('log_date')  # Order by the log_date
    )
    return warning_logs_count_with_date

def convert_queryset_to_list(data):
    """ 
    This function return the convert the queryset to list and returns it.
    """
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

def get_top_methods(log_file_type_name):
    return (
        Error_logs.objects
        .filter(log_file_type_name=log_file_type_name)
        .values('method_name')
        .annotate(no_of_times_called=Count('id'))
        .order_by('-no_of_times_called')[:3]
    )

def get_critical_top_method(log_file_type_name):
    """This function retrieves CRITICAL log method name and number of times it is called in descending order limit 1"""
    queryset = Error_logs.objects\
    .filter(log_file_type_name= log_file_type_name, log_level='CRITICAL') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset

def get_error_top_method(log_file_type_name):
    """This function retrieves ERROR log method name and number of times it is called in descending order limit 1"""
    queryset = Error_logs.objects \
    .filter(log_file_type_name= log_file_type_name, log_level='ERROR') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset


def get_youtility_warning_top_method():
    """This function retrieves WARNING log method name and number of times it is called in descending order limit 1"""
    queryset = Youtility_logs.objects \
    .filter(log_level='WARNING') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset

def get_mobileservices_warning_top_method():
    """This function retrieves WARNING log method name and number of times it is called in descending order limit 1"""
    queryset = Mobileservices_logs.objects \
    .filter(log_level='WARNING') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset

def get_reports_warning_top_method():
    """This function retrieves WARNING log method name and number of times it is called in descending order limit 1"""
    queryset = Reports_logs.objects \
    .filter(log_level='WARNING') \
    .values('method_name') \
    .annotate(no_of_times_called=Count('method_name')) \
    .order_by('-no_of_times_called')[:1]
    return queryset


def query_filter(request: Any) -> Dict[str, Union[str, int]]:
    """
    Generate query filter based on request parameters.

    Parameters:
    - request: HTTP request object.

    Returns:
    - Dict[str, Union[str, int]]: Query filter dictionary.
    """
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
    """
    This function return array of method name and no_of_times the method is called 
    """
    method_name = []
    no_of_times_called = []
    for data in response:
        print(data)
        print(data[0],data[1])
        method_name.append(response[data][0])
        no_of_times_called.append(response[data][1])
    return method_name,no_of_times_called


def extract_response_data(request: Any) -> List[Union[int, str]]:
    """
    Extract response data from the request.

    Parameters:
    - request: HTTP request object.

    Returns:
    - List[Union[int, str]]: List containing response data.
    """
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    field_index = request.GET.get('order[0][column]','0')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    return [draw, start, length,field_index,field_name,direction,order_by_field]


def get_response_data(page_obj: Any, is_error_table_data: bool) -> List[Dict[str, Union[str, int]]]:
    """
    Get response data based on page object and error table flag.

    Parameters:
    - page_obj: Paginator page object.
    - is_error_table_data: Flag indicating if it's an error table data.

    Returns:
    - List[Dict[str, Union[str, int]]]: List of response data dictionaries.
    """
    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "view": [obj.id,obj.log_file_type_name, is_error_table_data]
        })
    return data

def get_response_json(draw,log_entries,response_data):
    """
    Get JSON response dictionary.

    Parameters:
    - draw: Draw parameter.
    - log_entries: Log entries.
    - response_data: Response data.

    Returns:
    - Dict[str, Union[int, List[Dict[str, Union[str, int]]]]]: JSON response dictionary.
    """
    response = {
        'draw':draw,
        'recordsTotal':log_entries.count(),
        'recordsFiltered':log_entries.count(),
        'data':response_data
    }
    return response



def  get_response_error_data(page_obj,is_error_table_data):
    """
    This function creates a error response data which contains timestamp,log_level,method_name,log_message,traceback,exceptioname,log_file_type,view and return it.
    """
    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "traceback":obj.traceback,
            "exceptionName":obj.exceptionName,
            "log_file_type_name":obj.log_file_type_name,
            "view": [obj.id,obj.log_file_type_name,is_error_table_data]
        })
    return data


def get_error_filter(request):
    """
    Generate query filter based on request parameters.

    Parameters:
    - request: HTTP request object.

    Returns:
    - Dict[str, Union[str, int]]: Query filter dictionary.
    """
    filter = {} 
    for i in range(7):
        column_search_value = request.GET.get(f'columns[{i}][search][value]',None)
        if column_search_value:
            if i==0:
                start_date, end_date = get_start_and_end_date(column_search_value)
                filter['timestamp__range'] = (start_date,end_date)
            elif i == 1:
                filter['log_level__icontains'] = column_search_value
            elif i == 2:
                filter['method_name__icontains'] = column_search_value
            elif i == 3:
                filter['log_message__icontains'] = column_search_value
            elif i==4:
                filter['traceback__icontains'] = column_search_value
            elif i==5:
                filter['exceptionName__icontains'] = column_search_value
            elif i==6:
                filter['log_file_type_name__icontains'] = column_search_value
    return filter


def construct_response(log_data: Union[Error_logs,Youtility_logs,Mobileservices_logs,Reports_logs],Model) -> Dict[str, Union[str, int]]:
    """
    Construct response dictionary based on the type of log_data.

    Parameters:
    - log_data (Union[Error_logs, Youtility_logs, Mobileservices_logs, Reports_logs]): The log data object.

    Returns:
    - Dict[str, Union[str, int]]: Response dictionary containing log data.
    """
    response = {
        'timestamp':log_data.timestamp,
        'log_level':log_data.log_level,
        'method_name':log_data.method_name,
        'log_message':log_data.log_message
    }
    if isinstance(Model,Error_logs):
        response.update({
            'traceback':log_data.traceback,
            'exceptionname':log_data.exceptionName,
            'log_type':log_data.log_file_type_name
        })
    print(response)
    return response


def get_logs(request, model_class):
    """
    Get logs based on model class and return JSON response.

    Parameters:
    - request: HTTP request object.
    - model_class: Model class representing the logs.

    Returns:
    - JsonResponse: JSON response containing logs.
    """
    try:
        response_data = extract_response_data(request)
        draw = response_data[0]
        start = response_data[1]
        length = response_data[2]
        order_by_field = response_data[6]
        filter = query_filter(request)
        if filter:
            log_entries = model_class.objects.filter(**filter)
        else:
            log_entries = model_class.objects.all().order_by(order_by_field)
        paginator = Paginator(log_entries, length)
        page_number = (start // length) + 1
        page_obj = paginator.get_page(page_number)
        is_error_table_data = model_class == Error_logs
        response_data = get_response_data(page_obj, is_error_table_data)
        response_json = get_response_json(draw, log_entries, response_data)
        return JsonResponse(response_json)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def get_all_logs_critical_error_date_only():
    """
    This function return all log files critical error date only 
    """
    all_logs_critical_error_count_with_date = get_all_logs_critical_error_count_with_date()
    all_logs_critical_error_date = all_logs_date_critical_error_list(all_logs_critical_error_count_with_date)
    all_logs_critical_error_date_only = get_critical_error_date(all_logs_critical_error_count_with_date)
    return all_logs_critical_error_date_only,all_logs_critical_error_date

def get_graph_data(log_file,modelName,log_warning):
    """
    Retrieve graph data based on the specified log file, model name, and log warning name,
    and return a JSON response.

    This function retrieves graph data including critical and error logs count with date,
    warning logs count with date, and constructs the response.

    Parameters:
    - log_file: A string representing the log file name.
    - modelName: A string representing the model name.
    - log_warning: A string indicating which log to filter from error logs in the data.

    Returns:
    - JsonResponse: JSON response containing graph data.

    Raises:
    - Exception: If an error occurs during the execution, an error JSON response
      with the error message is returned with a status code of 500.
    """
    index_dictionary = {'youtility4':[1,2],'mobileservices':[3,4],'reports':[5,6]}
    try:
        all_logs_critical_error_date_only,all_logs_critical_error_date = get_all_logs_critical_error_date_only()
        youtility_warning_logs_count_with_date = get_warning_logs_count_with_date(modelName)
        youtility_warning_date_list = get_warning_date(youtility_warning_logs_count_with_date)
        youtility_date_with_warning_count_list = date_warning_list(youtility_warning_logs_count_with_date,log_warning)
        youtility_critical_error_warning_log_date_in_list = get_critical_error_warning_date_in_list(youtility_warning_date_list,all_logs_critical_error_date_only)
        youtility_critical_error_warning_log_date_list_in_str = convert_critical_error_warning_log_date_in_list_to_str(youtility_critical_error_warning_log_date_in_list)
        log_date, data = get_critical_error_warning_data(youtility_critical_error_warning_log_date_list_in_str,youtility_date_with_warning_count_list,all_logs_critical_error_date,log_file,index_dictionary)
        response = {
            'log_date':log_date,
            'data':data
        }
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'error':str(e)},status=500)