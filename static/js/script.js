function toUserFriendlyTimeStamp(data, type, row){
    if (type === 'display' || type === 'filter') {
        var date = new Date(data);
        return date.toLocaleString('en-US', {
            year: 'numeric', month: 'short', day: 'numeric',
            hour: '2-digit', minute: '2-digit', second: '2-digit',
            hour12: true
        });
    }
    return data; // Return unmodified data for sorting or type detection
  }

  function reduceTextLength(data, type, row){
    if (type === 'display') {
        if (data && typeof data === 'string') {
            return data.length > 30 ? data.substring(0, 30) + '...' : data;
        }
        return data; // Handle non-string or empty values gracefully.
    }
    return data; // Ensure data is returned for all types.
}

  function addViewLink(data, type, row){
    if (type === 'display') {
        return '<a class="view" href="#">View</a>'; // Assuming you want to always display the link for viewing details.
    }
    return ''; // Return an empty string or the original data for non-display types, depending on your needs.
}

document.getElementById('youtility_logs_dropdown').onclick = function () {
  console.log('Youtility Logs Show')
  document.getElementById('youtility_logs').style.display='block';
  document.getElementById('mobileserives_logs').style.display='none';
  document.getElementById('reports_logs').style.display='none';
  document.getElementById('error_logs').style.display='none';
  console.log("Server Side Code")
    var table = $('#youtility_logs_table').DataTable({
          "processing": true,
          "serverSide": true,
          "ajax": {
              "url": "/get-youtility-logs-data",
              "type": "GET"
          },
          "columns": [
              { "data": "timestamp"},
              { "data": "log_level"},
              { "data": "method_name"},
              { "data": "log_message"},
              {"data": "view"}
          ],
          "columnDefs":[
            {
            targets:0,
              "render": function(data, type, row){
                return toUserFriendlyTimeStamp(data, type, row)
              }},
            {
            targets:3,
              "render":function(data, type, row){
                return reduceTextLength(data, type, row)
              }
            },
            {
            targets:4,
            "orderable":false,
            "searchable":false,
            "render": function(data, type, row){
                return addViewLink(data,type,row)
              }
            },
            {
            targets:4,
            "orderable":false,
            "searchable":false
            }
          ],
      });
    
    $('#youtility_logs_table thead tr:eq(0) th input').each(function(i) {
        $(this).on('keypress', function(e) {
            if (e.keyCode == 13) {
                var val = this.value;
                if (table.column(i).search() !== val) {
                    table.column(i).search(val).draw();
                }
            }
        });
    });
};


// mobileservicelogs
document.getElementById('mobileserives_logs_dropdown').onclick = function () {
  console.log('MobileService Logs Show')
  document.getElementById('youtility_logs').style.display='none';
  document.getElementById('mobileserives_logs').style.display='block';
  document.getElementById('reports_logs').style.display='none';
  document.getElementById('error_logs').style.display='none';
  
  $(document).ready(function() {
  var table = $('#mobileservice_logs_table').DataTable({
          "processing": true,
          "serverSide": true,
          "ajax": {
              "url": "/get-mobileservice-logs-data",
              "type": "GET"
          },
          "columns": [
              // Specify your column data here
              { "data": "timestamp", "title": "Time Stamp"},
              { "data": "log_level", "title": "Log Level" },
              { "data": "method_name" , "title": "Method Name"},
              { "data": "log_message", "title": "Log Message" },
              {"data": "view", "title": "View"}
              // Add or remove columns as per your actual data
          ],
          "columnDefs":[
            {
              targets:0,
              "render": function(data, type, row){
                return toUserFriendlyTimeStamp(data, type, row)
              }},
            {
              targets:3,
              "render":function(data, type, row){
                return reduceTextLength(data, type, row)
              }
            },
            {
              targets:4,
              "orderable":false,
             "searchable":false,
              "render": function(data, type, row){
                return addViewLink(data,type,row)
              }
            },
          ],
      });
    $('#mobileservice_logs_table thead tr:eq(0) th input').each(function(i) {
        $(this).on('keypress', function(e) {
            if (e.keyCode == 13){
                var val = this.value;
                if (table.column(i).search()!== val){
                    table.column(i).search(val).draw();
                }
            }
        })
    })
  });

}

document.getElementById('reports_logs_dropdown').onclick = function () {
    console.log('Youtility Logs Show')
    document.getElementById('reports_logs').style.display='block';
    document.getElementById('youtility_logs').style.display='none';
    document.getElementById('mobileserives_logs').style.display='none';
    document.getElementById('error_logs').style.display='none';
    console.log("Outside Ajax Code")
    $(document).ready(function () {
        console.log("Inside")
    var table = $('#reports_logs_table').DataTable(
            {
                
            "processing":true,
            "serverSide":true,
            "ajax":{
                "url":"/get-reports-logs",
                'type':"GET"
            },
            // "dom": 'Qfrtip',
            // "search": {
            //     return: true
            // },
            "columns": [
                {"data":"timestamp", "title":"Time Stamp"},
                { "data": "log_level", "title": "Log Level" },
                { "data": "method_name" , "title": "Method Name"},
                { "data": "log_message", "title": "Log Message" },
                {"data": "view", "title": "View"}
            ],
            "columnDefs": [
                {
                    "targets":0,
                    "render":function(data, type, row){
                        return toUserFriendlyTimeStamp(data, type, row)
                    }
                },
                {
                    "targets":3,
                    "render":function (data, type, row){
                        return reduceTextLength(data, type, row)
                    }
                },
                {
                    "targets":4,
                    "orderable":false,
                    "searchable":false,
                    "render":function(data,type,row){
                        return addViewLink(data, type, row)
                    }
                },
            ]
        })
    $('#reports_logs_table thead tr:eq(0) th input').each(function(i){
        $(this).on('keypress', function(e){
            if (e.keyCode == 13){
                var val = this.value;
                if (table.column(i).search() !== val){
                    table.column(i).search(val).draw();
                }
            }
        })
    })
    })
}


document.getElementById('errors_logs_dropdown').onclick = function (){
    document.getElementById('reports_logs').style.display='none';
    document.getElementById('youtility_logs').style.display='none';
    document.getElementById('mobileserives_logs').style.display='none';
    document.getElementById('error_logs').style.display='block';
    console.log("Starting Datablae Code")
    $(document).ready(function (){
    var table = $('#error_logs_table').DataTable(
            {
                "processing":true,
                "serverSide":true,
                "ajax":{
                    "url":"/get-error-logs",
                    "type":"GET"
                },
                "columns":[
                    {"data":"timestamp","title":"Time Stamp"},
                    { "data": "log_level", "title": "Log Level" },
                    { "data": "method_name" , "title": "Method Name"},
                    { "data": "log_message", "title": "Log Message" },
                    {"data":"traceback","title":"Traceback"},
                    {"data":"exceptionName","title":"Exception"},
                    {"data":"log_file_type_name","title":"Log Type"},
                    {"data": "view", "title": "View"}
                ],
                "columnDefs":[
                    {
                        "targets":0,
                        "render":function(data,type,row){
                            return toUserFriendlyTimeStamp(data,type,row)
                        }
                    },
                    {
                        "targets":3,
                        "render":function (data, type, row){
                            return reduceTextLength(data, type, row)
                        }
                    },
                    {
                        "targets":7,
                        "orderable":false,
                        "searchable":false,
                        "render":function(data,type,row){
                            return addViewLink(data, type, row)
                        }
                    },
                    {
                        "targets":4,
                        "render":function(data,type,row){
                            return reduceTextLength(data, type, row)
                        }
                    },
                    {
                        "targets":5,
                        "render":function(data,type,row){
                            return reduceTextLength(data, type, row)
                        }
                    },
                ]            
            }
        )
    $('#error_logs_table thead tr:eq(0) th input').each(function(i) {
        $(this).on('keypress', function(e) {
            if (e.keyCode == 13) {
                var val = this.value;
                if (table.column(i).search() !== val){
                    table.column(i).search(val).draw();
                }
            }
        })
    })
    })
}
