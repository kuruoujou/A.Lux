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
					var output = "<div class=\"song col-md-12 add\"><a href=\"#\" class=\"addsong\">".concat(element,"</a></div>");
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
					var output = "<div class=\"song col-md-12\"><a href=\"#\" class=\"modifysong\" id=\"playlist-".concat(element.id, "\">", element.playlist,"</a></div>");
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
				var output = "<div class=\"song col-md-12\"><a href=\"#\" class=\"playsong\">".concat(element.title, "</a></div>");
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
	console.log("Not yet implemented.");
}
