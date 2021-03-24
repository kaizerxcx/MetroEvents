// $( document ).ready(function() {
//     user_id =  $('#user_sh').val()
//     console.log(user_id)
//      var href = $('#homeLink').attr('href');
//     if(user_id == '' || user_id == null || user_id == undefined)
//     	 window.location.href = href;
// });


$(document).ready( function () {
    $('#requestTable').DataTable();
} );

$(document).ready( function () {
    user_id = $('#user_sh').val();
    console.log(user_id)
} );

