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








