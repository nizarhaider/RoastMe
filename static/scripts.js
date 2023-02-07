
      document.getElementById("submit-button").addEventListener("click", haltFunction);

    
      var headerFinished = false;
      var head_text = "pip install roastbot...";
      var a = 0;
      var header = $("#comments-header h3");
      var interval = setInterval(function() {
        $('.blinking-cursor').remove();
        header.append(head_text[a]);
        header.append("<span class='blinking-cursor'>' '</span>");
        a++;
        if (a >= head_text.length) {
          $('.blinking-cursor').remove();
          clearInterval(interval);
          startCommentPrinting();
        }
      }, 100);

      let typing = false;

      function haltFunction() {
          clearInterval(promptInterval);
          clearInterval(interval);
          clearTimeout(timeout)
          $("#comments-list").text("");
          if(typing) {
            clearTimeout(typing_time);
            typing = false;
          }
          if (isPrinting) {
            clearInterval(promptInterval);
            isPrinting = false;
        }
      }

      var isPrinting = false;

      function startCommentPrinting() {
      isPrinting = true;
      var commentsList = $("#comments-list");
      var prompts = ["Waiting for image upload...", "Too scared to upload?", "Don't worry, I'll be nice. I promise..."];
      var currentPrompt = 0;
      var b = 0;
      function startPrinting() {
        if (b === 0) {
          commentsList.text("");
        }
        $('.blinking-cursor').remove();
        commentsList.append(prompts[currentPrompt][b]);
        commentsList.append("<span class='blinking-cursor'>| |</span>");
        b++;
        if (b >= prompts[currentPrompt].length) {
          clearInterval(promptInterval);
          currentPrompt++;
          b = 0;
          if (currentPrompt >= prompts.length) {
              currentPrompt = 0;
          }
          timeout = setTimeout(() => {
            promptInterval = setInterval(startPrinting, 100);
          }, 4000);
        }
      }
      promptInterval = setInterval(startPrinting, 100);
  }

      $("form").submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $("#comments-list").text("");
        $.ajax({
            url: '/',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data) {  
              console.log(data.fun_pass)
              if (data.fun_pass == "True") {
                document.getElementById("comments-list").scrollIntoView();  
                var comments = data.comments;
                comments = JSON.parse(comments);
                comments = comments.map(comment => comment.replace("[", "").replace("]", "").replace("\u2019", "'"));
                $("#comments-list").append("<br>"); 

                function typeComment(i, j) {  
                  typing = true;
                  if (i < comments.length) {
                    if (j < comments[i].length) {
                      $('.blinking-cursor').remove();
                      $("#comments-list").append(comments[i][j]);
                      $("#comments-list").append("<span class='blinking-cursor'>' '</span>");
                      var delay = Math.floor(Math.random() * 75) + 25;
                      document.querySelector('.blinking-cursor').style.animationDelay = delay + 'ms';
                      setTimeout(function () {
                        typeComment(i, j + 1);
                      }, delay);
                    } else {
                      $("#comments-list").append("<br>").append("<br>");
                      typing_time = setTimeout(function () {
                        typeComment(i + 1, 0);
                      }, 500);
                    }
                  }
                  typing = false;
                }
                setTimeout(function(){
                  document.getElementById("comments-list").scrollIntoView();  
                  typeComment(0, 0);
                },1000)
                $('frame').removeClass('hidden');
                $("#user-img").attr("src", data.user_img);
                // $("#match-img").attr("src", data.match_img);
                
              }
              else if(data.fun_pass=="False"){
                document.getElementById("comments-list").scrollIntoView();  
                comments = "I couldn't find your face, it must be hiding behind all that ugly";
                $("#comments-list").append("<br>"); 
                $("#comments-list").append(comments);
              }
              else{
                document.getElementById("comments-list").scrollIntoView();  
                comments = data.fun_pass
                $("#comments-list").append("<br>"); 
                $("#comments-list").append(comments);

              }
            },
                    error: function (data) {
                console.log("Error: " + data);
            }
        });
    });

