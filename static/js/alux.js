$(document).ready(function(){
	// Display the main page as soon as we load.
    if(playcheck == "True"){
		display_main_page();
	} else if(playcheck == "False"){
		$.ajax({
			type: 'get',
			contentType: 'application/json',
			dataType: 'json',
			url: "/status",
			success: function(data){
					if(data['playing'] == false && authenticated == false){
						display_out_of_bounds_page();
					} else if (authenticated == true){
                        display_main_page();
                    } else {
						display_media_page();
					}
			}
		});
	}
	
	// Log In Form
	$("#login").click(function(){
		var userInfo = {
			'username': $("#signin_username").val(),
			'password': $("#signin_password").val(),
			'alux_id': $.cookie("alux_id"),
			'expiration': $.cookie("alux_expiration")
		};
		$.ajax({
			type: 'post',
			contentType: 'application/json',
			dataType: 'json',
			url: "/authenticate",
			data: JSON.stringify(userInfo),
			beforeSend: function(){
				$("#form_signin").css('display', 'none');
				$("#login_error").css('display', 'block', 'important');
				$("#login_error").html("<img src='static/images/load.gif'>");
			},
			statusCode: {
				205: function(){
					location.reload();
				},
				401: function(){
					$("#login_error").html("Username or password incorrect.");
					$("#form_signin").css('display', 'block');
				}
			}
		});
		return false;
	});
	
	//Display the Add Songs dialog
	$("#add_songs_btn").click(function(){
		$("#navbar").collapse('hide');
		display_add_modify_song_list();
	});
	
	//Display the Add/Modify song form
	$("#choices").on('click', '.addsong', function(){
		$("#choices").empty();
		$("#description").empty();
		$("#description").html("<h1>Adding ".concat($(this).text(), " to the A.Lux database"))
		$("#choices").html("<form accept-charset=\"UTF-8\" class=\"form-add\" id=\"form-add\">\
						<label for=\"playlist_name\">Playlist Name</label>\
						<input type=\"text\" id=\"playlist_name\" name=\"playlist_name\" class=\"form-control\" value=\"" + $(this).text() + "\" required autofocus readonly>\
						<label for=\"title\">Playlist Title</label>\
						<input type=\"text\" id=\"title\" name=\"title\" class=\"form-control\" placeholder=\"Title\" autofocus>\
						<label for=\"artist\">Artist</label>\
						<input type=\"text\" id=\"artist\" name=\"artist\" class=\"form-control\" placeholder=\"Artist\" autofocus>\
						<label for=\"genre\">Genre</label>\
						<input type=\"text\" id=\"genre\" name=\"genre\" class=\"form-control\" placeholder=\"Genre\" autofocus>\
						<label for=\"image_url\">Image URL</label>\
						<input type=\"text\" id=\"image_url\" name=\"image_url\" class=\"form-control\" placeholder=\"Image URL\" autofocus>\
						<label for=\"thing_from\">Media From (TV Show, Movie, etc.)</label>\
						<input type=\"text\" id=\"thing_from\" name=\"thing_from\" class=\"form-control\" placeholder=\"Media From\" autofocus>\
						<div class=\"checkbox\"><label><input type=\"checkbox\" id=\"background\" value=\"background\"> Background Sequence</label></div>\
						<div class=\"checkbox\"><label><input type=\"checkbox\" id=\"hidden\" value=\"hidden\"> Hidden Sequence</label></div>\
						<button id=\"addsong\" class=\"btn btn-lg btn-primary btn-block\" type=\"submit\">Add Song</button>\
					</form>")
	});
	
	$("#choices").on('click', '.modifysong', function(){
		$("#choices").empty();
		$("#description").empty();
		var ajax_url = "/get/".concat(this.id.split("-")[1], "?alux_id=", $.cookie("alux_id"))
		console.log(ajax_url)
		$.ajax({
			type: 'get',
			contentType: 'application/json',
			dataType: 'json',
			url: ajax_url,
			beforeSend: function(){
				$("#choices").html("<img src='static/images/load.gif'>");
			},
			success: function(data){
				$("#choices").empty();
				$("#description").html("<h1>Modifying ".concat(data.playlist, " in the A.Lux database"))
				$("#choices").html("<form accept-charset=\"UTF-8\" class=\"form-add\" id=\"form-add\">\
						<label for=\"playlist_name\">Playlist Name</label>\
						<input type=\"text\" id=\"playlist_name\" name=\"playlist_name\" class=\"form-control\" value=\"" + data.playlist + "\" required autofocus readonly>\
						<label for=\"title\">Playlist Title</label>\
						<input type=\"text\" id=\"title\" name=\"title\" class=\"form-control\" placeholder=\"Title\" autofocus value=\"" + data.title + "\">\
						<label for=\"artist\">Artist</label>\
						<input type=\"text\" id=\"artist\" name=\"artist\" class=\"form-control\" placeholder=\"Artist\" autofocus value=\"" + data.artist + "\">\
						<label for=\"genre\">Genre</label>\
						<input type=\"text\" id=\"genre\" name=\"genre\" class=\"form-control\" placeholder=\"Genre\" autofocus value=\"" + data.genre + "\">\
						<label for=\"image_url\">Image URL (changing this will re-download)</label>\
						<input type=\"text\" id=\"image_url\" name=\"image_url\" class=\"form-control\" placeholder=\"Image URL\" autofocus value=\"" + data.image_url + "\">\
						<label for=\"thing_from\">Media From (TV Show, Movie, etc.)</label>\
						<input type=\"text\" id=\"thing_from\" name=\"thing_from\" class=\"form-control\" placeholder=\"Media From\" autofocus value=\"" + data.thing_from + "\">\
						<div class=\"checkbox\"><label><input type=\"checkbox\" id=\"background\" value=\"background\"> Background Sequence</label></div>\
						<div class=\"checkbox\"><label><input type=\"checkbox\" id=\"hidden\" value=\"hidden\"> Hidden Sequence</label></div>\
						<input type=\"hidden\" id=\"playlist_id\" name=\"playlist_id\" value=\"" + data.id + "\">\
						<button id=\"modifysong\" class=\"btn btn-lg btn-primary btn-block\" type=\"submit\">Add Song</button>\
					</form>")
				if (data.hidden != 0) {
					$("#hidden").prop("checked", true)
				}
				if (data.background != 0){
					$("#background").prop("checked", true)
				}
			}
		});
		
	});

    //Play a song when pressed, and if possible.
    $("#choices").on('click', '.playsong', function(){
        $("#choices").empty();
        $("#description").empty();
        var toPlay = {
            "id": this.id.split("-")[1],
        };
        if($(this).hasClass("repeat")){
            toPlay.repeat = true;
        } else {
            toPlay.repeat = false;
        }
        $.ajax({
            type: 'put',
            contentType: 'application/json',
            dataType: 'json',
            url: '/play?alux_id='.concat($.cookie("alux_id")),
			data: JSON.stringify(toPlay),
            beforeSend: function(){                                              
                $("#choices").html("<img src='static/images/load.gif'>");    
            },                                                                   
            statusCode: {                                                        
                205: function(){
					$("#choices").empty();
                    if (toPlay.repeat) {
                        display_main_page();
                    } else {
                        display_media_page();
                    }
                },                                                               
                404: function(){
                    $("#choices").empty();
                    $("#description").html("That playlist doesn't exist! If you got here through a link, email <a href=\"mailto:helloThere+kld@spencerjulian.com\">helloThere+kld@spencerjulian.com</a> to let me know.");
                },
                409: function(){
                    if(playcheck == "True"){
                        display_media_page();
                    } else {
                        display_out_of_bounds_page();
                    }
                }
            }
        });
    });
	
	$("#choices").on('click', '#stopsong', function(){
        $("#choices").empty();
        $("#description").empty();
        $.ajax({
            type: 'delete',
            contentType: 'application/json',
            dataType: 'json',
            url: '/stop?alux_id='.concat($.cookie("alux_id")),
            beforeSend: function(){                                              
                $("#choices").html("<img src='static/images/load.gif'>");    
            },                                                                   
            statusCode: {                                                        
                205: function(){
					$("#choices").empty();
                    display_main_page();
                }
            }
        });
    });
	
	//Add the song from the form
	$("#choices").on('click', '#addsong', function(){
		make_add_modify_request('add')
		return false;
	});
	
	//Modify the song from the form
		//Add the song from the form
	$("#choices").on('click', '#modifysong', function(){
		make_add_modify_request('modify')
		return false;
	});
});

function display_add_modify_song_list(){
		$("#description").html("<h1>Select songs to Add or Modify</h1>");
		$.ajax({
			type: 'get',
			contentType: 'application/json',
			dataType: 'json',
			url: "/listnew?alux_id=".concat($.cookie("alux_id")),
			success: function(data){
				$("#choices").empty();
				$.each(data.playlists, function(index, element){
					var output = "<div class=\"song col-md-12 add\"><a href=\"#\" class=\"addsong\"><span class=\"title\">".concat(element,"</span></a></div>");
					$("#choices").append(output)
				});
			}
		});
		$.ajax({
			type: 'get',
			contentType: 'application/json',
			dataType: 'json',
			url: "/get?alux_id=".concat($.cookie("alux_id")),
			success: function(data){
				$.each(data.playlists, function(index, element){
					var output = "<div class=\"song col-md-12\"><a href=\"#\" class=\"modifysong\" id=\"playlist-".concat(element.id, "\"><span class=\"title\">", element.playlist,"</span></a></div>");
					$("#choices").append(output)
				});
			}
		});
}

function make_add_modify_request(call_url){
		var newSong = {
			'playlist': $("#playlist_name").val(),
			'title': $("#title").val(),
			'artist': $("#artist").val(),
			'genre': $("#genre").val(),
			'image_url': $("#image_url").val(),
			'thing_from': $("#thing_from").val(),
			'background': $("#background").prop('checked'),
			'hidden': $("#hidden").prop('checked')
		}
		if ( $("#playlist_id").length ) {
			newSong.id = $("#playlist_id").val()
		}
		$.ajax({
			type: 'put',
			contentType: 'application/json',
			dataType: 'json',
			url: "/".concat(call_url, "?alux_id=", $.cookie("alux_id")),
			data: JSON.stringify(newSong),
			beforeSend: function(){
				$("#form-add").css('display', 'none');
				$("#choices").html("<img src='static/images/load.gif'>");
			},
			statusCode: {
				204: function(){
					display_add_modify_song_list();
				},
				201: function(){
					display_add_modify_song_list();
				}
			}
		});
}

function display_main_page(){
	$("#description").html("<h1>Tune your radio to ".concat(radioStation, ", select a song below, and enjoy!</h1>"));
	$.ajax({
		type: 'get',
		contentType: 'application/json',
		dataType: 'json',
		url: "/get?alux_id=".concat($.cookie("alux_id")),
		success: function(data){
			$.each(data.playlists, function(index, element){
                var output;
				var title = "<span class=\"title\">".concat(element.title, "</span>");
				var repeat = element.background == 1 ? "repeat" : "";
				var artist = element.artist == "" ? "" : "<br><span class=\"artist\">".concat(element.artist, "</span>");
				var thing_from = element.thing_from == "" ? "" : "<br><span class=\"thing_from\">From ".concat(element.thing_from, "</span>");
				var padding = element.thing_from == "" ? "<br><span class=\"thing_from\">&nbsp;</span>" : ""
				output = "<div class=\"song col-md-12\"><a href=\"#\" class=\"playsong ".concat(
					repeat,
					"\" id=\"playlist-",
					element.id,
					"\">",
					title,
					artist,
					thing_from,
					padding,
					"</a></div>"
				);
				$("#choices").append(output)
			});
		}
	});
}

function display_out_of_bounds_page(){
	$("#description").html("<h1>The show can only be played between sundown and midnight.</h1> <p>Sorry about that! Thanks for stopping by, come by tomorrow to see it, or send me an email at <a href=\"mailto:helloThere+kld@spencerjulian.com\">helloThere+kld@spencerjulian.com</a> if there's something wrong!");
	$("#choices").empty();
}

function display_media_page(){
    var since_start, total_time, percent_remaining;
    $.ajax({
        type: 'get',
        contentType: 'application/json',
        dataType: 'json',
        url: "/status?alux_id=".concat($.cookie("alux_id")),
        beforeSend: function(){
            $("#choices").html("<img src='static/images/load.gif'>");
        },
        success: function(element){
            var title = "<h1 class=\"title\">".concat(element.title, "</h1>");
            var artist = element.artist == "" ? "" : "<h2 class=\"artist\">".concat(element.artist, "</h2>");
            var thing_from = element.thing_from == "" ? "" : "<h3 class=\"thing_from\">From ".concat(element.thing_from, "</h3>");
            var art = element.image_url == "" ? "" : "<div class=\"art\"><img src=\"".concat(element.image_url, "\" class=\"album-art\"></div>");
            since_start = element.time_since_start;
            total_time = element.time_since_start + element.time_remaining;
            percent_remaining = Math.floor((element.time_since_start / element.time_remaining) * 100 );
            $("#description").html(title.concat(
                        artist,
                        thing_from
                        ));
            $("#choices").html(art.concat(
                        "<div class=\"pbar\"><span class=\"time_since_start\">",
                        sformat(since_start),
                        "</span><div class=\"progress\"><div class=\"progress-bar\" role=\"progressbar\" style=\"width: ",
                        percent_remaining,
                        "%\"></div></div><span class=\"total\">",
                        sformat(total_time),
                        "</span></div><div class=\"stopsong\" id=\"stopsong\">Stop this song</div>"
                        ));
        }
    });
    var interval = setInterval( function() {
        since_start = since_start+1;
        if (since_start == total_time || since_start % 5 == 0){
            $.ajax({
                type: 'get',
                contentType: 'application/json',
                dataType: 'json',
                url: "/status?alux_id=".concat($.cookie("alux_id")),
                success: function(element){
                   if(element.playing == true ){
                       since_start = element.time_since_start;
                       total_time = element.time_since_start + element.time_remaining;
                   } else {
					   $("#choices").empty();
                       clearInterval(interval);
                       display_main_page();
                   }
                }
            });
        }
        percent_remaining = Math.floor((since_start / total_time) * 100 );
        $(".progress-bar").width(percent_remaining + "%");
        $(".time_since_start").html(sformat(since_start));
    }, 1000);
}

// Found at https://forum.jquery.com/topic/converting-seconds-to-dd-hh-mm-ss-format
// by kbwood.au
function sformat(s) {
    var fm = [
        Math.floor(s / 60) % 60, // MINUTES
        s % 60 // SECONDS
    ];
return $.map(fm, function(v, i) { return ((v < 10) ? '0' : '') + v; }).join(':');
}
