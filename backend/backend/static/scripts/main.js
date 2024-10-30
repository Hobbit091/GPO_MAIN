function switchLanguage(language) {
    document.getElementById('ru').classList.remove('active');
    document.getElementById('en').classList.remove('active');
    document.getElementById(language).classList.add('active');
}
