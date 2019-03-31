function activate_plugin(self){
    id = $(self).val();
    state = $(self).prop('checked');
    console.log("id为："+id+"触发了",state,"操作");

    $.ajax({
        url:'/set_plugin_state/',
        type:'post',
        data:{'id':id,'state':state},
        dataType:'json',
        headers:{ "X-CSRFToken": '{{ csrf_token }}'},  
    })

}