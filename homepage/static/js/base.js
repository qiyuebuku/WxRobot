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








