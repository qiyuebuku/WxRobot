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
// 获取数据分析结果
update_analysis(10000);
function update_analysis(timeout){
    var update_analysis = setInterval(function () {
        $.ajax({
            url: '/analysis_result/',
            type: 'get',
            headers:{ "X-CSRFToken": '{{ csrf_token }}'},  
            success:function(arg){
                
                if (arg!="没有分析好")
                {
                    clearInterval(update_analysis);
                    var data = JSON.parse(arg);
                    console.log(data);
                    $('#loading-body').attr('style','display:none');
                    $('#loading-body').next().removeClass('hidden');
                    update_analysis_page(data);
                }
            }   
        })
    },timeout);
}


function update_analysis_page(data){
    // 好友数量
    griends_count = data['friends_count'];
    // 更新数据分析页面
    $('#friends_count').text(griends_count);
    $('#groups_count').text(data['groups_count']);
    $('#msps_count').text(data['msp_count']);
    update_sex(data['gender_statistics']);
    friends_city(data['region']);  

    var src = "data:image/jpeg;base64," + data['world_cloud'];
    $('#world_cloud').attr('src',src);
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
        // 更新性别饼图属性            
        update_sex(); 
    }
})



// var get_cloudId = setInterval(set_world_cloud,1000);
function set_world_cloud(){
    console.log('get_world_cloud')
    $.ajax({
        url: '/get_world_cloud/',
        type: 'get',
        headers:{ "X-CSRFToken": '{{ csrf_token }}'},  
        success:function(arg){
            console.log(arg)
            if (arg!="no")
            {
                var src = "data:image/jpeg;base64," + arg;
                $('#world_cloud').attr('src',arg);
            }
        }   
    })



}
