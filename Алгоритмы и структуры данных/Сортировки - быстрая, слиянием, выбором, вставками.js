// Требующийся функционал программы:
// 1)Создание массива случайных элементов заданного в интерфейсе размера.
// 2)Реализация выбора алгоритма сортировки 
// (вставками, выбором, слиянием, быстрая)
// 3)Возможность дублирования массива для применения одинакового
//  массива для всех алгоритмов.
function randomInteger(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1) + min); 
    // Максимум и минимум включаются
}
function getAnswer(nameOfFunction, array) {
    let time = performance.now();
    nameOfFunction(array);
    time = performance.now() - time;
    return [time, array];
}
array = [];
const prompt = require("prompt-sync")({sigint: true});
let min = prompt('Введите начало диапазона: ');
let max = prompt('Введите конец диапазона: ');
let lengthOfArray = prompt('Введите размер массива: ');

for (let i = 0; i < lengthOfArray; i++) {
    array.push(randomInteger(min, max));
}
console.log(array);

let sort = Number(prompt(`Выберите сортировку
(1-вставками, 2-выбором,3-слиянием, 4-быстрая, 5-все): `));

function insertionSort(arr) { 
    for (let i = 1; i < arr.length; i++) { 
        let current = arr[i]; 
        let j = i - 1; 
        while ((j > -1) && (current < arr[j])) { 
            arr[j + 1] = arr[j]; 
            j--; 
        } 
        arr[j + 1] = current; 
    } 
    return arr; 
} 

function selectionSort(arr) { 
    for (let i = 0; i < arr.length; i++) {
        let min = i;
        for (let j = i; j < arr.length; j++) {
            if (arr[j] < arr[min]) {
                min = j; 
            }
        }
        if (min != i) {
            let tmp = arr[i]; 
            arr[i] = arr[min];
            arr[min] = tmp;      
        }
    }
    return arr;
}

function merge(left, right) {
    let arr = [];
    while (left.length && right.length) {
        if (left[0] < right[0]) {
            arr.push(left.shift());  
        } else {
            arr.push(right.shift()); 
        }
    }

    return [...arr, ...left, ...right];
}

function mergeSort(array) {
    const half = array.length / 2;
    if (array.length < 2) {
        return array; 
    }
    const left = array.splice(0, half);
    return merge(mergeSort(left), mergeSort(array));
}


function quickSort(arr) {
    if (arr.length == 0) return [];
    let a = [], b = [], p = arr[0];
    for (let i = 1; i < arr.length; i++) { 
        if (arr[i] < p) {
            a[a.length] = arr[i];
        } else b[b.length] = arr[i];
    }
    return quickSort(a).concat(p, quickSort(b));
}

function what(sort) {
    switch (sort) {
    case 1:
        console.log("Время выполнения в ms и массив: ",
            getAnswer(insertionSort, Array.from(array)));
        break;
    case 2:
        console.log("Время выполнения в ms и массив: ",
            getAnswer(selectionSort, Array.from(array)));
        break;
    case 3:
        let timeMerge = performance.now();
        arr = mergeSort(Array.from(array));
        timeMerge = performance.now() - timeMerge;
        console.log("Время выполнения: ", timeMerge, "ms", "\n", arr);
        break;
    case 4:
        let timeQuick = performance.now();
        arr = quickSort(Array.from(array));
        timeQuick = performance.now() - timeQuick;
        console.log("Время выполнения: ", timeQuick, "ms", "\n", arr);
        break;
    case 5:
        console.log("Вставками. Время выполнения в ms и массив: ",
            getAnswer(insertionSort, Array.from(array)));
        console.log("Выбором. Время выполнения в ms и массив: ",
            getAnswer(selectionSort, Array.from(array))); 
        let timeM = performance.now();
        arr = mergeSort(Array.from(array));
        timeM = performance.now() - timeM;
        console.log("Слиянием. Время выполнения: ", timeM, "ms", "\n", arr);
        let timeQ = performance.now();
        arr = quickSort(Array.from(array));
        timeQ = performance.now() - timeQ;
        console.log("Быстрая. Время выполнения: ", timeQ, "ms", "\n", arr);
        break;      
    default:
        console.log("Нет такой команды");
            
    }
} 
what(sort);   

