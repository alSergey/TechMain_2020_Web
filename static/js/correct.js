$('.js-correct').click(function (ev) {
    ev.preventDefault()
    var $this = $(this)
    id = $this.data('id')

    checked = !!document.getElementById('answer-correct' + '-' + id).checked;

    $.ajax('/correct/', {
        method: 'POST',
        data: {
            id: id,
            checked: checked
        },
    }).done(function (data) {
        document.getElementById('answer-correct' + '-' + id).checked = data['correct']
    });
})