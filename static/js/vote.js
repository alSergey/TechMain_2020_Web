$('.js-vote').click(function (ev) {
    ev.preventDefault()
    var $this = $(this)
    vote = $this.data('action')
    id = $this.data('id')
    className = $this.data('class')

    map = {
        'like': 'dislike',
        'dislike': 'like'
    }

    if (document.getElementById(className + '-' + vote + '-' + id).classList.contains('vote')) {
        action = 'delete'
    } else if (document.getElementById(className + '-' + map[vote] + '-' + id).classList.contains('vote')) {
        action = 'update'
    } else {
        action = 'create'
    }

    // console.log('Class: ' + className + ' Id: ' + id + ' Action: ' + action + ' vote: ' + vote)

    document.getElementById(className + '-' + 'like' + '-' + id).classList.remove('vote')
    document.getElementById(className + '-' + 'dislike' + '-' + id).classList.remove('vote')

    $.ajax('/vote/', {
        method: 'POST',
        data: {
            class: className,
            id: id,
            action: action,
            vote: vote,
        },
    }).done(function (data) {
        document.getElementById(className + '-' + id).innerHTML = data['rating']
        if (action !== 'delete') {
            document.getElementById(className + '-' + vote + '-' + id).classList.add('vote')
        }
    })

});