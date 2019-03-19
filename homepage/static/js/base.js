// 默认显示的是数据分析页面
$(function () {
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
            alert(data['info']);
            window.location = "/mainpage";
        } else if (data['init_status'] == false) {
            console.log('登陆失败')
            alert(data['error']);
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
                            '<td>'+
                                '<div class="form-check">'+
                                    '<label class="form-check-label">'+
                                        '<input class="form-check-input friends-select friend-item" onchange="set_friends_tag();" type="checkbox">'+
                                        '<span class="form-check-sign"> </span>'+
                                    '</label>'+
                                '</div>'+
                            '</td>'+
                            '<input type="hidden" name="'+userinfo[i].puid+'">'+
                            '<td>'+userinfo[i].uname+'</td>'+
                            '<td>'+userinfo[i].usex+'</td>'+
                            '<td class="td-actions">'+
                                '<div class="form-button-action">'+
                                    '<button type="button" data-toggle="tooltip " title="" class="btn btn-link btn-simple-danger ">'+
                                    '<i class="la la-times">  </i>'+
                                    '</button>'+
                                '</div>'+
                            '</td>'+
                        '</tr>')

            info.find('input:first').prop('checked',
                userinfo[i].selected?true:false
            );
            $('#friends_info').append(info);
        }

        // 将后端获取到的数据，填充到群组选择框
        let groupinfo = intelligent_result['group_info'];
        for(var i=0; i<groupinfo.length; i++){
            
            let info = $('<tr>'+
                            '<td>'+
                                '<div class="form-check">'+
                                    '<label class="form-check-label">'+
                                        '<input class="form-check-input groups-select" onchange="set_groups_tag();" type="checkbox">'+
                                        '<span class="form-check-sign"> </span>'+
                                    '</label>'+
                                '</div>'+
                            '</td>'+
                            '<input type="hidden" name="'+groupinfo[i].puid+'">'+
                            '<td>'+groupinfo[i].gname+'</td>'+
                            '<td>'+groupinfo[i].gowner+'</td>'+
                            '<td>'+groupinfo[i].pcount+'</td>'+
                            '<td>'+groupinfo[i].mtfratio.male+'/'+groupinfo[i].mtfratio.female+'/'+groupinfo[i].mtfratio.secrecy+'</td>'+
                            '<td class="td-actions">'+
                                '<div class="form-button-action">'+
                                    '<button type="button" data-toggle="tooltip" title="Remove" class="btn btn-link btn-simple-danger">'+
                                        '<i class="la la-times"> </i>'+
                                    '</button>'+
                                '</div>'+
                            '</td>'+
                    '</tr>')
            info.find('input:first').prop('checked',
                groupinfo[i].selected?true:false
            );
            $("#group-box-info").append(info);
        }

        // 更新好友选择框已选择好友和已选择群组
        set_friends_tag();
        set_groups_tag();

        // // 更新智能聊天页面的已选择好友和已选择群组
        var select_friends = $('#checked_friends').children('span');
        var select_groups = $('#checked_groups').children('span');
        var g = $('.authorized_object .card-body .select_groups');
        $('.authorized_object .card-body .select_groups').html(select_groups);
        $('.authorized_object .card-body .select_friends').html(select_friends);
         // 更新好友选择框已选择好友和已选择群组
         set_friends_tag();
         set_groups_tag();
        
    }


});

// // 10秒汇报一次心跳
// open_heart(10000);
// function open_heart(timeout) {
//     var ref = setInterval(function () {
//         $.ajax({
//             url: '/Heart_rate_response/',
//             type: 'get',
//             // data: { 'puid':"{{puid}}" },
//             headers: { "X-CSRFToken": '{{ csrf_token }}' },
//             success: function (arg) {
//                 console.log(arg);
//                 if (arg != 'ok') {
//                     $(location).attr('href', '/index/');
//                 }
//             }
//         })
//     }, timeout);
// }


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








