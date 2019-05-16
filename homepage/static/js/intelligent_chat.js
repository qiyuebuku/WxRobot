
// 好友被全选
$('#collapseOne input[type=checkbox]').click(function () {
    set_friends_status(this);
});

// 好友被选中
function set_friends_status(self) {
    let puid = $(self).val();
    let is_checked = $(self).prop('checked');

    var friends_array = new Array();
    var friends_array_html = new Array();
    var span_style = {
        '男':"badge-default",
        '女':" badge-danger",
        '保密':"badge-success"
    }
    if (puid == "all") {
        console.log("所有");
        $('#friends_info .form-check-input').each(function () {
            var siblings = $(this).parents('td').siblings();
            let puid = $(siblings[0]).attr('name');
            // 获取好友名称
            var uname = $(siblings[1]).text();
            // 获取好友性别
            var sex = $(siblings[2]).text();
            friends_array.push(puid);
            let label = $("<span class='friends badge "+span_style[sex]+"' name='" + puid + "'>" + uname + "</span>");
            friends_array_html.push(label)
        });
    } else {
        let tr = $(self).parents('tr').children('td');
        var uname = $(tr[0]).text();
        var sex = $(tr[1]).text();
        let puid = $(self).val();
         // label样式
        let label = $("<span class='friends badge "+span_style[sex]+"' name='" + puid + "'>" + uname + "</span>");
        friends_array.push(puid);
        friends_array_html.push(label)
        is_all(self);
    };


    // 如果被选中
    if (is_checked) {
        save_config(true,friends_array_html, null,friends_array,[])

    } else {
        save_config(false,friends_array_html, null,friends_array,[]);
    }
}


// 群聊被选中
function set_groups_status(self) {
    let puid = $(self).val();
    let is_checked = $(self).prop('checked');
    var groups_array = new Array();
    var groups_array_html = new Array();
    let span_index = 0;
    var span_style = [
        'badge-count',
        'badge-default',
        'badge-primary',
        'badge-info',
        'badge-success',
        'badge-warning',
        'badge-danger'
    ]
    if (puid == "all") {
        console.log("所有");
        // 遍历所有已被选中的群组，为其在已选中群组的添加标签。
        $('#groups_info .form-check-input').each(function () {
            var siblings = $(this).parents('td').siblings();
            var puid = $(siblings[0]).attr('name');
            // 获取群组名称
            var gname = $(siblings[1]).text(); // group name
            var gowner = $(siblings[2]).text(); // group owner
            var pcount = $(siblings[3]).text(); // people count
            var mtfratio = $(siblings[4]).text(); //male to female ratio 
            //创建群标签
            var label = $('<span class="groups badge ' + span_style[span_index] + '"name="' + puid + '">' + gname + '<span class="badge">' + pcount + '</span> </span>')
            // 当将所有的群组样式都是用完毕后，将其下标归零
            if (++span_index >= 7) {
                span_index = 0;
            }
            groups_array.push(puid);
            groups_array_html.push(label);
        });

    } else { 
        let siblings = $(self).parents('td').siblings();
        let puid = $(siblings[0]).attr('name')
        var gname = $(siblings[1]).text(); // group name
        var gowner = $(siblings[2]).text(); // group owner
        var pcount = $(siblings[3]).text(); // people count
        var mtfratio = $(siblings[4]).text(); //male to female ratio
        //创建群标签
        var label = $('<span class="groups badge ' + span_style[span_index] + '"name="' + puid + '">' + gname + '<span class="badge">' + pcount + '</span> </span>')
        // 当将所有的群组样式都是用完毕后，将其下标归零
        if (++span_index >= 7) {
            span_index = 0;
        }
         groups_array.push(puid);
         groups_array_html.push(label);
         is_all(self);
    };


    // 如果被选中
    if (is_checked) {
        save_config(true,null,groups_array_html,[],groups_array)

    } 
    // 如果没取消勾选
    else {
        save_config(false,null,groups_array_html,[],groups_array);
    }
}


// 保存
function save_config(model, friends_array_html, groups_array_html, friends_array, groups_array) {
    $.ajax({
        url: '/save_chat_config/',
        type: 'post',
        data: { 'model': model, 'friends': JSON.stringify(friends_array), 'groups': JSON.stringify(groups_array) },
        headers: {
            "X-CSRFToken": '{{ csrf_token }}'
        },
        success: function (arg) {
            // 如果保存成功
            if (arg == "ok") {
                // 增加模式
                if(model){
                    save_select_config("friends",friends_array_html);
                    save_select_config("groups",groups_array_html);
                }
                // 删除模式
                else{
                    del_select_config("friends",friends_array_html);
                    del_select_config("groups",groups_array_html);
                }
            }
            // 保存失败
            else {
                alert('授权失败')
            }
        }
    });
}

// 好友显示到授权成功列表出
// model: 群组/好友
// array_html：需要保存的标签数组
function save_select_config(model,array_html){
    if(array_html){
        let select_box;
        if(model == "friends"){
            select_box = $('.authorized_object .card-body .select_friends');
        }else{
            select_box = $('.authorized_object .card-body .select_groups');
        }
        // console.log("select_box",select_box)
        for (var i = 0; i < array_html.length; i++) {
            let label = $(array_html[i]);
            let status = true;
            // 如果已经存在，则不再添加
            select_box.children().each(function(){
                let puid1 = $(this).attr('name');
                let puid2 = label.attr('name')
                if(puid1==puid2){
                    status = false;
                    return;
                }
            })
            // 如果不存在，则添加到前端
            if(status){
                select_box.append(label);
            }
        }
    }
}


function is_all(self){
    let all = $(self).parents('tbody').prev().children().find('.select-all-checkbox');
    let select_length = 0;
    let input_all = $(self).parents('tr').siblings().children().find('.form-check-input');
    input_all.each(function(){
        if($(this).prop('checked')){
            select_length+=1
        }
    })
    self_checked = $(self).prop('checked')
    if (self_checked){
        select_length+=1;
    }
    input_length= input_all.length+1;
    if(select_length == input_length){
        all.prop('checked',true);
    }else{
        all.prop('checked',false);
    }
}

// 好友显示到授权成功列表出
// model: 群组/好友
// array_html：需要保存的标签数组

function del_select_config(model,array_html){
    if(array_html){
        let select_array;
        if(model == "friends"){
            select_array =  $('.authorized_object .card-body .select_friends').children();
        }else{
            select_array = $('.authorized_object .card-body .select_groups').children();
        }
        // 遍历已显示的所有标签
        select_array.each(function(){
            // 便利所有需要删除的标签
            // 和已显示的每个标签puid做对比
            // 如果两者一致，则将从前端页面中删除
            for (var i = 0; i < array_html.length; i++) {
                let label = $(array_html[i]);
                if ($(this).attr('name') == label.attr('name')){
                    $(this).remove();
                }
            }
        })
    
    }
}




