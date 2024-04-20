// Требующийся функционал программы:
// 1) Создание массива случайных элементов заданного в интерфейсе размера.
// 2) Функции поиска, вставки и удаления по случайному массиву.
// 3) Создание упорядоченного массива заданного в интерфейсе размера.
// 4) Функции поиска, двоичного поиска, вставки и удаления 
// из упорядоченного массива.
function randomInteger(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min); 
    // Максимум и минимум включаются
}
array = [];
const prompt = require("prompt-sync")({sigint: true});
console.log('Первая часть');
let min = prompt('Введите начало диапазона: ');
let max = prompt('Введите конец диапазона: ');
let lengthOfArray = prompt('Введите размер массива: ');

for (let i = 0; i < lengthOfArray; i++) {
    array.push(randomInteger(min, max));
}
console.log(array);


let numb = Number(prompt('Введите элемент для поиска индекса: '));

function searchInArray(arr, element) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === element) {
            return i;
        }
    }
    return -1; 
}
let time = performance.now();
let index = searchInArray(array, numb);
time = performance.now() - time;

console.log('Индекс искомого элемента: ', index,
    `Время выполнения = ${time} ms`);

let newElement = prompt('Введите элемент, который хотите вставить: ');
let time1 = performance.now();
array.push(Number(newElement));
time1 = performance.now() - time1;

console.log('Новый массив: ', array,
    `\nВремя выполнения = ${time} ms`);

let delElement = Number(prompt('Введите элемент, который хотите удалить: '));
function deleteFromArray(arr, element) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === element) {
            index = i;
        }
    }
    index = -1; 
    if (index !== -1) {
        arr.splice(index, 1);
    }
}
timeDel = performance.now();
deleteFromArray(array, delElement);
timeDel = performance.now() - timeDel;

console.log('Новый массив: ', array,
    '\nВремя выполнения =', time, 'ms');


console.log('Вторая часть');
let orderedArray = [];
function createOrderedArray(size) {
    for (let i = 1; i <= size; i++) {
        orderedArray.push(i);
    }
    return orderedArray;
}    

let size = Number(prompt('Введите размер массива: '));
let time2 = performance.now();
orderedArray = createOrderedArray(size);
time2 = performance.now() - time2;

console.log(orderedArray, '\nВремя выполнения =', time2, 'ms');

function linearSearch(arr, item) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === item) {
            return i;
        }
    }
    return -1; 
}  


let linearElement = Number(prompt('Введите элемент для поиска индекса: '));

let timeLinear = performance.now();
index = linearSearch(orderedArray, linearElement);
timeLinear = performance.now() - timeLinear;
console.log('Индекс искомого элемента: ', index,
    `Время выполнения = ${timeLinear} ms`);

// Функция двоичного поиска
function binarySearch(arr, item) {
    let low = 0;
    let high = arr.length - 1;

    while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        if (arr[mid] === item) {
            return mid; 
        }
        if (arr[mid] > item) {
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }
    return -1;
} 

let binearElement = 
    Number(prompt('Введите элемент для двоичного поиска индекса: '));

let timeBinear = performance.now();
indexBinear = binarySearch(orderedArray, binearElement);
timeBinear = performance.now() - timeBinear;
console.log('Индекс искомого элемента: ', indexBinear,
    `Время выполнения = ${timeBinear} ms`);

    
// Функция удаления из упорядоченного массива
function binaryDelete(arr, elem) {
    let low = 0;
    let high = arr.length - 1;
    while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        if (arr[mid] === elem) {
            arr.splice(mid, 1);
            return arr;
        } else if (arr[mid] < elem) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return arr;
}    

let deleteOrderElement = 
    Number(prompt('Введите элемент, который хотите удалить: '));
let timeDelete = performance.now();
orderedArray = binaryDelete(orderedArray, deleteOrderElement);
timeDelete = performance.now() - timeDelete;
console.log('Изменённый массив: ', orderedArray,
    `\nВремя выполнения = ${timeDelete} ms`);

// Функция вставки в упорядоченный массив
function binaryInsert(arr, elem) {
    let low = 0;
    let high = arr.length - 1;
    
    while (low <= high) {
        let mid = Math.floor((low + high) / 2);
        if (arr[mid] < elem) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    
    arr.splice(low, 0, elem);
    return arr;
}
let insertOrderElement = 
    Number(prompt('Введите элемент, который хотите добавить: '));
let timeInsert = performance.now();
orderedArray = binaryInsert(orderedArray, insertOrderElement);
timeInsert = performance.now() - timeInsert;
console.log('Изменённый массив: ', orderedArray,
    `\nВремя выполнения = ${timeInsert} ms`);