<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="../../favicon.ico">

    <title>A.Lux</title>

    <!-- Bootstrap core CSS -->
    <link href="static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="static/css/base.css" rel="stylesheet">
	<link href="static/css/signin.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
	
	<script type="text/javascript">
		var radioStation = "{{radioStation}}";
		var playcheck = "{{playcheck}}";
	</script>
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">A.Lux</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <div class="col-xs-12">
            <ul class="nav navbar-nav">
              <li class="dropdown">
                  %if not userInfo['username']:
					<div class="err" id="login_error"></div>
					<form accept-charset="UTF-8" class="form-signin" id="form_signin">
						<label for="signin_username" class="sr-only">Username</label>
						<input type="text" id="signin_username" name="signin_username" class="form-control" placeholder="Username" required autofocus>
						<label for="signin_password" class="sr-only">Password</label>
						<input type="password" id="signin_password" name="signin_password" class="form-control" placeholder="Password" required>
						<button id="login" class="btn btn-lg btn-primary btn-block" type="submit">Log In</button>
					</form>
                  %else:
                     <ul class="nav lvl2">
                        <li><a href="#" id="add_songs_btn">Add/Modify Songs</a></li>
                        <li><a href="#">Config Options</a></li>
						<li><a href="#">Edit {{userInfo['username']}}'s Account</a></li>
                        <li><a href="/logout">Log Out</a></li>
                     </ul>
                  %end
              </li>
            </ul>
          </div>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
	
	
    <div class="container-fluid">
		<section class="description" id="description">
		</section>
		<section class="choices" id="choices">
		</section>
		<section class="description" id="problems">
			<small>Buttons don't work? Light display look broken or frozen? Let me know: <a href="mailto:helloThere+kld@spencerjulian.com">helloThere+kld@spencerjulian.com</a></small>
		</section>
    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
	<script src="static/js/alux.js"></script>
  </body>
</html>

