
$('.playlist-song-actions').delegate('.playlist-song-action','click', function () {
    var $row = $(this).parents('.playlist-song-container');
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
        if (status == 'normal'){
            $row.find('.playlist-song-actions').html(
                "<div class='flex-row'>" +
                "<div class='playlist-song-action' data-status='liked'> " +
                "<i class='fa fa-heart-o'></i> </div> " +
                "<div class='playlist-song-action' data-status='removed'>" +
                " <i class='fa fa-trash-o'></i> </div></div>"
            )
        }
        var $totalSongs = $("#numberOfSongs");
        if (status == 'removed') {
            $row.fadeOut();
            $totalSongs.text(parseInt($totalSongs.text()) - 1);

            if ($(".playlist-song-container ").filter(":visible").size() == 2) {
                $("#filterSongs").val('');
                $("#filterSongs").trigger('keyup');
            }
        }

        if (status == 'liked') {
             $row.find('.playlist-song-actions').html("<div class='playlist-song-action single-action' " +
                 "data-status='normal'>" +
                 " <i class='fa fa-heart'></i> </div>"
            );

            var $likedSongs = $("#likedSongs");
            $likedSongs.text(parseInt($likedSongs.text()) +1);

            $totalSongs.text(parseInt($totalSongs.text()) - 1);
        }
        console.log(response);
    }).fail(function(response){
        console.log(response);
    });
});

$( "#filterSongs" ).on('keyup', function () {
    var i;
    var $filter = $('#filterSongs').val().toUpperCase();
    var $songs = $(".playlist-songs").find('.playlist-song-container ');
    var numberOfSongs = $songs.size();

    for (i = 0; i < $songs.length; i++) {
        var song = $songs.eq(i).find('.playlist-song-artist');
        var artist = $songs.eq(i).find('.playlist-song-title');
        if (song.text().toUpperCase().indexOf($filter) > -1 || artist.text().toUpperCase().indexOf($filter) > -1) {
            $songs[i].style.display = "";
        } else {
            $songs[i].style.display = "none";
        }
    }

    if ($(".playlist-song-container ").filter(":hidden").size() >= numberOfSongs) {
        $(".playlist-label").hide();
        $(".playlist-empty-state").show();
    }
    else {
        $(".playlist-label").show();
        $(".playlist-empty-state").hide();
    }
});