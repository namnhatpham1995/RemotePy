// Auto Refresh page function
        function AutoRefresh( t ) {
               setTimeout("location.reload();", t);
            }

        // Setup to the clear choose file before upload
        $("#clear").on("click", function()
        {
            $("#upload_file").replaceWith( $("#upload_file").val('').clone( true ) );
        });


        function clearTextArea() {
            document.getElementById("typeText").value = "";
        }

		function get_xy(event, offset){
			// function to get position of event on image
			if(event.pageX == null){
				// for mobile
				var x = event.x - offset.left
				var y = event.y - offset.top;
			}
			else{
				// for pc
				var x = event.pageX - offset.left
				var y = event.pageY - offset.top;

			}

			return [x,y];
		}


		function mouse_event(screen, event, type) {
			var offset = screen.offset();
			var point = get_xy(event, offset);
			console.log(type);

			$.ajax({
				type: 'POST',
				url: "/mouse",
				data: {
						"type": type,
						"x": point[0],
						"y": point[1],
						"X": screen.width(),
						"Y": screen.height()
					},
                timeout: 3000,
				success: function(result) { }
			});
		}
        // Keyboard event for click button on mobile
		function keyboard_event(type) {
			console.log(type);

			$.ajax({
				type: 'POST',
				url: "/button",
				data: {
				        "type": "text",
						"type": type
					},
				success: function(result) { }
			});
		}


		$(document).ready(function() {

			$.Finger.doubleTapInterval = 2000;
			document.oncontextmenu = function() {return false;};

			<!--mouse action jquery -->
			/*$('#screen').on('doubletap dblclick', function(event) {
				var screen = $(this);
				mouse_event(screen, event, "dblclick");
			});*/
            // Button on mobile screen click
			$('.keyboard').click(function(event) {
				keyboard_event(this.id);
			});

            var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            if (isMobile) {
                  $('#screen').on("tap", function tapHandler(event) {
                    var screen = $(this);
                    mouse_event(screen, event, "click");
                    });

                  $('#button').on('keyup', function(event){
                        if(event.keyCode == 13){
                            $('#enter').click();
                        }else if(event.keyCode == 8){
                            $('#backspace').click();
                        }else if(event.keyCode == 38) {
                            $('#up').click();
                        }else if(event.keyCode == 40){
                            $('#down').click();
                        }else if(event.keyCode == 37){
                            $('#left').click();
                        }else if(event.keyCode == 39){
                            $('#right').click();
                        }
			        });

            }
            else {
                <!--Remove Click and Double Click, Add mouse press and mouse release-->
                $('#screen').on('mousedown', function(event) {
                    event.preventDefault();
                    var screen = $(this);
                    mouse_event(screen, event, "mousepress");

                    <!--Add check mouse position (for drag action) -->
                    $('#screen').on('mousemove', function(event) {
                        event.preventDefault();
                        var screen = $(this);
                        mouse_event(screen, event, "mousemove");
                    });

                });
                $('#screen').on('mouseup', function(event) {
                    event.preventDefault();
                    var screen = $(this);
                    mouse_event(screen, event, "mouserelease");
                    $('#screen').off('mousemove');
                });
            }



			$('#screen').on('taphold contextmenu', function(event) {
				event.preventDefault();
				var screen = $(this);
				mouse_event(screen, event, "rightclick");
			});
            <!--Add mousescroll up and down -->
			$('#screen').on('mousewheel', function(event) {
				event.preventDefault();
				var screen = $(this);
                if(event.originalEvent.wheelDelta > 0) {
                    mouse_event(screen, event, "mousewheelup");
                }
                else{
                    mouse_event(screen, event, "mousewheeldown");
                }

			});
            //<!--Add check mouse position (for drag action) -->
            //$('#screen').on('mousemove', function(event) {
			//	event.preventDefault();
			//	var screen = $(this);
			//	mouse_event(screen, event, "mousemove");
			//	setTimeout(this,100);
			//});

            /* Send text keyboard, click on empty space to activate keyboard oneye */

			$('html').keydown(function(event) {
                var text    = event.key.toLowerCase();
                if (text == "arrowdown")
                {
                    text = "down";
                }
                else if (text == "arrowup")
                {
                    text = "up";
                }
                else if (text == "arrowleft")
                {
                    text = "left";
                }
                else if(text == "arrowright")
                {
                    text = "right";
                }
                else if(text == "control")
                {
                    text = "ctrl";
                }
				console.log(text);
				$.ajax({
					type: 'POST',
					url: "/keyboard",
					data: {
					        "type": "keyboard",
							"text": text
						},

					success: function(result) { }
				});
			});


            /* Send text area*/
			$('#text').click(function(event) {
				var text = document.getElementById('typeText').value;
				console.log(text);
				$.ajax({
					type: 'POST',
					url: "/button",
					data: {
							"type": "text",
							"text": text
						},
					success: function(result) { }
				});
				document.getElementById("typeText").value = "";
			});

			$('#upload_button').click(function(event) {
			    var fd = new FormData();
			    var files = $('#upload_file')[0].files;
				if(files.length > 0 ){
                   fd.append('file',files[0]);
                   $.ajax({
                      url: '/upload_file/',
                      type: 'post',
                      data: fd,
                      contentType: false,
                      processData: false,
                      //success: function(response){}
                       error: function (data) {
                            layer.msg('upload failed', {
                                icon: 2,
                                time: 1000 // 1 second off (if not configured, the default is 3 seconds)
                            });
                        },

                       success: function (data)
                       {
                            if (data.code == 1) {
                                layer.msg('Uploaded successfully', {
                                    icon: 1,
                                    time: 1000 // 1 second off (if not configured, the default is 3 seconds)
                                }, function () {
                                    parent.location.reload();
                                });
                            }
                            else {
                                layer.msg(data.msg, {
                                    icon: 2,
                                    time: 1000 // 1 second off (if not configured, the default is 3 seconds)
                                });
                            }
                        },
                       xhr: function () {
                            myXhr = $.ajaxSettings.xhr();
                            if (myXhr.upload) { // check upload property exists
                                // Bind event callback progress
                                myXhr.upload.addEventListener('progress', progressHandlingFunction, false);
                            }
                            return myXhr; // xhr object back to using jQuery
                        }

                   });

                }
			});
            function progressHandlingFunction(event) {
                var loaded = Math.floor(100 * (event.loaded / event.total)); // percentage has been uploaded
                $("#progress-bar").html(loaded + "%").css("width", loaded + "%");
            }

		});