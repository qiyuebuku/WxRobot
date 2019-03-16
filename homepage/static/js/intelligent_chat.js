$(function () {
            // 好友选择列表里的复选框被单击时
            $('#collapseOne [type=checkbox]').change(function () {
                friend_ischecked();
            });

            // 获取被选中的好友标签并将其显示到已选好友列表里
            function friend_ischecked() {
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
                        '男':"<span class='badge badge-default' name='" + uid + "'>" + uname + "</span>",
                        '女':"<span class='badge badge-danger' name='" + uid + "'>" + uname + "</span>",
                        '保密':"<span class='badge badge-success' name='" + uid + "'>" + uname + "</span>",
                    }
                    var label = span_style[sex]
                    // var label = sex == "男" ? $( : $('<span class="badge " name="' + uid + '">' + uname + '</span>');
                    // 根据好友的性别为其创建相应颜色的标签  
                    $('#checked_friends').append(label);
                });
            }

            // 好友选择列表里的复选框被单击时
            $('#collapseTwo [type=checkbox]').change(function () {
                groups_ischecked();
            });


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
            function groups_ischecked() {
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
                    var label = $('<span class="badge ' + span_style[span_index] + '" name="' + uid + '">' + gname + '<span class="badge">' + pcount + '</span>  </span>')
                    // 当将所有的群组样式都是用完毕后，将其下标归零
                    if (++span_index >= 7) {
                        span_index = 0;
                    }
                    $('#checked_groups').append(label);
                });
            }
            $('#save_chat_config').click(function(){
                console.log('save_chat_config');
                var select_friends = $('#checked_friends').children();
                var select_groups = $('#checked_groups').children();
                $.ajax({
                    url: '/save_chat_config/',
                    type: 'get',
                    data:{'friends':select_friends,'groups':select_groups},
                    headers: {
                        "X-CSRFToken": '{{ csrf_token }}'
                    },
                    success: function (arg) {
                        if(arg == "ok"){
                            alert('保存成功');
                            $('.authorized_object .card-body .select_groups').html(select_groups);
                            $('.authorized_object .card-body .select_friends').html(select_friends);
                            $('#friend-selection-box').modal('hide');
                        }
                        else{
                            alert('保存失败');
                        }
                    }
                });



            });



            $('#chat_config').click(function () {
                console.log('ilt-config')
                $.ajax({
                    url: '/groups_and_friends_info/',
                    type: 'get',
                    headers: {
                        "X-CSRFToken": '{{ csrf_token }}'
                    },
                    success: function (arg) {
                        var gu_info = JSON.parse(arg);
                        console.log(gu_info);
                        // if (arg!="没有分析好")
                        // {
                        //     clearInterval(update_analysis);
                        //     var data = JSON.parse(arg);
                        //     console.log(data);
                        //     $('#loading-body').attr('style','display:none');
                        //     $('#loading-body').next().removeClass('hidden');
                        //     update_analysis_page(data);
                        // }
                    }
                });

            });


        });