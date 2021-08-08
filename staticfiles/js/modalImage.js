const modal = $('.modal')
const imgs = $('.tweet-image')
const modalImage = $('.modalImage')
const modalClose = $('.modalClose')

imgs.click(function (e) {
    const image = e.target
    const source = image.getAttribute('src')

    $(modalImage).attr('src', source)

    $(modal).addClass('open')
    $(modalImage).addClass('open')
})

$(modal).click(function (e) {
    if (!e.target.classList.contains('modalImage')) {
        $(modal).removeClass('open')
        $(modalImage).removeClass('open')
    }
})

$(modalClose).click(function (e) {
    $(modal).removeClass('open')
    $(modalImage).removeClass('open')
})