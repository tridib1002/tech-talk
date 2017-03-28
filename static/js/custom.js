$(document).ready(function(){
 	
	var counter = 0
	blogTemplateCreate(counter);
	blogTag = "all"
	userName = "none"

	function blogTemplateCreate(counter){
		for (var i=counter;i<(counter+3);i++){
	    var blogname= eval('blogData.blogname'+i);
	    var image= eval('blogData.image'+i);
	    var username = eval('blogData.username'+i);
	    var blogtag = eval('blogData.blogtag'+i);
	    var datestamp = eval('blogData.datestamp'+i);
	    var blog = eval('blogData.blog'+i);

	    // Checking if the blogdata is null or not.
	    if (typeof datestamp === "undefined"){ 
	    	$('#loadMore').hide(); // Hiding the load more button if there is no more Blog to show.
	    	break; // Braking the loop if data is undefined
	    }; 
	  	var blogTemplate = '<div class="row" id = "template'+i+'">  \
	                 <div class="col-md-12"> \
	                     <h1>'+blogname+'</h1> \
	                     <img onerror="this.src= \'static/images/favicon1_180x180.jpg\'" src="static/img/'+image+'" alt="your image" \
	                     name="aboutme" width="150" height="150" border="0" style="margin-right:20px;" \
	                     class="pull-left img-responsive thumb margin20 img-thumbnail"> \
	                     <div style="margin-bottom:15px;"> \
					        Blog By: <span class="badge">'+username+'</span><div class="pull-right"><span \
					        class="label label-info">'+blogtag+'</span></div> \
					    </div> \
					    <div> \
					    <span class="badge badge-success">Posted on: '+datestamp+'</span> \
					    </div> \
					    <div class="morelink"> \
	                     <article><p style="font-size : 115%"> \
	                         '+blog+' \
	                         </p></article> \
	                     </div> \
	               <div class="col-md-12 gap10"></div> \
	             </div>'
	    	$('#mainContainer').append(blogTemplate);
	    	}
		}

	$('.blogTag').click(function(e){

		$('#loadMore').show(); // Displaying the Load more button from hidden state.

		counter = 0;

		blogTag = $(this).text(); // fetching bloagTag when clicked on the Tag.

		userName = "none"; //  Setting useName to none

		$('#mainContainer').empty(); // clearing the blogs.

		loadMore(blogTag, userName); // chnaging blog tag value from 'all' to other blogtag.

		e.preventDefault(); // Preventing default action of click function on blogtag.

		});

	$('#homePage').click(function(e){

		$('#loadMore').show(); // Displaying the Load more button from hidden state.

		blogTag = "all"; // blogTag for home page is 'all' this value will be sent to server for fetching blogs.

		counter = 0; // Setting useName to none

		userName = "none"

		$('#mainContainer').empty(); // clearing the blogs.

		loadMore(blogTag, userName); // chnaging blog tag value from 'all' to other blogtag.

		e.preventDefault();
	});

	$('#userName').click(function(e){
  		
  		$('#loadMore').show(); // Displaying the Load more button from hidden state.

		blogTag = "all"; // blogTag for home page is 'all' this value will be sent to server for fetching blogs.

		counter = 0;

		$('#mainContainer').empty(); // clearing the blogs.
		  		
  		userName = $('#userName').text();

  		loadMore(blogTag, userName); // chnaging blog tag value from 'all' to other blogtag.

		e.preventDefault();
	});

	$('#loadMore').click(function(){
		counter = counter + 3; // Counter increment, as 3 blogs are fetched at a time.
		loadMore(blogTag,userName);
	});


	function loadMore(blogTag, userName){		
		fetchBlog(counter,blogTag,userName);
  	}

	function fetchBlog(counter,blogTag,userName){

  	$.ajax({

		data :{ 
			userName : userName,
			val : counter,
			blogtag : blogTag
		}, // sending the value of counter and blogtag to the server

		type: 'POST',
		url : '/fetchBlog' // check '/fetchBlog' section of '__init__.py' file for server side functions.

	})

    .done(function(data){ // This function will execute after the AJAX request.

      	blogData = data // replacing blogData value to the new value

      	blogTemplateCreate(counter); // Calling the blogTemplateCreate function for new blogs.

    	});
 	
  	};

  	$('#loginForm').submit(function(e){

		e.preventDefault();

		console.log('Working');

		loginUser = $('#username').val();
		loginPass = $('#password').val();


		$.ajax({

		data :{ 
			username : loginUser,
			password : loginPass
		}, // sending the value of counter and blogtag to the server

		type: 'POST',
		url : '/LogIn' // check '/fetchBlog' section of '__init__.py' file for server side functions.

	})

    .done(function(data){ // This function will execute after the AJAX request.

      	if (data == "notFound"){
			$('#loginWarning').show();	
      		}
      	else{
      		location.reload();
      	}

    	});

	});

  	$('#userNameSignUp').keyup(function(e){
  		var newUser = e.target.value;
  		$.ajax({

  			data:{
  				newUser : newUser
  			},
  			type: 'POST',
  			url: '/checkUser'
  		}).done(function(data){

  			if (data == 'exists'){	
  			$('#userNameavAilability').show();
  			$('#signupButton').prop('disabled', true);
  			}
  			else{
  			$('#userNameavAilability').hide();
  			$('#signupButton').prop('disabled', false);
  			}

  		});

  		// console.log(e.target.value);
  	});


});
