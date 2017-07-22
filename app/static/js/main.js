$(document).ready(function() {
    $('.playlist-song-action').click(function () {
        var songId = $(this).parents('.playlist-song-container').data('id');
        var status = $(this).data('status');

        $.ajax({
            url: window.endpoint + '/songs/' + songId + '/status',
            type: 'PUT',
            crossDomain: true,
            headers: {
                'Content-type': 'application/json;charset=utf-8',
		    },
            data: JSON.stringify({'status': status })
        }).done(function(response){
            console.log(response);
        }).fail(function(response){
            console.log(response);
        });
    });

});