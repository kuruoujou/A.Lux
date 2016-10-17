$(document).ready(function(){
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
						<input type=\"text\" id=\"playlist_name\" name=\"playlist_name\" class=\"form-control\" placeholder=\"" + $(this).text() + "\" required autofocus readonly>\
						<label for=\"title\">Playlist Title</label>\
						<input type=\"text\" id=\"title\" name=\"title\" class=\"form-control\" placeholder=\"Title\" autofocus>\
						<label for=\"artist\">Artist</label>\
						<input type=\"text\" id=\"artist\" name=\"artist\" class=\"form-control\" placeholder=\"Artist\" autofocus>\
						<label for=\"genre\">Genre</label>\
						<input type=\"text\" id=\"genre\" name=\"genre\" class=\"form-control\" placeholder=\"Genre\" autofocus>\
						<label for=\"image_url\">Image URL</label>\
						<input type=\"text\" id=\"image_url\" name=\"image_url\" class=\"form-control\" placeholder=\"Image URL\" autofocus>\
						<label for=\"thing_from\">Media From (TV Show, Movie, etc.)</label>\
						<input type=\"text\" id=\"thing_from\" name=\"thing_from\" class=\"form-control\" placeholder=\"Image URL\" autofocus>\
						<div class=\"checkbox\"><label><input type=\"checkbox\" id=\"background\" value=\"background\"> Background Sequence</label></div>\
						<div class=\"checkbox\"><label><input type=\"checkbox\" id=\"hidden\" value=\"hidden\"> Hidden Sequence</label></div>\
						<button id=\"addsong\" class=\"btn btn-lg btn-primary btn-block\" type=\"submit\">Add Song</button>\
					</form>")
	});
	
	//Add the song from the form
	$("#choices").on('click', '#addsong', function(){
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
		$.ajax({
			type: 'put',
			contentType: 'application/json',
			dataType: 'json',
			url: "/add",
			data: JSON.stringify(newSong),
			beforeSend: function(){
				$("#form-add").css('display', 'none');
				$("#choices").html("<img src='static/images/load.gif'>");
			},
			statusCode: {
				204: function(){
					location.reload();
				}
			}
		});
		display_add_modify_song_list();
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
					var output = "<div class=\"song col-md-12 add\"><a href=\"#\" class=\"addsong\">Add ".concat(element,"</a></div>");
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
					var output = "<div class=\"song col-md-12\"><a href=\"#\" class=\"modifysong\">Modify ".concat(element,"</a></div>");
					$("#choices").append(output)
				});
			}
		});
}