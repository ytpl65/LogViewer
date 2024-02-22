from django.urls import path 
from log_app import views
urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard_data/',views.get_dashboard_data, name='dashboard-data'),
    path('particular_id_data/<int:pk>/<str:log_type>/<str:is_error_table>', views.get_particular_data, name='get_particular_data'),
    path('get-youtility-logs-data',views.get_youtility_logs, name='youtility-logs'),
    path('get-mobileservice-logs-data',views.get_mobileservices_logs, name='mobileservices'),
    path('get-reports-logs',views.get_reports_logs, name = 'reportslogs'),
    path('get-error-logs',views.get_error_logs, name = 'errorlogs'),
    path('get_reports_graph_data', views.get_reports_graph_data, name='reports-graph-data'),
    path('get_mobileservices_graph_data', views.get_mobileservices_graph_data, name='mobileservice-graph-data'),
    path('get_youtility_graph_data', views.get_youtility_graph_data, name='youtility-graph-data'),
    path('get_piechart_data',views.get_piechart_data, name='piechart_data'),
    
]