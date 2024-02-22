from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Youtility_logs,Mobileservices_logs,Reports_logs,Error_logs
from django.db.models import Q,Count,Case,When,Value,IntegerField
from django.db.models.functions import TruncDate


# Create your views here.
from .utils import get_start_and_end_date,query_filter,convert_queryset_to_list,get_error_top_method,get_response_data,get_critical_top_method,get_mobileservices_warning_top_method,get_reports_warning_top_method,get_youtility_warning_top_method,get_mobileservices_warning_logs_count_with_date,get_mobileservices_warning_date,get_top_methods,mobileservices_date_warning_list,get_youtility_warning_logs_count_with_date,get_all_logs_critical_error_count_with_date,get_youtility_warning_date,get_critical_error_date,convert_critical_error_warning_log_date_in_list_to_str,get_critical_error_warning_date_in_list,all_logs_date_critical_error_list,get_critical_error_warning_data,get_reports_warning_logs_count_with_date,get_reports_warning_date,reports_date_warning_list,youtility_date_warning_list
from django.core.paginator import Paginator
def home(request):
    return render(request,'log_select.html')

def get_youtility_logs(request):
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    field_index = request.GET.get('order[0][column]','0')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')

    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    filter = query_filter(request)
    if filter:
        log_entries = Youtility_logs.objects.filter(**filter)
    else:
        log_entries = Youtility_logs.objects.all().order_by(order_by_field)
    paginator = Paginator(log_entries,length)
    page_number = (start // length) +1
    page_obj = paginator.get_page(page_number)
    is_error_table_data = False
    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "view": [obj.id,obj.log_file_type_name, is_error_table_data]
        })
    response = {
        'draw':draw,
        'recordsTotal':log_entries.count(),
        'recordsFiltered':log_entries.count(),
        'data':data
    }
    return JsonResponse(response)




def get_mobileservices_logs(request):
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    filter = query_filter(request)
    if filter:
        log_entries = Mobileservices_logs.objects.filter(**filter)
    else:
        log_entries = Mobileservices_logs.objects.all().order_by(order_by_field)
    paginator = Paginator(log_entries,length)
    page_number = (start // length) +1
    page_obj = paginator.get_page(page_number)
    is_error_table_data = False
    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "view": [obj.id,obj.log_file_type_name,is_error_table_data]
        })
    response = {
        'draw':draw,
        'recordsTotal':log_entries.count(),
        'recordsFiltered':log_entries.count(),
        'data':data
    }

    return JsonResponse(response)


def get_reports_logs(request):
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    filter = query_filter(request)
    if filter:
        log_entries = Reports_logs.objects.filter(**filter)
    else:
        log_entries = Reports_logs.objects.all().order_by(order_by_field)
    
    pagintor = Paginator(log_entries, length)
    page_number = (start // length ) + 1
    page_obj = pagintor.get_page(page_number)

    is_error_table_data = False
    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "view": [obj.id,obj.log_file_type_name, is_error_table_data]
        })
    response = {
        'draw':draw,
        'recordsTotal':log_entries.count(),
        'recordsFiltered':log_entries.count(),
        'data':data
    }

    return JsonResponse(response)

def get_error_logs(request):
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name

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
    if filter:
        log_entries = Error_logs.objects.filter(**filter)
    else:
        log_entries = Error_logs.objects.all().order_by(order_by_field)
    paginator = Paginator(log_entries,length)
    page_number = (start//length)+1
    page_obj = paginator.get_page(page_number)
    is_error_table_data = True
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
    response = {
        'draw':draw,
        'recordsTotal':log_entries.count(),
        'recordsFiltered':log_entries.count(),
        'data':data
    }
    return JsonResponse(response)


def get_particular_data(request, pk,log_type, is_error_table):

    if is_error_table == 'true':
 
        log_data = Error_logs.objects.get(id=pk,log_file_type_name=log_type)
        response = {
            'timestamp':log_data.timestamp,
            'log_level':log_data.log_level,
            'method_name':log_data.method_name,
            'log_message':log_data.log_message,
            'traceback':log_data.traceback,
            'exceptionname':log_data.exceptionName,
            'log_type':log_data.log_file_type_name
        }
    else:
        if log_type=='youtility4':
            log_data = Youtility_logs.objects.get(id=pk)
        elif log_type == 'mobileservice':
            log_data = Mobileservices_logs.objects.get(id=pk)
        else:
            log_data = Reports_logs.objects.get(id=pk)

        response = {
            'timestamp':log_data.timestamp,
            'log_level':log_data.log_level,
            'method_name':log_data.method_name, 
            'log_message':log_data.log_message
        }
    return JsonResponse({'data':response})


def get_dashboard_data(request):
    youtility_critical_count = len(Error_logs.objects.filter(log_level='CRITICAL',log_file_type_name='youtility4'))
    youtility_error_count = len(Error_logs.objects.filter(log_level='ERROR',log_file_type_name='youtility4'))
    youtility_warning_count = len(Youtility_logs.objects.filter(log_level='WARNING'))

    mobileservices_critical_count = len(Error_logs.objects.filter(log_level='CRITICAL',log_file_type_name='mobileservice')) 
    mobileservices_error_count = len(Error_logs.objects.filter(log_level='ERROR',log_file_type_name='mobileservice'))   
    mobileservices_warning_count = len(Mobileservices_logs.objects.filter(log_level='WARNING'))   
    
    reports_critical_count = len(Error_logs.objects.filter(log_level='CRITICAL',log_file_type_name='reports'))  
    reports_error_count = len(Error_logs.objects.filter(log_level='ERROR',log_file_type_name='reports'))    
    reports_warning_count = len(Reports_logs.objects.filter(log_level='WARNING'))    
    
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
    

index_dictionary = {'youtility4':[1,2],'mobileservices':[3,4],'reports':[5,6]}

    
def get_youtility_graph_data(request):
    log_file = 'youtility4'
    all_logs_critical_error_count_with_date = get_all_logs_critical_error_count_with_date()
    # This will contanis an array of array which where at index 0 I have following data ['2023-03-24',0,5,3,5,7,8]
    all_logs_critical_error_date = all_logs_date_critical_error_list(all_logs_critical_error_count_with_date)
    # This will give me all date in array called critical_error_date
    all_logs_critical_error_date_only = get_critical_error_date(all_logs_critical_error_count_with_date)
    youtility_warning_logs_count_with_date = get_youtility_warning_logs_count_with_date()
    youtility_warning_date_list = get_youtility_warning_date(youtility_warning_logs_count_with_date)

    youtility_date_with_warning_count_list = youtility_date_warning_list(youtility_warning_logs_count_with_date)

    youtility_critical_error_warning_log_date_in_list = get_critical_error_warning_date_in_list(youtility_warning_date_list,all_logs_critical_error_date_only)
    youtility_critical_error_warning_log_date_list_in_str = convert_critical_error_warning_log_date_in_list_to_str(youtility_critical_error_warning_log_date_in_list)
    log_date, data = get_critical_error_warning_data(youtility_critical_error_warning_log_date_list_in_str,youtility_date_with_warning_count_list,all_logs_critical_error_date,log_file,index_dictionary)

    response = {
        'log_date':log_date,
        'data':data
    }
    return JsonResponse(response)

def get_mobileservices_graph_data(request):
    log_file = 'mobileservices'
    all_logs_critical_error_count_with_date = get_all_logs_critical_error_count_with_date()
    all_logs_critical_error_date = all_logs_date_critical_error_list(all_logs_critical_error_count_with_date)
    all_logs_critical_error_date_only = get_critical_error_date(all_logs_critical_error_count_with_date)
    mobileservices_warning_logs_count_with_date = get_mobileservices_warning_logs_count_with_date()
    mobileservices_warning_date_list = get_mobileservices_warning_date(mobileservices_warning_logs_count_with_date)
    mobileservices_date_with_warning_count_list = mobileservices_date_warning_list(mobileservices_warning_logs_count_with_date)
    mobileservices_critical_error_warning_log_date_in_list = get_critical_error_warning_date_in_list(mobileservices_warning_date_list,all_logs_critical_error_date_only)
    mobileservices_critical_error_warning_log_date_in_list_in_str = convert_critical_error_warning_log_date_in_list_to_str(mobileservices_critical_error_warning_log_date_in_list)
    log_date, data = get_critical_error_warning_data(mobileservices_critical_error_warning_log_date_in_list_in_str, mobileservices_date_with_warning_count_list,all_logs_critical_error_date,log_file,index_dictionary)
    response = {
        'log_date':log_date,
        'data':data
    }
    return JsonResponse(response)




def get_reports_graph_data(request):
    log_file = 'reports'
    all_logs_critical_error_count_with_date = get_all_logs_critical_error_count_with_date()
    all_logs_critical_error_date = all_logs_date_critical_error_list(all_logs_critical_error_count_with_date) 
    all_logs_critical_error_date_only = get_critical_error_date(all_logs_critical_error_count_with_date)
    reports_warning_logs_count_with_date = get_reports_warning_logs_count_with_date()
    reports_warning_date_list = get_reports_warning_date(reports_warning_logs_count_with_date)
    reports_date_with_warning_count_list = reports_date_warning_list(reports_warning_logs_count_with_date)
    reports_critical_error_warning_log_date_in_list = get_critical_error_warning_date_in_list(reports_warning_date_list,all_logs_critical_error_date_only)
    reports_critical_error_warning_log_date_in_list_in_str = convert_critical_error_warning_log_date_in_list_to_str(reports_critical_error_warning_log_date_in_list)
    log_date, data = get_critical_error_warning_data(reports_critical_error_warning_log_date_in_list_in_str, reports_date_with_warning_count_list,all_logs_critical_error_date,log_file,index_dictionary)
    response = {
        'log_date':log_date,
        'data':data
    }

    return JsonResponse(response)




def get_piechart_data(request):

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
        print(x)
        method_name.append(x[0])
        no_of_times_called.append(x[1])
    print(method_name)
    print(no_of_times_called)
    # method_name,no_of_times_called = get_response_data(response)
    # print(method_name)
    # print(no_of_times_called)
    response = {
        'method_name':method_name,
        'no_of_times_called':no_of_times_called
    }
    return JsonResponse(response)


