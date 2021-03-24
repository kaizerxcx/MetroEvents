$( document ).ready(function() {
    user_id =  $('#user_sh').val()
    console.log(user_id)
     var href = $('#homeLink').attr('href');
    if(user_id == '' || user_id == null || user_id == undefined)
    	 window.location.href = href;
});


$(document).ready( function () {
    $('#requestTable').DataTable();
} );

$(document).ready( function () {
    user_id = $('#user_sh').val();
    console.log(user_id)
} );





$( "#organizerButton" ).click(function(e) {
 
  $("#organizerButton").html("Loading")
     e.preventDefault();
    $.ajax({
        type:'POST',
        url:" ",
        data:{
        user_id: $('#user_sh').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        action: 'requestOrganizer'
        },
        success:function(json){
             $("#organizerButton").html('Organizer'); 
             location.reload();
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });


})


$( "#adminButton" ).click(function(e) {
 
  $("#adminButton").html("Loading")
     e.preventDefault();
    $.ajax({
        type:'POST',
        url:" ",
        data:{
        user_id: $('#user_sh').val(),
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
        action: 'requestAdmin'
        },
        success:function(json){
             $("#adminButton").html('Site Administrator'); 
             location.reload();
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });


})