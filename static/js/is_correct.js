$('.js-correct').click(function(ev) {
    let $this = $(this),
        id = $this.data('id');
    $.ajax('/correct/', {
        method: 'POST',
        data: {
            id: id,
        },
    }).done(function(data) {
        $('#correct-' + id).prop('checked', data.action);
        if (data.action) {
            $('#correct-' + id).next('.form-check-label').css('color', '#28a745');
        } else {
            $('#correct-' + id).next('.form-check-label').css('color', '');
        }
    });
    console.log("Correct is " + id);
});