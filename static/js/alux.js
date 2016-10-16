$(document).ready(function(){
	$("#login_error").css('display', 'none', 'important');
	$("#login").click(function(){
		var userInfo = {
			'username': $("#signin_username").val(),
			'password': $("#signin_password").val()
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
			success: function(){
				window.reload();
			},
			error: function(){
				$("#login_error").html("Username or password incorrect.");
				$("#form_signin").css('display', 'block');
			}
		});
		return false;
	});
});