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
    search_value = request.GET.get('search[value]', '')
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    print(request.GET)
    print(field_name)
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

# def get_mobileservices_logs(request):
#     if request.method == 'GET':
#         mobileservices_logs = Mobileservices_logs.objects.order_by('-timestamp')[0:100]
#         logs_list = list(mobileservices_logs.values('timestamp','log_level','method_name','log_message'))
#         print(logs_list)
#     return JsonResponse({'logs':logs_list})


def get_mobileservices_logs(request):
    print("Received Ajax request")
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    search_value = request.GET.get('search[value]', '')
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
    search_value = request.GET.get('search[value]', '')
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    print(request.GET)
    print(field_name)
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    print(order_by_field)
    reports_logs_data = Reports_logs.objects.all().order_by(order_by_field)


    # if search_value:
    #     reports_logs_data = reports_logs_data.filter(
    #         Q(timestamp__icontains=search_value) | Q(log_level__icontains = search_value)|
    #         Q(method_name__icontains = search_value) | Q(log_message__icontains = search_value) |
    #         Q(log_file_type_name__icontains = search_value)
    #     )

    pagintor = Paginator(reports_logs_data, length)
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
        'recordsTotal':reports_logs_data.count(),
        'recordsFiltered':reports_logs_data.count(),
        'data':data
    }

    return JsonResponse(response)

def get_error_logs(request):
    draw = int(request.GET.get('draw',0))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))
    search_value = request.GET.get('search[value]', '')
    field_index = request.GET.get('order[0][column]')
    field_name = request.GET.get(f'columns[{field_index}][data]')
    direction = request.GET.get('order[0][dir]')
    
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    error_logs_data = Error_logs.objects.all().order_by(order_by_field)


    # if search_value:
    #     error_logs_data = error_logs_data.filter(
    #         Q(timestamp__icontains=search_value) | Q(log_level__icontains = search_value)|
    #         Q(method_name__icontains = search_value) | Q(log_message__icontains = search_value) |
    #         Q(log_file_type_name__icontains = search_value) | Q(traceback__icontains = search_value) |
    #         Q(exceptionName__icontains = search_value) | Q(log_file_type_name__icontains = search_value)
    #     )

    paginator = Paginator(error_logs_data,length)
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
        'recordsTotal':error_logs_data.count(),
        'recordsFiltered':error_logs_data.count(),
        'data':data
    }

    return JsonResponse(response)
