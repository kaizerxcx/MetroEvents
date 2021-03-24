$( document ).ready(function() {
    user_id =  $('#user_id').val()
    console.log(user_id)
     var href = $('#homeLink').attr('href');
    if(user_id == -1 || user_id == '')
    	 window.location.href = href;
});