
// document.getElementById("submit-button").addEventListener("click", haltFunction);




  
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


Dropzone.options.myDropzone = {
  url:'/',
  method:'post',
  maxFiles: 1,
  addRemoveLinks: true,
  dictDefaultMessage: "Drop files here to upload",
  acceptedFiles: "image/*",
  maxFilesize: 10,
  resizeWidth: null,
  resizeHeight: null,

  init: function() {

  this.on("addedfile", function(file) {

    if (this.files.length > 1) {
      this.removeFile(this.files[0]);
    }
    this.options.dictRemoveFile = "Remove";
    this.options.dictCancelUpload = "Cancel";

   
    
  });

    
  this.on("maxfilesexceeded", function(file) {
    this.removeFile(file);
    this.submit();

  });

  this.on("complete", function(file) {
    haltFunction();
  });
  this.on("addedfile", function (file) {
    // Perform any additional processing on the file here
  
    // Use FormData and $.ajax to send the file
    var formData = new FormData();
    formData.append("image", file);
    $.ajax({
      url: "/", // the URL to handle the file upload
      method: "POST",
      data: formData,
      processData: false,
      contentType: false,
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
            if (i < 5 && i < comments.length) {
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
          $("#comments-list").text("");
          $("#toast-body").text("");
          document.getElementById("comments-list").scrollIntoView();  
          comments = "Failed to detect face. Please try a different image";
          $("#comments-list").append("<br>"); 
          $("#comments").append(comments);
          $("#toast-body").append(comments);

          $('.toast').toast('show');
          setTimeout(function(){
              $('.toast').toast('hide');
          }, 5000);
        }

        else{

          $("#comments-list").text("");
          $("#toast-body").text("");

          document.getElementById("comments-list").scrollIntoView();  
          comments = data.fun_pass
          $("#comments-list").append("<br>"); 
          $("#comments-list").append(comments);
          $("#toast-body").append(comments);

          $('.toast').toast('show');
          setTimeout(function(){
              $('.toast').toast('hide');
          }, 5000);

        }
      
      },
      error: function (error) {
        // Handle the error of the file upload
        console.log(error)
      },
    });
  });


        }
      }
    


      

        


//   $("form").submit(function(event) {
//     // event.preventDefault();
//     var formData = new FormData(this);
//     $("#comments-list").text("");
//     $.ajax({
//         url: '/',
//         type: 'POST',
//         data: formData,
//         contentType: false,
//         processData: false,
//         success: function (data) {  
//           console.log(data.fun_pass)
//           if (data.fun_pass == "True") {
//             document.getElementById("comments-list").scrollIntoView();  
//             var comments = data.comments;
//             comments = JSON.parse(comments);
//             comments = comments.map(comment => comment.replace("[", "").replace("]", "").replace("\u2019", "'"));
//             $("#comments-list").append("<br>"); 

//             function typeComment(i, j) {  
//               typing = true;
//               if (i < comments.length) {
//                 if (j < comments[i].length) {
//                   $('.blinking-cursor').remove();
//                   $("#comments-list").append(comments[i][j]);
//                   $("#comments-list").append("<span class='blinking-cursor'>' '</span>");
//                   var delay = Math.floor(Math.random() * 75) + 25;
//                   document.querySelector('.blinking-cursor').style.animationDelay = delay + 'ms';
//                   setTimeout(function () {
//                     typeComment(i, j + 1);
//                   }, delay);
//                 } else {
//                   $("#comments-list").append("<br>").append("<br>");
//                   typing_time = setTimeout(function () {
//                     typeComment(i + 1, 0);
//                   }, 500);
//                 }
//               }
//               typing = false;
//             }
//             setTimeout(function(){
//               document.getElementById("comments-list").scrollIntoView();  
//               typeComment(0, 0);
//             },1000)
//             $('frame').removeClass('hidden');
//             $("#user-img").attr("src", data.user_img);
//             // $("#match-img").attr("src", data.match_img);
            
//           }
//           else if(data.fun_pass=="False"){
//             $("#comments-list").text("");
//             $("#toast-body").text("");
//             document.getElementById("comments-list").scrollIntoView();  
//             comments = "Failed to detect face. Please try a different image";
//             $("#comments-list").append("<br>"); 
//             $("#comments").append(comments);
//             $("#toast-body").append(comments);

//             $('.toast').toast('show');
//             setTimeout(function(){
//                 $('.toast').toast('hide');
//             }, 5000);
//           }

//           else{

//             $("#comments-list").text("");
//             $("#toast-body").text("");

//             document.getElementById("comments-list").scrollIntoView();  
//             comments = data.fun_pass
//             $("#comments-list").append("<br>"); 
//             $("#comments-list").append(comments);
//             $("#toast-body").append(comments);

//             $('.toast').toast('show');
//             setTimeout(function(){
//                 $('.toast').toast('hide');
//             }, 5000);

//           }
//         },
//                 error: function (data) {
//             console.log("Error: " + data);
//         }
//     });
// });