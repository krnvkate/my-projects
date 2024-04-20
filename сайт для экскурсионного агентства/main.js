'use strict';
const url = 
    new URL('http://exam-2023-1-api.std-900.ist.mospolytech.ru/api');
const API_KEY = '6dfde9c9-c88d-408b-8676-995c8ade91a1';

let button = document.querySelector('#create');

let today = new Date();
let tomorrow = new Date(today);
tomorrow.setDate(today.getDate() + 1);
let tomorrowFormatted = tomorrow.toISOString().split('T')[0];
document.getElementById('today-date').setAttribute('min', tomorrowFormatted);

document.getElementById('today-date').valueAsDate = tomorrow;

let currentTime = new Date();
const timeInput = document.getElementById('timeCheck');
let hours = currentTime.getHours().toString().padStart(2, '0');
let minutes = currentTime.getMinutes().toString().padStart(2, '0'); 
let timeString = hours + ':' + minutes;
timeInput.value = timeString;


let previousValue = timeInput.value;
timeInput.onchange = function() {
    if (timeInput.value < timeInput.min 
        || timeInput.value > timeInput.max) {
        timeInput.value = previousValue;
    }
    previousValue = timeInput.value;
};    


function getMainObject() {
    const select = document.getElementById('routes-select');  
    select.innerHTML = '';
    const option = document.createElement('option');
    option.textContent = 'Не выбрано';
    select.appendChild(option);  
}

function numberOfPeople(numberOfVisitors) {
    let peopleAddPrice = Number(0);
    if (1 <= numberOfVisitors && numberOfVisitors < 5) {
        peopleAddPrice = Number(0);
    } else if (5 <= numberOfVisitors && numberOfVisitors < 10) {
        peopleAddPrice = Number(1000);
    } else {
        peopleAddPrice = Number(1500);
    }
    return peopleAddPrice;

}

function isItMorningOrEvening() {
    let timeAdd = Number(0);
    if (timeInput.value >= "09:00" && timeInput.value <= "12:00") {
        timeAdd = Number(400);
    } else if (timeInput.value >= "20:00" && timeInput.value <= "23:00") {
        timeAdd = Number(1000);
    }
    return timeAdd;
}

function calculateItogPrice() {

    let guideServiceCost = 
        Number(document.querySelector('.price-per-hour').textContent);
    let hoursNumber = Number(document.getElementById('select-duration').value);
    let numberOfVisitors = 
        Number(document.getElementById('number-of-persons').value);
    let addPrice = numberOfPeople(numberOfVisitors);
    let timeAdd = Number(isItMorningOrEvening());
    let option1 = document.getElementById('opt-1');
    let option2 = document.getElementById('opt-2');
    let price = 
        Math.floor(Number(guideServiceCost * hoursNumber + timeAdd + addPrice));
    if (option1.checked) {
        price = Math.floor(price * Number(0.85));
    } else { 

    }
    if (option2.checked) {
        price += Number(500 * numberOfVisitors);
    }
    document.getElementById('itog-price').textContent = price;
               
}

function populate(data) {
    let table = document.getElementById('table-guides');
    data.forEach(function (item) {
        let row = table.insertRow();
        let cell = row.insertCell(0);
        let cell1 = row.insertCell(1);
        let cell2 = row.insertCell(2);
        let cell3 = row.insertCell(3);
        let cell4 = row.insertCell(4);
        let cell5 = row.insertCell(5);
        let img = document.createElement('img');
        img.src = 'photo/human.png';
        cell.appendChild(img);
        cell1.textContent = item.name;
        cell2.textContent = item.language;
        cell3.textContent = item.workExperience;
        cell4.textContent = item.pricePerHour;
        let btn = document.createElement('button');
        btn.textContent = 'Выбрать';
        cell5.appendChild(btn);
        btn.onclick = function (event) {
            document.querySelector('.name-guide').textContent = item.name;
            document.querySelector('.language').textContent = item.language;
            document.querySelector('.price-per-hour').textContent 
                = item.pricePerHour;
            document.querySelector('.guide-id').textContent = item.id;    
            let colorBtn = event.target;
            let rows = table.getElementsByTagName('tr');
            for (let i = 0; i < rows.length; i++) {
                colorBtn.style.background = 'initial';
            }
            colorBtn.style.background = 'lightgrey';
            calculateItogPrice();    
        };
    });
}

function getLanguage(data) {
    let table = document.getElementById('table-guides');
    const select = document.getElementById('routes-guides');  
    select.innerHTML = '';
    const option = document.createElement('option');
    option.textContent = 'Язык экскурсии';
    select.appendChild(option);
    const option1 = document.createElement('option');
    option1.textContent = 'Не выбрано';
    select.appendChild(option1);
    let languages = [];
    data.forEach(function (item) {
        if (!languages.includes(item.language)) {
            const option = document.createElement('option');
            option.textContent = item.language;    
            select.appendChild(option);
            languages.push(item.language);
        }        
    });
    select.addEventListener('change', function () {
        let selectedLanguage = select.value;
        Array.from(table.rows).forEach(function (row, index) {
            if (index !== 0 && row.cells.length > 2) {
                let cellLanguage = row.cells[2].textContent;
                if (cellLanguage === selectedLanguage 
                    || selectedLanguage === 'Не выбрано' 
                    || selectedLanguage === 'Язык экскурсии') {
                    row.style.display = '';
                } else row.style.display = 'none';
            } 
        });
    });       
}


function getSecondTableData(id) {
    let xhr = new XMLHttpRequest();
    let urlGuides = new URL(url + `/routes/${id}/guides`);
    urlGuides.searchParams.set('api_key', API_KEY);
    xhr.open('GET', urlGuides);
    xhr.responseType = 'json';
    xhr.onload = function () {
        if (xhr.status === 200) {
            let data = xhr.response;
            populate(data);
            getLanguage(data);
        } else {
            alert('Ошибка при получении данных таблицы гидов');
            console.error('Failed to fetch data: ' + xhr.status);
        }
    };
    xhr.send();
}

const perPage = 5;
let currentPage = 1;
const maxPages = 3;
const tableHead = 
    document.getElementById('table-routes')
        .getElementsByTagName('thead')[0].innerHTML;       


function tableRoutes(data) {
    let table = document.getElementById('table-routes');
    let tbody = document.getElementById('table-routes-body');
    tbody.innerHTML = '';

    table.getElementsByTagName('thead')[0].innerHTML = tableHead;
    const totalPages = Math.ceil(data.length / perPage);
    let pagination = document.getElementById('pagination');
    pagination.innerHTML = '';

    let startPage = 1;
    let endPage = totalPages;

    if (totalPages > maxPages) {
        startPage = Math.max(1, currentPage - Math.floor(maxPages / 2));
        endPage = Math.min(totalPages, startPage + maxPages - 1);

        if (endPage - startPage < maxPages - 1) {
            startPage = endPage - maxPages + 1;
        }
    }

    if (currentPage > 1) {
        let previousBtn = document.createElement('button');
        previousBtn.textContent = 'Назад';
        previousBtn.classList.add('page-link');
        previousBtn.id = "scrollPrevious";
        previousBtn.addEventListener('click', function () {
            currentPage -= 1;
            tableRoutes(data);
        });
        pagination.appendChild(previousBtn);
    }

    for (let i = startPage; i <= endPage; i++) {
        let li = document.createElement('li');
        let btn = document.createElement('button');
        btn.classList.add('page-link');
        btn.id = "scrollBtn";
        btn.textContent = i;
        if (i === currentPage) {
            btn.disabled = true;
        }
        btn.addEventListener('click', function () {
            currentPage = i;
            tableRoutes(data); 
        });
        li.appendChild(btn);
        pagination.appendChild(li);
    }

    if (currentPage < totalPages) {
        let nextBtn = document.createElement('button');
        nextBtn.textContent = 'Вперед';
        nextBtn.classList.add('page-link');
        nextBtn.id = "scrollNext";
        nextBtn.addEventListener('click', function () {
            currentPage += 1;
            tableRoutes(data);
        });
        pagination.appendChild(nextBtn);
        
    }

    const start = (currentPage - 1) * perPage;
    const end = currentPage * perPage;

    data.slice(start, end).forEach(function (item) {
        let row = tbody.insertRow();
        let cell1 = row.insertCell(0);
        let cell2 = row.insertCell(1);
        let cell3 = row.insertCell(2);
        let cell4 = row.insertCell(3);
        cell1.textContent = item.name;
        cell2.textContent = item.description;
        cell3.textContent = item.mainObject;
        let btn = document.createElement('button');
        btn.textContent = 'Выбрать';
        cell4.appendChild(btn);
        btn.onclick = function (event) {
            document.getElementById('route-name').textContent = item.name;
            document.querySelector('.name-route').textContent = item.name;
            document.querySelector('.route-id').textContent = item.id;
            getSecondTableData(item.id);
            let colorBtn = event.target;
            let rows = table.getElementsByTagName('tr');
            for (let i = 0; i < rows.length; i++) {
                colorBtn.style.background = 'initial';
            }
            colorBtn.style.background = 'lightgrey';
        };
    });
}


function getTableData() {
    let xhr = new XMLHttpRequest();
    let urlRoutes = new URL(url + `/routes`);
    urlRoutes.searchParams.set('api_key', API_KEY);
    xhr.open('GET', urlRoutes);
    xhr.responseType = 'json';
    xhr.onload = function () {
        if (xhr.status === 200) {
            let data = xhr.response;
            tableRoutes(data);
            getMainObject();
        } else {
            alert('Ошибка при получении данных таблицы маршрутов');
            console.error('Failed to fetch data: ' + xhr.status);
        }
    };
    xhr.send();
}

button.addEventListener('click', function() {
    let xhr = new XMLHttpRequest();
    let urlToSendOrder = new URL(url + `/orders`);
    urlToSendOrder.searchParams.set('api_key', API_KEY);

    let guideId = (document.querySelector('.guide-id').textContent);
    let routeId = Number(document.querySelector('.route-id').textContent);
    let date = document.getElementById('today-date').value;
    let timeData = document.getElementById('timeCheck').value + ':00';
    let personsData = 
        Number(document.getElementById('number-of-persons').value);  
    let duration = Number(document.getElementById('select-duration').value);
    let totalPrice = 
        Number(document.getElementById('itog-price').textContent);   
    let optionFirst = Number(document.getElementById('opt-1').checked);
    let optionSecond = Number(document.getElementById('opt-2').checked);
    
    let data = new FormData();
    data.append("guide_id", guideId);
    data.append("route_id", routeId);
    data.append("date", date); 
    data.append("time", timeData);
    data.append("duration", duration);
    data.append("persons", personsData);
    data.append("price", totalPrice);
    data.append("optionFirst", optionFirst); 
    data.append("optionSecond", optionSecond);

    xhr.open("POST", urlToSendOrder);
    xhr.responseText;
    xhr.onload = function() {
        if (xhr.status != 200) {
            alert(`Ошибка ${xhr.status}: ${xhr.statusText}`);
        } else {
            alert(`Заявка успешно отправлена!`);
        }
    };
    
    xhr.send(data);


});

window.onload = function () {
    getTableData();
    document.getElementById('route-name').innerHTML = '';
    document.querySelector('.name-route').innerHTML = '';
    document.querySelector('.name-guide').innerHTML = '';
    document.querySelector('.language').innerHTML = '';
    let modal = document.getElementById('createModal');
    let inputs = modal.getElementsByTagName('input');
    Array.from(inputs).forEach(function(input) {
        input.addEventListener('input', function() {
            calculateItogPrice();
        });
    });
    let selects = modal.getElementsByTagName('select');
    Array.from(selects).forEach(function(select) {
        select.addEventListener('change', function() {
            calculateItogPrice();
        });
    });
            
        
};