
import django
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','log_viewer_project.settings')
django.setup()


from log_app.utils import get_file_names,get_respective_log_of_files,inserting_into_mobileservices_table,inserting_into_report_table,inserting_into_youtility_table,inserting_into_error_table

def load_data():
    dir_path = '/home/satyam/Downloads/youtility4_logs'
    report_log_arr, mobile_log_arr, youtility_log_arr =  get_file_names(dir_path)
    final_log_arr =get_respective_log_of_files(reports_log_file_arr=report_log_arr,mobile_services_log_file_arr=mobile_log_arr,youtility_log_file_arr=youtility_log_arr)    
    inserting_into_database(final_log_arr)


def inserting_into_database(final_log_arr):
    mobileservice_normal_log_arr = final_log_arr[0]
    mobileservice_error_log_arr = final_log_arr[1]
    report_normal_log_arr = final_log_arr[2]
    report_error_log_arr = final_log_arr[3]
    youtility_normal_log_arr = final_log_arr[4]
    youtility_error_log_arr = final_log_arr[5]

    error_log = mobileservice_error_log_arr + report_error_log_arr + youtility_error_log_arr
    # inserting_into_mobileservices_table(mobileservice_normal_log_arr)
    # inserting_into_report_table(report_normal_log_arr)
    inserting_into_youtility_table(youtility_normal_log_arr)
    inserting_into_error_table(error_log)

load_data()