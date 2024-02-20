from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Youtility_logs,Mobileservices_logs,Reports_logs,Error_logs
from django.db.models import Q,Count,Case,When,Value,IntegerField
from django.db.models.functions import TruncDate


# Create your views here.
from .utils import get_start_and_end_date
from django.core.paginator import Paginator
def home(request):
    return render(request,'log_select.html')

def get_youtility_logs(request):
    print("Received Ajax request")
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    filter = {}
    for i in range(4):
        column_search_value = request.GET.get(f'columns[{i}][search][value]',None)
        print("Coulmn Search Value", column_search_value)
        if column_search_value:
            if i == 0:
                start_date, end_date = get_start_and_end_date(column_search_value)
                print("Start Date",start_date)
                print("End Date", end_date)
                filter['timestamp__range'] = (start_date,end_date)
            elif i == 1:
                filter['log_level__icontains'] = column_search_value
            elif i == 2:
                filter['method_name__icontains'] = column_search_value
            elif i == 3:
                filter['log_message__icontains'] = column_search_value
    print(filter)
    if filter:
        log_entries = Youtility_logs.objects.filter(**filter)
    else:
        log_entries = Youtility_logs.objects.all().order_by(order_by_field)
    print("Log Entries",str(log_entries.query))
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
    print("Received Ajax request")
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    filter = {}

    for i in range(4):
        column_search_value = request.GET.get(f'columns[{i}][search][value]',None)
        if column_search_value:
            if i == 0:
                start_date, end_date = get_start_and_end_date(column_search_value)
                print("Start Date",start_date)
                print("End Date", end_date)
                filter['timestamp__range'] = (start_date,end_date)
            elif i == 1:
                filter['log_level__icontains'] = column_search_value
            elif i == 2:
                filter['method_name__icontains'] = column_search_value
            elif i == 3:
                filter['log_message__icontains'] = column_search_value

    if filter:
        log_entries = Mobileservices_logs.objects.filter(**filter)
    else:
        log_entries = Mobileservices_logs.objects.all().order_by(order_by_field)
    print(str(log_entries.query))
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

    filter = {}

    for i in range(4):
        column_search_value = request.GET.get(f'columns[{i}][search][value]', None)
        if column_search_value:
            if i==0:
                start_date, end_date = get_start_and_end_date(column_search_value)
                print("Start Date",start_date)
                print("End Date", end_date)
                filter['timestamp__range'] = (start_date,end_date)
            elif i==1:
                filter['log_level__icontains'] = column_search_value
            elif i==2:
                filter['method_name__icontains'] = column_search_value
            elif i==3:
                filter['log_message__icontains'] = column_search_value

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
                print("Start Date",start_date)
                print("End Date", end_date)
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
    print(type(is_error_table),is_error_table)
    if is_error_table == 'true':
        print("Error log", pk)
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
            print("youtility log",pk)
            log_data = Youtility_logs.objects.get(id=pk)
        elif log_type == 'mobileservice':
            print("Mobile log",pk)
            log_data = Mobileservices_logs.objects.get(id=pk)
        else:
            print("Report log",pk)
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


    log_counts_by_date = (
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
    for x in log_counts_by_date:
        print(x)
    print(len(log_counts_by_date))

    youtility_warning_logs_by_date = (
    Youtility_logs.objects
    .filter(log_level='WARNING')
    .annotate(log_date=TruncDate('timestamp'))
    .values('log_date')  # Group by this date
    .annotate(youtility_warning=Count('id'))  # Count occurrences
    .order_by('log_date')  # Order by the log_date
    )
    # for x in youtility_warning_logs_by_date:
    #     print(x)
    print(len(youtility_warning_logs_by_date))

    mobileservices_warning_logs_by_date = (
    Mobileservices_logs.objects
    .filter(log_level='WARNING')
    .annotate(log_date=TruncDate('timestamp'))
    .values('log_date')  # Group by this date
    .annotate(youtility_warning=Count('id'))  # Count occurrences
    .order_by('log_date')  # Order by the log_date
    )
    # for x in mobileservices_warning_logs_by_date:
    #     print(x)
    print(len(mobileservices_warning_logs_by_date))

    reports_warning_logs_by_date = (
    Reports_logs.objects
    .filter(log_level='WARNING')
    .annotate(log_date=TruncDate('timestamp'))
    .values('log_date')  # Group by this date
    .annotate(youtility_warning=Count('id'))  # Count occurrences
    .order_by('log_date')  # Order by the log_date
    )
    # for x in reports_warning_logs_by_date:
    #     print(x)
    print(len(reports_warning_logs_by_date))
    return JsonResponse(response)
    
    