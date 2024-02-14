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
  var page = 1
  console.log('Youtility Logs Show')
  document.getElementById('youtility_logs').style.display='block';
  document.getElementById('mobileserives_logs').style.display='none';
  document.getElementById('reports_logs').style.display='none';
  document.getElementById('error_logs').style.display='none';
  console.log("Server Side Code")
  $(document).ready(function() {
      $('#youtility_logs_table').DataTable({
          "orderCellsTop":true,
          "fixedHeader": true,
          "processing": true,
          "serverSide": true,
          "ajax": {
              "url": "/get-youtility-logs-data",
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
            {
                targets:4,
                "orderable":false,
                "searchable":false
            }
          ]
      });
  });

}

// mobileservicelogs
document.getElementById('mobileserives_logs_dropdown').onclick = function () {
  console.log('MobileService Logs Show')
  document.getElementById('youtility_logs').style.display='none';
  document.getElementById('mobileserives_logs').style.display='block';
  document.getElementById('reports_logs').style.display='none';
  document.getElementById('error_logs').style.display='none';
  
  $(document).ready(function() {
    
      $('#mobileservice_logs_table').DataTable({
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
        $('#reports_logs_table').DataTable(
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
    })
}


document.getElementById('errors_logs_dropdown').onclick = function (){
    document.getElementById('reports_logs').style.display='none';
    document.getElementById('youtility_logs').style.display='none';
    document.getElementById('mobileserives_logs').style.display='none';
    document.getElementById('error_logs').style.display='block';
    console.log("Starting Datablae Code")
    $(document).ready(function (){
        $('#error_logs_table').DataTable(
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
    })
}
