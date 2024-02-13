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

    print(direction)

    
    order_by_field = f'-{field_name}' if direction == 'desc' else field_name
    youtility_logs_data = Youtility_logs.objects.all().order_by(order_by_field)



    if search_value:
        youtility_logs_data = youtility_logs_data.filter(
            Q(timestamp__icontains=search_value) | Q(log_level__icontains = search_value) |
            Q(method_name__icontains=search_value) |  Q(log_message__icontains = search_value) |
            Q(log_file_type_name__icontains = search_value) )

    paginator = Paginator(youtility_logs_data,length)
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
        'recordsTotal':youtility_logs_data.count(),
        'recordsFiltered':youtility_logs_data.count(),
        'data':data
    }

    return JsonResponse(response)

def get_mobileservices_logs(request):
    if request.method == 'GET':
        mobileservices_logs = Mobileservices_logs.objects.order_by('-timestamp')[0:100]
        logs_list = list(mobileservices_logs.values('timestamp','log_level','method_name','log_message'))
        print(logs_list)
    return JsonResponse({'logs':logs_list})

