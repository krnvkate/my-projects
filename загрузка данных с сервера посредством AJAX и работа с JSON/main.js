function createAuthorElement(record) {
    let user = record.user || { 'name': { 'first': '', 'last': '' } };
    let authorElement = document.createElement('div');
    authorElement.classList.add('author-name');
    authorElement.innerHTML = user.name.first + ' ' + user.name.last;
    return authorElement;
}

function createUpvotesElement(record) {
    let upvotesElement = document.createElement('div');
    upvotesElement.classList.add('upvotes');
    upvotesElement.innerHTML = record.upvotes;
    return upvotesElement;
}

function createFooterElement(record) {
    let footerElement = document.createElement('div');
    footerElement.classList.add('item-footer');
    footerElement.append(createAuthorElement(record));
    footerElement.append(createUpvotesElement(record));
    return footerElement;
}

function createContentElement(record) {
    let contentElement = document.createElement('div');
    contentElement.classList.add('item-content');
    contentElement.innerHTML = record.text;
    return contentElement;
}

function createListItemElement(record) {
    let itemElement = document.createElement('div');
    itemElement.classList.add('facts-list-item');
    itemElement.append(createContentElement(record));
    itemElement.append(createFooterElement(record));
    return itemElement;
}

function renderRecords(records) {
    let factsList = document.querySelector('.facts-list');
    factsList.innerHTML = '';
    for (let i = 0; i < records.length; i++) {
        factsList.append(createListItemElement(records[i]));
    }
}

function setPaginationInfo(info) {
    document.querySelector('.total-count').innerHTML = info.total_count;
    let start = info.total_count && (info.current_page - 1) 
* info.per_page + 1;
    document.querySelector('.current-interval-start').innerHTML = start;
    let end = Math.min(info.total_count, start + info.per_page - 1);
    document.querySelector('.current-interval-end').innerHTML = end;
}

function createPageBtn(page, classes = []) {
    let btn = document.createElement('button');
    classes.push('btn');
    for (cls of classes) {
        btn.classList.add(cls);
    }
    btn.dataset.page = page;
    btn.innerHTML = page;
    return btn;
}

function renderPaginationElement(info) {
    let btn;
    let paginationContainer = document.querySelector('.pagination');
    paginationContainer.innerHTML = '';

    btn = createPageBtn(1, ['first-page-btn']);
    btn.innerHTML = 'Первая страница';
    if (info.current_page == 1) {
        btn.style.visibility = 'hidden';
    }
    paginationContainer.append(btn);

    let buttonsContainer = document.createElement('div');
    buttonsContainer.classList.add('pages-btns');
    paginationContainer.append(buttonsContainer);

    let start = Math.max(info.current_page - 2, 1);
    let end = Math.min(info.current_page + 2, info.total_pages);
    for (let i = start; i <= end; i++) {
        btn = createPageBtn(i, i == info.current_page ? ['active'] : []);
        buttonsContainer.append(btn);
    }

    btn = createPageBtn(info.total_pages, ['last-page-btn']);
    btn.innerHTML = 'Последняя страница';
    if (info.current_page == info.total_pages) {
        btn.style.visibility = 'hidden';
    }
    paginationContainer.append(btn);
}

function downloadData(page = 1, query) {
    let factsList = document.querySelector('.facts-list');
    let url = new URL(factsList.dataset.url);
    let perPage = document.querySelector('.per-page-btn').value;
    url.searchParams.append('page', page);
    url.searchParams.append('per-page', perPage);
    query ? url.searchParams.set('q', query) : query;
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'json';
    xhr.onload = function () {
        renderRecords(this.response.records);
        setPaginationInfo(this.response['_pagination']);
        renderPaginationElement(this.response['_pagination']);
    };
    xhr.send();
}

function perPageBtnHandler() {
    const searchField = document.querySelector('.search-field');
    downloadData(1, query = searchField.value.trim());
}

function pageBtnHandler(event) {
    const searchField = document.querySelector('.search-field');
    if (event.target.dataset.page) {
        downloadData(event.target.dataset.page, 
            query = searchField.value.trim());
        window.scrollTo(0, 0);
    }
}


function searchRecords () {
    const searchField = document.querySelector('.search-field');
    searchField.value = searchField.value.trim();
    if (searchField.value === '') {
        query = '';
        return downloadData();    
    }
    downloadData(page = 1, query = searchField.value);
    console.log(query);
    window.scrollTo(0, 0);
}

function clearItems(event) {
    const list = document.getElementById('autocomplete');
    const field = document.querySelector('.search-field');
    if (event && event.target === field) return; 
    list.innerHTML = '';
}

function autocomplete(event, data) {
    const autocompleteList = document.getElementById('autocomplete');
    const value = event.target.value.trim();
    clearItems();
    if (value === '') return false; 
    for (const word of data) {
        const item = document.createElement("div");
        item.innerHTML = "<strong>" + word.substr(0, value.length)
         + "</strong>";
        item.innerHTML += word.substr(value.length);
        item.addEventListener("click", function(e) {
            event.target.value = word;
            clearItems(e);
        });
        autocompleteList.append(item);
    }
}

function getAutocompleteItems(event) {
    let query = event.target.value.trim();
    if (query === '') return;
    let url = new URL(
        'http://cat-facts-api.std-900.ist.mospolytech.ru/autocomplete'
    );
    url.searchParams.set('q', query);
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'json';
    xhr.onload = function () {
        autocomplete(event, this.response);
    };
    xhr.send();
}

window.onload = function () {
    downloadData();
    document.querySelector('.search-field')
        .addEventListener("input", getAutocompleteItems);

    document.onclick = addEventListener("click", function (event) {
        clearItems(event);
    });
    document.querySelector('.search-btn').onclick = searchRecords;
    document.querySelector('.pagination').onclick = pageBtnHandler;
    document.querySelector('.per-page-btn').onchange = perPageBtnHandler;
};

