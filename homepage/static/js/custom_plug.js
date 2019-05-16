function activate_plugin(self){
    id = $(self).val();
<<<<<<< HEAD
    text = $(self).text();
    state = text=="未开启"? true:false 
    console.log("状态为："+state)

    if(state){
        $(self).text('已开启');
        $(self).attr('class','btn btn-sm btn-success')
    }else{
        $(self).text('未开启');
        $(self).attr('class','btn btn-sm btn-default disabled');
    }
=======
    state = $(self).prop('checked');
    console.log("id为："+id+"触发了",state,"操作");
>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97

    $.ajax({
        url:'/set_plugin_state/',
        type:'post',
        data:{'id':id,'state':state},
        dataType:'json',
        headers:{ "X-CSRFToken": '{{ csrf_token }}'},  
<<<<<<< HEAD
        success:function(data){
            console.log(data);
            if(data['status']==false){
                if(state){
                    $(self).text('未开启');
                    $(self).attr('class','btn btn-sm btn-default disabled');
                }else{
                    $(self).text('已开启');
                    $(self).attr('class','btn btn-sm btn-success')
                }
            }
        }
=======
>>>>>>> acb8c86e5915306157008056c793ddc27ee3fd97
    })

}