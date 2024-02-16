from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Youtility_logs,Mobileservices_logs,Reports_logs,Error_logs
from django.db.models import Q
# Create your views here.
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
                filter['timestamp__icontains'] = column_search_value
            elif i == 1:
                filter['log_level__icontains'] = column_search_value
            elif i == 2:
                filter['method_name__icontains'] = column_search_value
            elif i == 3:
                filter['log_message__icontains'] = column_search_value

    if filter:
        log_entries = Youtility_logs.objects.filter(**filter)
    else:
        log_entries = Youtility_logs.objects.all().order_by(order_by_field)
    print("Log Entries",str(log_entries.query))
    paginator = Paginator(log_entries,length)
    page_number = (start // length) +1
    page_obj = paginator.get_page(page_number)

    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "view": None
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
                filter['timestamp__icontains'] = column_search_value
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

    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "view": None
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
                filter['timestamp__icontains'] = column_search_value
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


    data = []
    for obj in page_obj:
        data.append({
            "timestamp":obj.timestamp,
            "log_level":obj.log_level,
            "method_name":obj.method_name,
            "log_message":obj.log_message,
            "view": None
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
    for i in range(4):
        column_search_value = request.GET.get(f'columns[{i}][search][value]',None)
        if column_search_value:
            if i==0:
                filter['timestamp__icontains'] = column_search_value
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
            "view": None
        })
    response = {
        'draw':draw,
        'recordsTotal':log_entries.count(),
        'recordsFiltered':log_entries.count(),
        'data':data
    }
    return JsonResponse(response)
