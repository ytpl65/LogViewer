from django.shortcuts import render
from django.http import JsonResponse
from .models import Youtility_logs,Mobileservices_logs,Reports_logs,Error_logs
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .utils import *


def home(request):
    return render(request,'base.html')

def get_youtility_logs(request):
    """
    Get Youtility logs and return JSON response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing Youtility logs.
    """
    return get_logs(request,Youtility_logs)


def get_mobileservices_logs(request):
    """
    Get Mobileservice logs and return JSON response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing MobileService logs.
    """
    return get_logs(request, Mobileservices_logs)


def get_reports_logs(request):
    """
    Get Reports logs and return JSON response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing Reports logs.
    """
    return get_logs( request, Reports_logs)

def get_error_logs(request):
    """
    Get error logs and return JSON response.

    This function takes request as an input extract the necessary data like draw,start
    length,order_by_field based on this it creates filter then retrieve the logs from Error Logs
    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing error logs data, recordPassed, recordFiltered ,draw.
    
    Raises:
    - Exception: If an error occurs during the execution of the function,
      an error JSON response with the error message is returned with a status
      code of 500.
    """
    try:
        response_data = extract_response_data(request)
        draw = response_data[0]
        start = response_data[1]
        length = response_data[2]
        order_by_field = response_data[6]
        filter = get_error_filter(request)
        if filter:
            log_entries = Error_logs.objects.filter(**filter)
        else:
            log_entries = Error_logs.objects.all().order_by(order_by_field)
        paginator = Paginator(log_entries,length)
        page_number = (start//length)+1
        page_obj = paginator.get_page(page_number)
        is_error_table_data = True
        response_data = get_response_error_data(page_obj,is_error_table_data)
        response_json = get_response_json(draw,log_entries,response_data)
        return JsonResponse(response_json)
    except Exception as e:
        return JsonResponse({'error':str(e)},status=500)
    
def get_particular_data(request, pk:int,log_type:str, is_error_table:str)-> JsonResponse:
    """
    Get particular data based on primary key, log type, and error table flag.

    Parameters:
    - request: HTTP request object.
    - pk (int): Primary key of the log entry.
    - log_type (str): Type of log entry.
    - is_error_table (str): Flag indicating if it's an error table.

    Returns:
    - JsonResponse: JSON response containing the requested data.
    """
    
    try:
        if is_error_table.lower() == 'true':
            log_data = get_object_or_404(Error_logs,id=pk,log_file_type_name = log_type)
            Model = Error_logs
        else:
            if log_type == 'youtility4':
                Model = Youtility_logs
            elif log_type == 'mobileservice':
                Model = Mobileservices_logs
            else:
                Model = Reports_logs
            log_data = get_object_or_404(Model,id=pk)
        response = construct_response(log_data,Model)
        return JsonResponse({'data':response})
    except Exception as e:
        return JsonResponse({'error':str(e)},status=500)




def get_dashboard_data(request):
    """
    Retrieve dashboard data including counts of critical, error, and warning logs
    for different log types, and return a JSON response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing dashboard data.

    Raises:
    - Exception: If an error occurs during the execution, an error JSON response
      with the error message is returned with a status code of 500.
    """
    try:
        youtility_critical_count = Error_logs.objects.filter(log_level='CRITICAL',log_file_type_name='youtility4').count()
        youtility_error_count = Error_logs.objects.filter(log_level='ERROR',log_file_type_name = 'youtility4').count()
        youtility_warning_count = Youtility_logs.objects.filter(log_level='WARNING').count()

        mobileservices_critical_count = Error_logs.objects.filter(log_level='CRITICAL',log_file_type_name='mobileservice').count() 
        mobileservices_error_count = Error_logs.objects.filter(log_level='ERROR',log_file_type_name='mobileservice').count()
        mobileservices_warning_count = Mobileservices_logs.objects.filter(log_level='WARNING').count()

        reports_critical_count = Error_logs.objects.filter(log_level='CRITICAL',log_file_type_name='reports').count()  
        reports_error_count = Error_logs.objects.filter(log_level='ERROR',log_file_type_name='reports').count()
        reports_warning_count = Reports_logs.objects.filter(log_level='WARNING').count()
        
        response = {
            'youtility_critical':youtility_critical_count,
            'youtility_error':youtility_error_count,
            'youtility_warning':youtility_warning_count,
            'mobileservices_critical':mobileservices_critical_count,
            'mobileservices_error': mobileservices_error_count,
            'mobileservices_warning':mobileservices_warning_count,
            'reports_critical':reports_critical_count,
            'reports_error':reports_error_count,
            'reports_warning':reports_warning_count
        }
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'error':str(e)}, status=500)

    
def get_youtility_graph_data(request):
    """
    Retrieve Youtility graph data and return JSON response.

    This function retrieves Youtility graph data including critical and error logs count with date,
    warning logs count with date, and constructs the response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing Youtility graph data.

    Raises:
    - Exception: If an error occurs during the execution, an error JSON response
      with the error message is returned with a status code of 500.
    """
    log_file = 'youtility4'
    modelName = Youtility_logs
    log_warning = 'youtility_warning'
    return get_graph_data(log_file,modelName,log_warning)

def get_mobileservices_graph_data(request):
    """
    Retrieve MobileServices graph data and return JSON response.

    This function retrieves MobileServices graph data including critical and error logs count with date,
    warning logs count with date, and constructs the response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing MobileServices graph data.

    Raises:
    - Exception: If an error occurs during the execution, an error JSON response
      with the error message is returned with a status code of 500.
    """
    log_file = 'mobileservices'
    modelName = Mobileservices_logs
    log_warning = 'mobileservices_warning'

    return get_graph_data(log_file,modelName,log_warning)


def get_reports_graph_data(request):
    """
    Retrieve Reports graph data and return JSON response.

    This function retrieves Reports graph data including critical and error logs count with date,
    warning logs count with date, and constructs the response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing Reports graph data.

    Raises:
    - Exception: If an error occurs during the execution, an error JSON response
      with the error message is returned with a status code of 500.
    """
    log_file = 'reports'
    modelName = Reports_logs
    log_warning = 'reports_warning'
    return get_graph_data(log_file,modelName,log_warning)


def get_piechart_data(request):
    """
    Retrieve pie chart data for warning, critical, and error logs across different log types,
    and return a JSON response.

    This function retrieves data for warning, critical, and error logs for Youtility, Mobile Services,
    and Reports, converts the queryset results to lists, and constructs the response.

    Parameters:
    - request: HTTP request object.

    Returns:
    - JsonResponse: JSON response containing pie chart data.

    Raises:
    - Exception: If an error occurs during the execution, an error JSON response
      with the error message is returned with a status code of 500.
    """

    youtility_warning= get_youtility_warning_top_method()
    mobileservices_warning = get_mobileservices_warning_top_method()
    reports_warning = get_reports_warning_top_method()

    youtility_critical = get_critical_top_method('youtility4')
    mobileservices_critical = get_critical_top_method('mobileservice')
    reports_critical = get_critical_top_method('reports')

    youtility_error = get_error_top_method('youtility4')    
    mobileservices_error = get_error_top_method('mobileservice')
    reports_error = get_error_top_method('reports')
    
    youtility_warning_data = convert_queryset_to_list(youtility_warning)
    mobileservices_warning_data = convert_queryset_to_list(mobileservices_warning)
    reports_warning_data = convert_queryset_to_list(reports_warning)
    youtility_critical_data = convert_queryset_to_list(youtility_critical)
    mobileservices_critical_data = convert_queryset_to_list(mobileservices_critical)
    reports_critical_data = convert_queryset_to_list(reports_critical)
    youtility_error_data = convert_queryset_to_list(youtility_error)
    mobileservices_error_data = convert_queryset_to_list(mobileservices_error)
    reports_error_data = convert_queryset_to_list(reports_error)
    
    data = [youtility_warning_data,mobileservices_warning_data,reports_warning_data,youtility_critical_data,mobileservices_critical_data,reports_critical_data,youtility_error_data,mobileservices_error_data,reports_error_data]
    
    method_name = []
    no_of_times_called = []
    for x in data:
        method_name.append(x[0])
        no_of_times_called.append(x[1])
    response = {
        'method_name':method_name,
        'no_of_times_called':no_of_times_called
    }
    return JsonResponse(response)