import re 
import os 
from .models import Mobileservices_logs,Youtility_logs,Reports_logs,Error_logs
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import datetime

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

def get_log_file_name():
    pass

















# if __name__ == '__main__':
#     dir_path = '/home/satyam/Downloads/youtility4_logs'
#     report_log_arr, mobile_log_arr, youtility_log_arr =  get_file_names(dir_path)
#     final_log_arr =get_respective_log_of_files(reports_log_file_arr=report_log_arr,mobile_services_log_file_arr=mobile_log_arr,youtility_log_file_arr=youtility_log_arr)



