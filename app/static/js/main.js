$(document).ready(function() {
    $('.playlist-song-action').click(function () {
        var $row = $(this).parents('.playlist-song-container')
        var songId = $row.data('id');
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
            $row.fadeOut();
        }).fail(function(response){
            console.log(response);
        });
    });

});