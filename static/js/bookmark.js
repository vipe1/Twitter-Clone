$('.bookmark-form').submit(function (e){
    e.preventDefault()
    const url = $(this).attr('action')
    const like_id = $(this).attr('id').substring(15)
    const submit = $(`#tweet-bookmark-submit-${like_id}`)
    const status = $(submit).text()

    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'csrfmiddlewaretoken':  $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            if(status.trim() === 'Save'){
                $(submit).text('Unsave')
            } else {
                $(submit).text('Save')
            }
        },
        error: function (response) {
            console.log('error', response)
        }
    })
})