// Поиск
// Скрытие кнопки и появление формы поиска с курсором в поле ввода
$(".action-search-btn").on('click', function (event) {
    event.preventDefault();
    $(this).hide();
    $(this).next(".input-field").fadeToggle();
    document.getElementsByName('search')[0].focus();
});

// Если был клик вне формы поиска, форма скрывается
$(document).mouseup(function (event) {
    const actionSearchButton = $(".action-search-btn");
    const searchInputField = actionSearchButton.next(".input-field");
    if (searchInputField.has(event.target).length === 0) {
        searchInputField.hide();
        actionSearchButton.show(300);
    }
});

// Комментарии
// Появление ответов и формы для ответа
$(".reply-action-link").on('click', function (event) {
    event.preventDefault();
    $(this).parent().parent().next(".reply-block").fadeToggle();
});