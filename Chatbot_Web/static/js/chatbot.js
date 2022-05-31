$(function(){
    // SEND 버튼을 누르거나 
    $("#sendbtn").click(function(){
        send_message();
    });

    // ENTER key 가 눌리면
    $("#chattext").keyup(function(event){
        if(event.keyCode == 13){
            send_message()
        }
    })
})

function send_message(){
    const chattext = $('#chattext').val().trim();

    //입력한 메세지가 없으면 리턴
    if(chattext == ""){
        $("#chattext").focus();
        return
    }

    // 입력한 채팅 화면에 출력
    const addtext = "<div style='margin:15px 0;text-align:right;'> <span style='padding:3px 10px;background-color:#B7F0B1;border-radius:3px;'>" + chattext + "</span></div>";
    $('#chatbox').append(addtext);

    // 먼저 입력했던 것은 지우기
    $("#chattext").val("");
    $("#chattext").focus();
    
     // 이쪽 부분은 수정될 예정?
    // API 서버에 요청할 데이터
    const jsonData = {
        query: chattext
    }
   
    $.ajax({
        url: "http://127.0.0.10:5000/query/TEST",
        type: "POST",
        data: JSON.stringify(jsonData),
        dataType: "JSON",  // 응답받을 데이터 타입
        contentType: "application/json; charset=utf-8",

        success: function(response){
            // 답변 텍스트는 response.Answer 에 담겨있다
            $chatbox = $('#chatbox');

            // 답변 출력
            const bottext = "<div style='margin:15px 0;text-align:left;'><span style='padding:3px 10px;background-color:#CEFBC9;border-radius:3px;'>" + response.Answer + "</span></div>";
            $chatbox.append(bottext);

            // 스크롤 조정하기
            $chatbox.animate({scrollTop: $chatbox.prop('scrollHeight')})
        }
    });

}