console.log("All set ")

// document.getElementById('youtility_logs_dropdown').onclick = function () {
//     var page = 1
//     console.log('Youtility Logs Show')
//     document.getElementById('youtility_logs').style.display='block';
//     document.getElementById('mobileserives_logs').style.display='none';
//     document.getElementById('reports_logs').style.display='none';
//     new DataTable('#youtility_logs_table',{
//         ajax: `{% url 'youtility-logs' %}`,
//         processing: true,
//         serverside: true
//     })
// }

document.getElementById('mobileserives_logs_dropdown').onclick = function () {
    console.log('Mobile Logs Show')
    document.getElementById('mobileserives_logs').style.display='block';
    document.getElementById('youtility_logs').style.display='none';
    document.getElementById('reports_logs').style.display='none';
}

document.getElementById('reports_logs_dropdown').onclick = function () {
    console.log('Youtility Logs Show')
    document.getElementById('reports_logs').style.display='block';
    document.getElementById('youtility_logs').style.display='none';
    document.getElementById('mobileserives_logs').style.display='none';

}


// function getYoutilityLogs() {
//     fetch('get-youtility-logs-data')
//     .then(response=>response.json())
//     .then(data => {
//         // const logs = JSON.parse(data.logs)
//         const logs = data.logs
//         const table = document.createElement('table');
//         table.innerHTML = `
//         <tr>
//         <th>Sr. No</th>
//         <th>Timestamp</th>
//         <th>Log Level</th>
//         <th>Method Name</th>
//         <th>Log Message</th>
//         <th>View</th>
//         </tr>
//         `
//         // const ele = document.createElement('a')
//         // ele.innerHTML = 'View'
//         logs.forEach((log, index) => {
//             const row = table.insertRow(-1); // -1 appends the row to the end of the table
//             row.insertCell(0).textContent = index + 1;
//             row.insertCell(1).textContent = log.timestamp;
//             row.insertCell(2).textContent = log.log_level;
//             row.insertCell(3).textContent = log.method_name;
//             row.insertCell(4).textContent = log.log_message;
//             const viewCell = row.insertCell(5); 
//             const viewLink = document.createElement('a'); 
//             viewLink.href = "#"; 
//             viewLink.textContent = 'view';
//             viewCell.appendChild(viewLink);
//         });
//         document.getElementById('youtility_logs_table').innerHTML = '';
//         document.getElementById('youtility_logs_table').appendChild(table);
//         table.className = 'table table-striped table-hover';
//     })
// }


// function getMobileServicesLogs() {
//     fetch('get-mobileservice-logs-data')
//     .then(response=>response.json())
//     .then(data => {
//         const logs = data.logs
//         const table = document.createElement('table');
//         table.innerHTML = `
//         <tr>
//         <th>Sr. No</th>
//         <th>Timestamp</th>
//         <th>Log Level</th>
//         <th>Method Name</th>
//         <th>Log Message</th>
//         <th>View</th>
//         </tr>
//         `

//         logs.forEach((log, index) => {
//             const row = table.insertRow(-1); // -1 appends the row to the end of the table
//             row.insertCell(0).textContent = index + 1;
//             row.insertCell(1).textContent = log.timestamp;
//             row.insertCell(2).textContent = log.log_level;
//             row.insertCell(3).textContent = log.method_name;
//             row.insertCell(4).textContent = log.log_message;
//             const viewCell = row.insertCell(5); 
//             const viewLink = document.createElement('a'); 
//             viewLink.href = "#"; 
//             viewLink.textContent = 'view';
//             viewCell.appendChild(viewLink);
//         });
//         document.getElementById('mobileservice_logs_table').innerHTML = '';
//         document.getElementById('mobileservice_logs_table').appendChild(table);
//         table.className = 'table table-striped table-hover';
//     }
//     )


// }


document.getElementsByClassName('.view')