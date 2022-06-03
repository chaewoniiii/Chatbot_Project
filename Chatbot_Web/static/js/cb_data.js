function req_data(){
    token = $('#h_csrf').val()
    let cookie = document.cookie
    let csrfToken = cookie.substring(cookie.indexOf('=') + 1)

   $.ajax({
       url : 'http://127.0.0.2:8000/',
       success : function(response){
          $('#test').text(response[0].test1)
          
       }
   })
}