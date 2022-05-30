$(function(){

$(window).resize(function(){
    var width = $(window).width();
    // 모바일 화면 일 경우
    if(width < 580){
        $('#chat_switch').css('display', 'block')
        $('#chat_content').css('display', 'none')
        $('#list').css('display', 'none')
        // 스위치 값
        $('#chat_chk').click(function(){
            if($('#chat_chk').val() == 0){
                $('#chat_content').css('display', 'block')
                $('#music_content').css('display', 'none')
                $('#chat_chk').val(1)
            }
            else{
                $('#chat_content').css('display', 'none')
                $('#music_content').css('display', 'block')
                $('#chat_chk').val(0)
            }
        })
    }
    else{
        $('#chat_switch').css('display', 'none')
        $('#music_content').css('display', 'block')
        $('#chat_content').css('display', 'block')
        $('#list').css('display', 'block')
    }
})
})