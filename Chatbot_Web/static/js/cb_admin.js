$(function(){
    
})

function learning(){
    var data_num = $('#sel_data').val()
    if($('#n_data').css('display', 'none')){
        $('#n_data').css('display', 'block')
        $('.btn_res').css('display', 'block')
        $('#n_data').text(data_num + "개의 데이터를 학습시키겠습니까?")
    }
}

function btn_cancel(){
    $('#n_data').css('display', 'none')
    $('.btn_res').css('display', 'none')
}

function btn_ok(flag){
    if(flag == 1){
        var maskHeight = $(document).height();
        var maskWidth = window.document.body.clientWidth;
    
        var mask = "<div id='mask' style='position:absolute; z-index:9000; background-color:#000000; display:none; left:0; top:0;'></div>";
        var loadingImg = "";
    
        loadingImg += "<div id='loadingImg' class='position-relative'>";
        loadingImg += "<img src='/static/img/Skype-balls-loader-unscreen.gif' class='position-absolute top-0 start-50 translate-middle'/>";
        loadingImg += "</div>";
    
        $('body')
            .append(mask)
            .append(loadingImg)
        
        $('#mask').css({
            'width' : maskWidth,
            'height' : maskHeight,
            'opacity' : '0.1'
        });
    
        $('#mask').show();
    
        $('#loadingImg').show();
    
        setTimeout('closeLoadingWithMask()', 3000)
    }
    else if(flag == 2){
        $('#test_res').css('display', 'none')
        $('#test_btn').css('display', 'none')
    }
    
    
}

function learn_test(){
    $('#test_res').css('display', 'block')
    $('#test_btn').css('display', 'block')
}

function closeLoadingWithMask(){
    $('#mask, #loadingImg').hide();
    $('#mask, #loadingImg').empty();

    alert('학습이 완료되었습니다')

    if($('#n_data').css('display', 'block')){
        $('#n_data').css('display', 'none')
        $('.btn_res').css('display', 'none')
    }
}

