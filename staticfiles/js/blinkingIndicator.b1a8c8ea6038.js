const object = $('.scrollDown')

function blink () {
    $(object).delay(250).fadeTo(2000, 0.6).fadeTo(2000, 0, blink)
}

$(document).ready(function () {
    blink()
})