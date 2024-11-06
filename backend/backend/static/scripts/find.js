function executeSearchQuery() {
    const query = document.querySelector('.find-input').value.trim();

    if (query) {
        window.location.href = `/main?find=${encodeURIComponent(query)}`;
    } else {
        alert('Введите запрос для поиска.');
    }
}

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Получаем значение параметра "find"
const searchQuery = getQueryParam('find');
const headerNameElement = document.querySelector('.main__header-name');
const errorMessageElement = document.getElementById('error-message');

if (searchQuery) {
    headerNameElement.textContent = searchQuery;
} else {
    errorMessageElement.style.display = 'block';
    errorMessageElement.textContent = 'Запрос не найден.';
}