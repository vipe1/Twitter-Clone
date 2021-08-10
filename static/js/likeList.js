$('.like-form').submit(function (e){
    e.preventDefault()
    const url = $(this).attr('action')
    const like_id = $(this).attr('id').substring(11)
    const button = $(`.like-btn-${like_id}`)
    const icon = $(`.like-icon-${like_id}`)
    const status = $(button).val()

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken':  $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            if(status === 'Like'){
                $(button).prop('value', 'Liked')
            } else {
                $(button).prop('value', 'Like')
            }
            $(button).toggleClass('btn-danger btn-outline-danger')
            $(icon).toggleClass('bi-heart bi-heart-fill')
            $(`.like-count-${like_id}`).text(`\u00A0\u00A0${response}`)
        },
        error: function (response) {
            console.log('error', response)
        }
    })
})