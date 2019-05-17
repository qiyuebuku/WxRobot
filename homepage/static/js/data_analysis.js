// 头像
// update_avatar();
// // 签名
// update_signature();



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




// 好友地区分布图
function friends_city(region) {

	var dom = document.getElementById("container");
	var myChart = echarts.init(dom);
	var app = {};
	console.log("region", region)
	// 各城市人数统计数组
	var citys = [];
	// 遍历所有好友的城市,统计各个城市的人数
	for(var i in region){
		// 如果城市字符串为空，则将其归为保密
		var name = region[i].length == 0 ? '保密' : region[i];
		// 创建一个城市列表副本，用于循环遍历
		var citys2 = citys;
		// 遍历已加入到列表里的城市，将其和当前循环到的城市比较
		// 如果当前城市已经存在于列表当中，将其下标所对应的城市人数+1
		// 否则将其加入到城市列表
		var res = false;
		for(var j=0;j<citys2.length;j++){
			if(name == (citys2[j]['name'])){
				citys[j]['value']++;
				res = true;
				break;
			}
		}
		if(!res){
			citys.push({'name':name,'value':1});
		}
	}	
	
	// 对城市按照人数从小到达排序
	for(var i=1;i<citys.length;i++){
		// console.log('i',i);
		// 获取当前无序数据
		var temp = citys[i];
		// console.log(temp);
		var pos = i;
		for(var j = i-1;j>=0;j--){
			// console.log('j',j);
			if(citys[j]['value']>temp['value']){
				citys[j+1] = citys[j];
				pos = j;
			}else{
				pos = j+1;
				break;
			}
		}
		citys[pos] = temp;
	}

	console.log('人数最少的城市',citys[0]['value'],'人数最多的城市:', citys[citys.length-1]['value'])
	option = null;
	option = {
		title: {
			text: '微信好友全国分布图',
			subtext: '真实数据',
			x: 'center'
		},
		tooltip: {
			trigger: 'item'
		},
		legend: {
			orient: 'vertical',
			x: 'left',
			data: ['好友数量']
		},
		dataRange: {
			min: citys[0]['value'],
			max: citys[citys.length-1]['value'],
			x: 'left',
			y: 'bottom',
			text: ['高', '低'], // 文本，默认为数值文本
			calculable: true
		},
		toolbox: {
			show: true,
			orient: 'vertical',
			x: 'right',
			y: 'center',
			feature: {
				mark: { show: true },
				dataView: { show: true, readOnly: false },
				restore: { show: true },
				saveAsImage: { show: true }
			}
		},
		roamController: {
			show: true,
			x: 'right',
			mapTypeControl: {
				'china': true
			}
		},
		series: [
			{
				name: '好友数量',
				type: 'map',
				mapType: 'china',
				roam: false,
				itemStyle: {
					normal: { label: { show: true } },
					emphasis: { label: { show: true } }
				},
				data: citys,
			}
		]
	};;
	// myChart.setOption(option, true);
	if (option && typeof option === "object") {
		myChart.setOption(option, true);
	}   
}



// 好友性别饼图
function update_sex(sex_data) {
	var sex_echartsPie;
	//总人数
	var people_count = sex_data['female'] + sex_data['secrecy'] + sex_data['male'];
	console.log(sex_data);
	var json = [{
		value: sex_data['female'] / people_count * 100,
		name: '女'
	},
	{
		value: sex_data['secrecy'] / people_count * 100,
		name: '保密'
	},
	{
		value: sex_data['male'] / people_count * 100,
		name: '男'
	}
	];
	var count = parseFloat("{c}")
	var option = {
		title: {
			text: '好友性别分析',
			subtext: '小i机器人',
			x: 'center'
		},
		tooltip: {
			trigger: 'item',
			formatter: "{a} <br/>{b} : {c}%"
		},
		legend: {
			orient: 'vertical',
			x: 'left',
			data: ['女', '保密', '男']
		},
		toolbox: {
			show: true,
			feature: {
				mark: {
					show: true
				},
				dataView: {
					show: true,
					readOnly: false
				},
				magicType: {
					show: true,
					type: ['pie', 'funnel'],
					option: {
						funnel: {
							x: '25%',
							width: '50%',
							funnelAlign: 'left',
							max: 1548
						}
					}
				},
				saveAsImage: {
					show: true
				}
			}
		},
		calculable: true,
		series: [{
			name: '性别比例',
			type: 'pie',
			radius: ['40%', '70%'], //饼图的半径大小
			center: ['50%', '60%'], //饼图的位置
			data: json
		}]
	};

	sex_echartsPie = echarts.init(document.getElementById('sex_echartsPie'));
	sex_echartsPie.setOption(option);
}


// 好友头像分析饼图
function update_avatar() {
	var echartsPie;
	var json = [{
		value: 30,
		name: '人脸'
	},
	{
		value: 26,
		name: '其他'
	},
	];
	var option = {
		title: {
			text: '人脸头像分析',
			subtext: '小i机器人',
			x: 'center'
		},
		tooltip: {
			trigger: 'item',
			formatter: "{a} <br/>{b} : {c} %"
		},
		legend: {
			orient: 'vertical',
			x: 'left',
			data: ['人脸', '其他']
		},
		toolbox: {
			show: true,
			feature: {
				mark: {
					show: true
				},
				dataView: {
					show: true,
					readOnly: false
				},
				magicType: {
					show: true,
					type: ['pie', 'funnel'],
					option: {
						funnel: {
							x: '25%',
							width: '50%',
							funnelAlign: 'left',
							max: 1548
						}
					}
				},
				// restore : {show: true},
				saveAsImage: {
					show: true
				}
			}
		},
		calculable: true,
		series: [{
			name: '',
			type: 'pie',
			radius: ['40%', '70%'], //饼图的半径大小
			center: ['50%', '60%'], //饼图的位置
			data: json
		}]
	};

	avatar_echartsPie = echarts.init(document.getElementById('avatar_echartsPie'));
	avatar_echartsPie.setOption(option);
}

// 基于好友签名信息的情感分析饼状图
function update_signature() {
	// 基于准备好的dom，初始化echarts实例
	var signature_echartsPie = echarts.init(document.getElementById('signature_echartsPie'));
	// 指定图表的配置项和数据
	signature_echartsPie.setOption({
		color: ['#06a45f'],
		width: "90%",
		title: {
			text: '基于好友签名信息，情感判断分析',
			subtext: 'Rainbow bar example'
		},
		/* 鼠标悬浮显示数据 */
		tooltip: {
			trigger: 'axis',
			axisPointer: { // 坐标轴指示器，坐标轴触发有效
				type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
			}
		},
		xAxis: {
			data: ['负面消极', '中性', '正面积极']
		},
		// 显示工具菜单
		toolbox: {
			show: true,
			feature: {
				dataView: {
					show: true,
					readOnly: false
				},
				saveAsImage: {
					show: true
				}
			}
		},
		yAxis: {},
		series: [{
			// 指定柱子的宽度
			barWidth: '20%',
			type: 'bar',
			// 指定柱子的数据
			data: ["1", "2", "5"],
			label: {
				normal: {
					show: true,
					// 数据在柱子头部显示
					position: 'top',
					textStyle: {
						color: '#5475c7',
						fontSize: 16,
					}
				}
			},

		}]
	});
}