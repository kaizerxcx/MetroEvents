// Submit post on submit
// $('#register-form').on('submit', function(event){
//     event.preventDefault();
//    // console.log("create post is working!") // sanity check
//    console.log("firstname: "+ $('#firstname').val() )
//     register_user();
// });

  
//$('#modalLRFormDemo').modal('show')
$('#success-registered').hide()
$('#invalid-login').hide()
$('#registrationStatus').hide()
$('#loginStatus').hide()
$(document).on('submit', '#register-form',function(e){
	 e.preventDefault();
     $('#Signup').hide()
     $('#registrationStatus').show()
    $.ajax({
        type:'POST',
        url:" ",
        data:{
        firstname : $('#firstname').val(),
       	middlename : $('#middlename').val(),
        lastname : $('#lastname').val(),
        username: $('#username').val(),
        password: $('#password').val(),
        age: $('#age').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        action: 'post'
        },
        success:function(json){
            $('#registrationStatus').hide()
              $('#Signup').show()
        	$('#success-registered').show()
        	$('#login').trigger("click");
            document.getElementById("register-form").reset();
           // $('#login_username').val(json.username); 
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});

$(document).on('submit', '#login-form',function(e){
     e.preventDefault();
      $('#loginButton').hide()
       $('#loginStatus').show()
    $.ajax({
        type:'POST',
        url:" ",
        data:{
        username: $('#login_username').val(),
        password: $('#login_password').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        action: 'postLogin'
        },
        success:function(json){
           
           // var data = $.parseJSON(json)
           // console.log(data[0].pk)
            $('#loginButton').show()
             $('#loginStatus').hide()
             
            // // is a member
            // if(json.status == 1){
            //     window.location.replace("user");
            // }
            // else if(json.status==3){
            //      window.location.replace("organizer");
            // }
            //  else if(json.status == 2){
            //       window.location.replace("admin");
            //  }
            //  else{
            //        $('#invalid-login').show()
            //        console.log("invalid-login")
            //  }

            if (json.status == 0) {
                $('#invalid-login').show()
            }
            if (json.status == 1) {
                 window.location.replace("user");
            }
            if (json.status==2) {
                 window.location.replace("admin");
            }
            if (json.status==3) {
                 window.location.replace("organizer");
            }


           console.log(json.status)
            document.getElementById("login-form").reset();
           // $('#login_username').val(json.username); 
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});
