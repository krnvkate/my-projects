'use strict';
const url = 
    new URL('http://exam-2023-1-api.std-900.ist.mospolytech.ru/api');
const API_KEY = '6dfde9c9-c88d-408b-8676-995c8ade91a1';
let currentPage = 1;
let recordsPerPage = 5;
let orderData = [];
let routesData = [];
let table = document.getElementById('application-table');

function getData(url, callback) {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                let data = JSON.parse(xhr.responseText);
                callback(data);
            } else {
                alert('Ошибка получения данных о заявках');
                console.error('Не удалось получить данные: ' + xhr.status);
            }
        }
    };
    xhr.open('GET', url);
    xhr.send();
};
function displayData(start, end) {
    table.innerHTML = '';
    for (let i = start; i < end; i++) {
        if (i < orderData.length) {
            let row = table.insertRow(table.rows.length);
            let cell1 = row.insertCell(0);
            let cell2 = row.insertCell(1);
            let cell3 = row.insertCell(2);
            let cell4 = row.insertCell(3);
            cell1.innerHTML = i + 1;
            let matchingData = 
                routesData.find(item => item.id === orderData[i].route_id);    
            if (matchingData) {
                cell2.innerHTML = matchingData.name;
                cell3.innerHTML = orderData[i].date;
                cell4.innerHTML = orderData[i].price;
            }
        }
    }
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        let start = (currentPage - 1) * recordsPerPage;
        let end = currentPage * recordsPerPage;
        displayData(start, end);
    }
}

function nextPage() {
    if (currentPage < Math.ceil(orderData.length / recordsPerPage)) {
        currentPage++;
        let start = (currentPage - 1) * recordsPerPage;
        let end = currentPage * recordsPerPage;
        displayData(start, end);
    }
}
let urlOrders = new URL(url + `/orders`);
urlOrders.searchParams.set('api_key', API_KEY);

let urlRoutes = new URL(url + `/routes`);
urlRoutes.searchParams.set('api_key', API_KEY);


window.onload = function () {
    getData(urlOrders, function (data) {
        orderData = data;
        getData(urlRoutes, function (data) {
            routesData = data;
            displayData(0, recordsPerPage); 
        });
    
    });
    document.getElementById("prevBtn").onclick = prevPage;
    document.getElementById('nextBtn').onclick = nextPage;
};