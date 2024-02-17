
flatpickr("#datetimepicker",
              {
          mode: "range",
          enableTime: true,
          dateFormat: "Y-m-d H:i:S",
      }
        );

function toUserFriendlyDateTime(data){
    var date = new Date(data);
    return date.toLocaleString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: true
    });
}



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

  function reduceTextLength(data, type, row, length){
    if (type === 'display') {
        if (data && typeof data === 'string') {
            return data.length > length ? data.substring(0, length) + '...' : data;
        }
        return data; // Handle non-string or empty values gracefully.
    }
    return data; // Ensure data is returned for all types.
}

  function addViewLink(data, type, row){
    if (type === 'display') {
        // return `<a class="view" href="#">View</a>`;
        return `<a class="view" href="${data[0]}" id="${data[0]}" log_type="${data[1]}" is_error_table_data="${data[2]} " class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" >View</a>`; 
    }
    return ''; // Return an empty string or the original data for non-display types, depending on your needs.
}

// $(document).ready(function() {
//     $(`a.view`).click(function(e){
//         e.preventDefault();
//         console.log("Anchor Tag Clicked")

//     })
// })

function formattedJsonData(data){
    var formattedJson = JSON.stringify(data, null, 2);
    var formattedData = formattedJson.replace(/\\n/g, "<br>");
    return formattedData
}


$(document).ready(function() {
    // Using the document to delegate the click event to dynamically added `a.view` elements
    $(document).on('click', 'a.view', function(e) {
        e.preventDefault(); // Prevent the default anchor action
        // console.log(e)
        // console.log(e.target.id)
        var id = $(this).attr('id')
        var log_type = $(this).attr('log_type')
        var is_error_table_data = $(this).attr('is_error_table_data')
        console.log(id ,log_type, is_error_table_data)
        $.ajax({
            url:`particular_id_data/${id}/${log_type}/${is_error_table_data}`,
            dataType:'json',
            success:function(data){
                var response = data.data
                var timestamp = toUserFriendlyDateTime(response.timestamp)
                var log_type = response.log_type
                if (log_type === undefined){
                    console.log("Normal Log")
                    $('#timestampValue').text(timestamp);
                    $('#logLevelValue').text(response.log_level);
                    $(`#methodNameValue`).text(response.method_name);
                    // var formattedJson = JSON.stringify(response.log_message, null, 2)
                    // var formattedData = formattedJson.replace(/\\n/g, "<br>")
                    formattedData = formattedJsonData(response.log_message)
                    $(`#logmessageValue`).html(formattedData);

                }
                else{
                    console.log("Error Log", log_type)
                    $('#timestampValue').text(timestamp);
                    $('#logLevelValue').text(response.log_level);
                    $(`#methodNameValue`).text(response.method_name);
                    // var formattedJson = JSON.stringify(response.log_message, null, 2)
                    // var formattedData = formattedJson.replace(/\\n/g, "<br>")
                    formattedData = formattedJsonData(response.log_message)
                    $(`#logmessageValue`).html(formattedData);

                }
                // $('#timestampValue').text(timestamp);
                // $('#logLevelValue').text(response.log_level);
                // $(`#methodNameValue`).text(response.method_name);
                // var formattedJson = JSON.stringify(response.log_message, null, 2)
                // var formattedData = formattedJson.replace(/\\n/g, "<br>")
                // $(`#logmessageValue`).html(formattedData);
                
            }
        })

        // Your code here to handle the click event
    });
});





document.getElementById('youtility_logs_dropdown').onclick = function () {
  console.log('Youtility Logs Show')
  document.getElementById('youtility_logs').style.display='block';
  document.getElementById('mobileserives_logs').style.display='none';
  document.getElementById('reports_logs').style.display='none';
  document.getElementById('error_logs').style.display='none';
  console.log("Server Side Code")
    var table = $('#youtility_logs_table').DataTable({
           retrieve: true,
          "processing": true,
          "serverSide": true,
          "ajax": {
              "url": "/get-youtility-logs-data",
              "type": "GET"
          },
          "columns": [
              { "data": "timestamp", "width":"15%"},
              { "data": "log_level", "width":"10%"},
              { "data": "method_name","width":"15%"},
              { "data": "log_message"},
              {"data": "view", "width":"5%"}
          ],
          dom: 'lrtip',
          "columnDefs":[
            {
            targets:0,
              "render": function(data, type, row){
                return toUserFriendlyTimeStamp(data, type, row)
              }},
            {
            targets:3,
              "render":function(data, type, row){
                return reduceTextLength(data, type, row, 140)
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
    $(function() {
      var table = $('#mobileservice_logs_table').DataTable({
                retrieve: true,
               dom: 'lrtip',
              "processing": true,
              "serverSide": true,
              "ajax": {
                  "url": "/get-mobileservice-logs-data",
                  "type": "GET"
              },
              "columns": [
                  // Specify your column data here
                //   { "data": "timestamp", "title": "Time Stamp"},
                //   { "data": "log_level", "title": "Log Level" },
                //   { "data": "method_name" , "title": "Method Name"},
                //   { "data": "log_message", "title": "Log Message" },
                //   {"data": "view", "title": "View"}
                { "data": "timestamp", "width":"15%"},
                  { "data": "log_level", "width":"10%"},
                  { "data": "method_name","width":"15%"},
                  { "data": "log_message"},
                  {"data": "view", "width":"5%"}
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
                    return reduceTextLength(data, type, row, 140)
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
    $(function () {
        console.log("Inside")
    var table = $('#reports_logs_table').DataTable(
            {
            retrieve: true,
            dom: 'lrtip',
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
                { "data": "timestamp", "width":"15%"},
                { "data": "log_level", "width":"10%"},
                { "data": "method_name","width":"15%"},
                { "data": "log_message"},
                {"data": "view", "width":"5%"}
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
                        return reduceTextLength(data, type, row, 140)
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
    $(function (){
    var table = $('#error_logs_table').DataTable(
            {
                retrieve: true,
                dom: 'lrtip',
                "processing":true,
                "serverSide":true,
                "ajax":{
                    "url":"/get-error-logs",
                    "type":"GET"
                },
                "columns":[
                    { "data": "timestamp", "width":"15%"},
                    { "data": "log_level", "width":"7%"},
                    { "data": "method_name","width":"15%"},
                    { "data": "log_message"},
                    {"data":"traceback","title":"Traceback"},
                    {"data":"exceptionName","title":"Exception"},
                    {"data":"log_file_type_name","width":"7%"},
                    {"data": "view", "width":"5%"}
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
                            return reduceTextLength(data, type, row, 30)
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
                            return reduceTextLength(data, type, row, 30)
                        }
                    },
                    {
                        "targets":5,
                        "render":function(data,type,row){
                            return reduceTextLength(data, type, row, 30)
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


$(function(){
    $("button#sendComment").click(function(){
        var comment = $('developerComment').val()
        console.log("Form Data Submitted", comment)
    })
})