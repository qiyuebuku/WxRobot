
// 好友被全选
$('#collapseOne input[type=checkbox]').click(function () {
    if ($(this).prop('checked') == true) {
        $('#checked_friends').children().each(function () {
            $(this).remove();
        })
        // 遍历所有已被选中的好友，为其在已选中好友出添加标签。
        $('#collapseOne tbody input').each(function () {
            var siblings = $(this).parents('td').siblings();
            var uid = $(siblings[0]).attr('name');
            // 获取好友名称
            var uname = $(siblings[1]).text();
            var sex = $(siblings[2]).text();
            // label样式
            var span_style = {
                '男': "<span class='friends badge badge-default' name='" + uid + "'>" + uname + "</span>",
                '女': "<span class='friends badge badge-danger' name='" + uid + "'>" + uname + "</span>",
                '保密': "<span class='friends badge badge-success' name='" + uid + "'>" + uname + "</span>",
            }
            var label = span_style[sex]
            // console.log(span_style);
            // var label = sex == "男" ? $( : $(''<span class="badge " name="' + uid + '">'' + uname + ''</span>'');
            // 根据好友的性别为其创建相应颜色的标签  
            $('#checked_friends').append(label);
        });
    }else{
        $('#checked_friends').children().each(function () {
            $(this).remove();
        })
    }
});

// 某个好友被选中
function set_friends_tag() {

    // 获取被选中的好友标签并将其显示到已选好友列表里
    // 清空上一次选择的好友标签                                                                                                                                                                                                                                                         
    $('#checked_friends').children().each(function () {
        $(this).remove();
    })
    // 遍历所有已被选中的好友，为其在已选中好友出添加标签。
    $('#collapseOne tbody input:checked').each(function () {
        var siblings = $(this).parents('td').siblings();
        var uid = $(siblings[0]).attr('name');
        // 获取好友名称
        var uname = $(siblings[1]).text();
        var sex = $(siblings[2]).text();
        // label样式
        var span_style = {
            '男': "<span class='friends badge badge-default' name='" + uid + "'>" + uname + "</span>",
            '女': "<span class='friends badge badge-danger' name='" + uid + "'>" + uname + "</span>",
            '保密': "<span class='friends badge badge-success' name='" + uid + "'>" + uname + "</span>",
        }
        var label = span_style[sex]
        // console.log(span_style);
        // var label = sex == "男" ? $( : $(''<span class="badge " name="' + uid + '">'' + uname + ''</span>'');
        // 根据好友的性别为其创建相应颜色的标签  
        $('#checked_friends').append(label);
    });

}


// 群聊被全选
$('#collapseTwo [type=checkbox]').change(function () {
    if ($(this).prop('checked') == true) {
        // 清空上一次选择的群组标签
        $('#checked_groups').children().each(function () {
            $(this).remove();
        })
        var span_style = [
            'badge-count',
            'badge-default',
            'badge-primary',
            'badge-info',
            'badge-success',
            'badge-warning',
            'badge-danger'
        ]
        var span_index = 0;
        // 遍历所有已被选中的群组，为其在已选中群组的添加标签。
        $('#collapseTwo tbody input[type=checkbox]').each(function () {
            var siblings = $(this).parents('td').siblings();
            var uid = $(siblings[0]).attr('name');
            // 获取群组名称
            var gname = $(siblings[1]).text(); // group name
            var gowner = $(siblings[2]).text(); // group owner
            var pcount = $(siblings[3]).text(); // people count
            var mtfratio = $(siblings[4]).text(); //male to female ratio 
            //创建群标签
            var label = $('<span class="groups badge ' + span_style[span_index] + '" name="' + uid + '">' + gname + '<span class="badge">' + pcount + '</span> </span>')
            // 当将所有的群组样式都是用完毕后，将其下标归零
            if (++span_index >= 7) {
                span_index = 0;
            }
            $('#checked_groups').append(label);
        });
    }else{
       // 清空上一次选择的群组标签
        $('#checked_groups').children().each(function () {
            $(this).remove();
        })
    }
});

// 某个群聊被选中
function set_groups_tag(){
        var span_style = [
            'badge-count',
            'badge-default',
            'badge-primary',
            'badge-info',
            'badge-success',
            'badge-warning',
            'badge-danger'
        ]
        var span_index = 0;
        // 获取被选中的群组，并将其显示到已选群组列表里
        // 清空上一次选择的群组标签
        $('#checked_groups').children().each(function () {
            $(this).remove();
        })
        // 遍历所有已被选中的群组，为其在已选中群组的添加标签。
        $('#collapseTwo tbody input:checked').each(function () {
            var siblings = $(this).parents('td').siblings();
            var uid = $(siblings[0]).attr('name');
            // 获取群组名称
            var gname = $(siblings[1]).text(); // group name
            var gowner = $(siblings[2]).text(); // group owner
            var pcount = $(siblings[3]).text(); // people count
            var mtfratio = $(siblings[4]).text(); //male to female ratio 
            //创建群标签
            var label = $('<span class="groups badge ' + span_style[span_index] + '"name="' + uid + '">' + gname + '<span class="badge">' + pcount + '</span> </span>')
            // 当将所有的群组样式都是用完毕后，将其下标归零
            if (++span_index >= 7) {
                span_index = 0;
            }
            $('#checked_groups').append(label);
        });
}


// 保存
$('#save_chat_config').click(function () {
    var select_friends = $('#checked_friends').children('span');
    var select_groups = $('#checked_groups').children('span');
    var friends_array = new Array();
    var groups_array = new Array();

    for(var i=0; i<select_friends.length; i++){
        let s = $(select_friends[i]);
        // console.log(s)
        // console.log(s.attr('name'))
        friends_array.push({'fid':s.attr('name'),'fname':s.text()});
    }
    for(var i=0; i<select_groups.length; i++){
        let s = $(select_groups[i]);
        // console.log(s)
        // console.log(s.attr('name'))
        groups_array.push({'gid':s.attr('name'),'gname':s.text()});
    }

    // console.log(select_friends.length)
    // console.log(friends_array)
    // console.log(groups_array)
    // console.log(JSON.stringify(friends_array),JSON.stringify(select_groups))

    $.ajax({
        url: '/save_chat_config/',
        type: 'post',
        data: { 'friends': JSON.stringify(friends_array), 'groups': JSON.stringify(groups_array) },
        headers: {
            "X-CSRFToken": '{{ csrf_token }}'
        },
        success: function (arg) {
            // console.log(arg)
            if (arg == "ok") {
                alert('保存成功');
                $('.authorized_object .card-body .select_groups').html(select_groups);
                $('.authorized_object .card-body .select_friends').html(select_friends);
                //  更新好友选择框已选择好友和已选择群组
                set_friends_tag();
                set_groups_tag();
                $('#friend-selection-box').modal('hide');
            }
            else {
                alert('保存失败');
            }
        }
    });



});