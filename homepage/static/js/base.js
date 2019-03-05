// 默认显示的是数据分析页面
$(function () {
    $('#my_tab li:eq(0) a').tab('show');
});

// 10秒汇报一次心跳
open_heart(10000);
function open_heart(timeout){
    var ref = setInterval(function () {
    $.ajax({
        url: '/Heart_rate_response/',
        type: 'get',
        // data: { 'puid':"{{puid}}" },
        headers:{ "X-CSRFToken": '{{ csrf_token }}'},  
        success:function(arg){
            console.log(arg);
            if(arg!='ok'){
                $(location).attr('href','/index/');							
            }
        }   
    })
    },timeout);
}


// 给用户所点击的菜单，加上样式
$('#my_tab').children(".nav-item:not('.update-pro')").click(function(e){
    // e.preventDefault()
    // $(this).tab('show');
    $('#my_tab').children(".nav-item:not('.update-pro')").removeClass('active');
    $(this).addClass('active');
    $("html,body").animate({scrollTop:0}, 500);
    var page = $(this).children('a').attr('href');
    if(page=="#data_analysis"){
    }
})



