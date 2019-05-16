// 默认显示的是数据分析页面
$(function () {

    $('#clues').blur(function(){
        text = $(this).val();
        console.log(text)
        $.ajax({
            url:'/save_clues/',
            type:'post',
            headers:{ "X-CSRFToken": $('#csrf_token').val() },  
            data:{"text":text}
        })
    })

    $('.regularly_radio').click(function(){
        repetition = $('#repetition').val()
        timer = $("#regularly_timer").val();
        text = $('#regularly_text').val()
        timer_send_isActive = $('.regularly_radio:checked').val();
        console.log(repetition,timer,text,timer_send_isActive)
        $.ajax({
            url:'/save_timer_send/',
            type:'post',
            headers:{ "X-CSRFToken": $('#csrf_token').val() },  
            data:{"repetition":repetition,"timer":timer,'text':text,'timer_send_isActive':timer_send_isActive}
        })
    })

    $('#repetition,#regularly_timer,#regularly_text,regularly_radio').change(function(){
        repetition = $('#repetition').val()
        timer = $("#regularly_timer").val();
        text = $('#regularly_text').val()
        timer_send_isActive = $('.regularly_radio:checked').val();
        console.log(repetition,timer,text,timer_send_isActive)
        $.ajax({
            url:'/save_timer_send/',
            type:'post',
            headers:{ "X-CSRFToken": $('#csrf_token').val() },  
            data:{"repetition":repetition,"timer":timer,'text':text,'timer_send_isActive':timer_send_isActive}
        })
    })
    $('#my_tab li:eq(0) a').tab('show');

    var username = $('#username').val();
    var socket = new WebSocket('ws://' + window.location.host + "/homepage/"+username);
    socket.onopen = function open() {
        console.log('Websockets connection created.');
    };

    socket.onmessage = function message(event) {
        var data = JSON.parse(event.data);
        console.log('接收到消息', data)

        if("analysis_result" in data){
            $('#loading-data-analysis').attr('style','display:none');
            $('#loading-data-analysis').next().removeClass('hidden');
            update_analysis_page(data["analysis_result"]);
        }
        else if("intelligent_result" in data){
            $('#loading-intelligent-chat').attr('style','display:none');
            $('#loading-intelligent-chat').next().removeClass('hidden');
            console.log("智能聊天模块加载完毕!!!")
            set_friend_box_info(data['intelligent_result']);
        }
                      
        if (data['init_status']) {
            console.log('登录成功')
            // alert(data['info']);
            window.location = "/mainpage";
        } else if (data['init_status'] == false) {
            console.log('登陆失败')
            // alert(data['error']);
        } else if (data['qrcode']) {
            var src = "data:image/jpeg;base64," + data['qrcode'];
            $('#img_page').attr('src', src);
        }
        else {
            var username = encodeURI(data['username']);
            if (data['is_logged_in']) {
                // user.html(username + ': 在线');
            }
            else {
                // user.html(username + ': 离线');
            }
        }
    };
    if (socket.readyState == WebSocket.OPEN) {
        socket.onopen();
    }


    //好友选择框的数据更新
    function set_friend_box_info(intelligent_result){
        // 将后端获取到的数据，填充到好友选择框
        let userinfo = intelligent_result['user_info'];
        for(var i=0; i<userinfo.length; i++){
            let info = $('<tr>'+
                            '<input type="hidden" name="'+userinfo[i].puid+'">'+
                            '<td>'+userinfo[i].uname+'</td>'+
                            '<td>'+userinfo[i].usex+'</td>'+
                            '<td class="td-actions" >'+
                                '<div class="form-check">'+
                                    '<label class="form-check-label">'+
                                        '<input class="form-check-input friends-select friend-item" value="'+userinfo[i].puid+'" onchange="set_friends_status(this);" type="checkbox">'+
                                        '<span class="form-check-sign"> </span>'+
                                    '</label>'+
                                '</div>'+
                            '</td>'+
                        '</tr>')

            info.find('.form-check-input').prop('checked',
                userinfo[i].selected?true:false
            );
            
            info.append('<input type="checkbox" checked data-toggle="toggle" data-onstyle="primary" data-style="btn-round">')
            $('#friends_info').append(info)
        }

        // 将后端获取到的数据，填充到群组选择框
        let groupinfo = intelligent_result['group_info'];
        for(var i=0; i<groupinfo.length; i++){
            
            let info = $('<tr>'+
                            '<input type="hidden" name="'+groupinfo[i].puid+'">'+
                            '<td>'+groupinfo[i].gname+'</td>'+
                            '<td>'+groupinfo[i].gowner+'</td>'+
                            '<td>'+groupinfo[i].pcount+'</td>'+
                            '<td>'+groupinfo[i].mtfratio.male+'/'+groupinfo[i].mtfratio.female+'/'+groupinfo[i].mtfratio.secrecy+'</td>'+
                            '<td>'+
                                '<div class="form-check">'+
                                    '<label class="form-check-label">'+
                                        '<input class="form-check-input groups-select" onchange="set_groups_status(this);" type="checkbox">'+
                                        '<span class="form-check-sign"> </span>'+
                                    '</label>'+
                                '</div>'+
                            '</td>'+
                    '</tr>')
            info.find('.form-check-input').prop('checked',
                groupinfo[i].selected?true:false
            );
            $("#groups_info").append(info);
        }

        // 更新好友选择框已选择好友和已选择群组
        // set_friends_tag();
        // set_groups_tag();
        set_select();
        
    }


});


// 将已经选中的好友和群组显示到前端上
function set_select(){
    let friends_array_html= new Array;
    let groups_array_html = new Array;
    let span_index = 0;
    var groups_span_style = [
        'badge-count',
        'badge-default',
        'badge-primary',
        'badge-info',
        'badge-success',
        'badge-warning',
        'badge-danger'
    ]
    var friend_span_style = {
        '男':"badge-default",
        '女':" badge-danger",
        '保密':"badge-success"
    }

    $('#friends_info .form-check-input:checked').each(function () {
        var siblings = $(this).parents('td').siblings();
        let puid = $(siblings[0]).attr('name');
        // 获取好友名称
        var uname = $(siblings[1]).text();
        // 获取好友性别
        var sex = $(siblings[2]).text();
        let label = $("<span class='friends badge "+friend_span_style[sex]+"' name='" + puid + "'>" + uname + "</span>");
        friends_array_html.push(label)
        is_all($(this));
    });


    // 遍历所有已被选中的群组，为其在已选中群组的添加标签。
    $('#groups_info .form-check-input:checked').each(function () {
        var siblings = $(this).parents('td').siblings();
        var puid = $(siblings[0]).attr('name');
        // 获取群组名称
        var gname = $(siblings[1]).text(); // group name
        var gowner = $(siblings[2]).text(); // group owner
        var pcount = $(siblings[3]).text(); // people count
        var mtfratio = $(siblings[4]).text(); //male to female ratio 
        //创建群标签
        var label = $('<span class="groups badge ' + groups_span_style[span_index] + '"name="' + puid + '">' + gname + '<span class="badge">' + pcount + '</span> </span>')
        // 当将所有的群组样式都是用完毕后，将其下标归零
        if (++span_index >= 7) {
            span_index = 0;
        }
        groups_array_html.push(label);
    });

    save_select_config("friends",friends_array_html);
    save_select_config("groups",groups_array_html);


}

// 给用户所点击的菜单，加上样式
$('#my_tab').children(".nav-item:not('.update-pro')").click(function (e) {
    // e.preventDefault()
    // $(this).tab('show');
    $('#my_tab').children(".nav-item:not('.update-pro')").removeClass('active');
    $(this).addClass('active');
    $("html,body").animate({ scrollTop: 0 }, 500);
    var page = $(this).children('a').attr('href');
    if (page == "#data_analysis") {
    }
})
function refresh_plug_shops(){
    $.ajax({
        url:'/get_plug_shops/',
        type:'get',
        dataType:'json',
        success:function(data){
            console.log(data)
            // 如果查询结果正常
            if (data['status']){
                // 清空前端中原先所有的col

                // 将得到的数据渲染到页面中

                

            }

        }
    })
}


function close_user_plug(self){
    let id = $(self).val();
    console.log(id);
    let plug_shop_id = $(self).attr('plug-shop-id');
    console.log('plug-shop-id:'+plug_shop_id);
    let col = $(self)
    $.ajax({
        url:'/del_plug/',
        type:'post',
        data:{'id':id},
        headers:{ "X-CSRFToken": $('#csrf_token').val()},
        success:function(data){
            if(data=="ok"){
                // 将插件从已拥有删除
                col.parents('.col-md-12').first().remove();

                // 将插件商店中对应的插件状态更改为未拥有
                // 1. 获取插件商店中对应id的row
                let row = $("#plug-shops .row button[value='"+plug_shop_id+"']")
                // 2. 更改插件状态
                row.text('获取');
                row.attr('class','btn btn-lg btn-success');
                row.attr('onclick','get_more_plugins(this);');
            }
        }  
    })
}

function get_more_plugins(self){
    id = $(self).val();
    $.ajax({
        url:'/add_user_plug/',
        type:'post',
        data:{'id':id},
        dataType:'json',
        headers:{ "X-CSRFToken": $('#csrf_token').val()},
        success:function(data){
            console.log("id"+id);
            console.log("data"+data);
            if(data['status']){
                console.log('添加成功')
                $(self).text('已拥有');
                $(self).attr('class','btn btn-lg btn-default disabled');
                $(self).attr('onclick','');
                let user_plug_id = data['user_plug']['id'];
                let isActive = data['user_plug']['isActive'] == true ?'checked="checked"':''
                let plug = data['user_plug']['plug']
                console.log(user_plug_id,plug)
                let user_plug = $(''+
                '<div class="col-md-12">'+
                    '<div class="card">'+
                        '<div class="card-header">'+
                            '<button type="button" onclick="close_user_plug(this);" class="close" value="'+user_plug_id+'" plug-shop-id="'+plug['id']+'" data-dismiss="alert" aria-label="Close">'+
                                '<span aria-hidden="true">&times;</span>'+
                            '</button>'+
                            '<h4 class="card-title">'+plug['ptitle']+'</h4>'+
                            '<p class="card-category">'+plug['pdescribe']+'</p>'+
                        '</div>'+
                        '<div class="card-body ">'+
                            '<p class="demo">'+
                            '<button type="button" class="btn btn-sm btn-default disabled" onclick="activate_plugin(this);" value="'+user_plug_id+'" >未开启</button>'+
                            '<button class="btn btn-sm btn-info" id="chat_config" data-toggle="modal" data-target="#friend-selection-box">config'+
                            '</button>'+
                            '</p>'+
                        '</div>'+
                    '</div>'+
                '</div>');
                $('#my-plug .row').append(user_plug);
            }

        }  
    })
    // refresh_plug_shops();
    console.log(id);
}

$('.get-more-plugins').click(function(){
    id = $(this).val();
    $.ajax({
        url:'/add_user_plug/',
        type:'post',
        data:{'id':id},
        dataType:'json',
        headers:{ "X-CSRFToken": $('#csrf_token').val()},
        success:function(data){
            console.log(data)
        }  
    })
})











