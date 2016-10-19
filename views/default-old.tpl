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

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>

  <body>

    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="#">A.Lux</a>
        </div>
        </div><!--/.nav-collapse -->
      </div>
    </nav>
    <div class="container-fluid">
      <section class="description" id="description">
          %if error:
          <h1>{{error}}</h1>
          %end
          %if not playing and playable:
          <h1>Tune your radio to {{radioStation}}, select a song below, and enjoy!</h1>
          %elif not playable:
          <h1>The show is only playable between roughly sundown and midnight, sorry about that! Thanks for stopping by!</h1>
          %else:
          <h1>Currently playing {{playlistName}}, about {{timeRemaining}} seconds left.</h1>
          %end
      </section>
      %if not playing and playable:
      <section class="choices" id="choices">
        %iteration=0
        %for playlist in playlists:
      	<div class="row">
                %if iteration==0:
		<div class="song top col-md-12">
                %iteration=1
                %else:
                <div class="song col-md-12">
                %end
			<a href="/play?song={{playlist['title']}}">{{playlist['displayTitle']}}</a>
		</div>
	</div>
        %end
      </section>
      %elif playable:
      <section class="stop" id="stop">
        <div class="row">
              <div class="song top col-md-12">
                  <a href="/stop">Tap to stop the currently playing song.</a>
              </div>
        </div> 
      </section>
      %end
      %if playable:
      <section class="description" id="problems">
	  <small>Buttons don't work? Light display look broken or frozen? Let me know: <a href="mailto:helloThere+kld@spencerjulian.com">helloThere+kld@spencerjulian.com</a></small>
      </section>
      %end
    </div><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="static/js/bootstrap.min.js"></script>
  </body>
</html>

