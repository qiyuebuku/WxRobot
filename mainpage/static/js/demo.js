// update_circles();
// 性别
update_sex();
// 头像
update_avatar();
// 签名
update_signature();

function update_circles() {
	Circles.create({
		id: 'task-complete',
		radius: 75,
		value: 80,
		maxValue: 100,
		width: 8,
		text: function (value) {
			return value + '%';
		},
		colors: ['#eee', '#1D62F0'],
		duration: 400,
		wrpClass: 'circles-wrp',
		textClass: 'circles-text',
		styleWrapper: true,
		styleText: true
	})
}



$.notify({
	icon: 'la la-bell',
	title: 'Bootstrap notify',
	message: 'Turning standard Bootstrap alerts into "notify" like notifications',
}, {
	type: 'success',
	placement: {
		from: "bottom",
		align: "right"
	},
	time: 1000,
});

// monthlyChart

Chartist.Pie('#monthlyChart', {
	labels: ['50%', '20%', '30%'],
	series: [50, 20, 30]
}, {
	plugins: [
		Chartist.plugins.tooltip()
	]
});

// trafficChart
var chart = new Chartist.Line('#trafficChart', {
	labels: [1, 2, 3, 4, 5, 6, 7],
	series: [
		[5, 9, 7, 8, 5, 3, 5],
		[6, 9, 5, 10, 2, 3, 7],
		[2, 7, 4, 10, 7, 6, 2]
	]
}, {
	plugins: [
		Chartist.plugins.tooltip()
	],
	low: 0,
	height: "245px",
});

// salesChart
var dataSales = {
	labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
	series: [
		[5, 4, 3, 7, 5, 10, 3, 4, 8, 10, 6, 8],
		[3, 2, 9, 5, 4, 6, 4, 6, 7, 8, 7, 4]
	]
}

var optionChartSales = {
	plugins: [
		Chartist.plugins.tooltip()
	],
	seriesBarDistance: 10,
	axisX: {
		showGrid: false
	},
	height: "245px",
}

var responsiveChartSales = [
	['screen and (max-width: 640px)', {
		seriesBarDistance: 5,
		axisX: {
			labelInterpolationFnc: function (value) {
				return value[0];
			}
		}
	}]
];

Chartist.Bar('#salesChart', dataSales, optionChartSales, responsiveChartSales);

$(".mapcontainer").mapael({
	map: {
		name: "world_countries",
		zoom: {
			enabled: true,
			maxLevel: 10
		},
		defaultPlot: {
			attrs: {
				fill: "#004a9b",
				opacity: 0.6
			}
		},
		defaultArea: {
			attrs: {
				fill: "#e4e4e4",
				stroke: "#fafafa"
			},
			attrsHover: {
				fill: "#59d05d"
			},
			text: {
				attrs: {
					fill: "#505444"
				},
				attrsHover: {
					fill: "#000"
				}
			}
		}
	},
	areas: {
		// "department-56": {
		// 	text: {content: "Morbihan", attrs: {"font-size": 10}},
		// 	tooltip: {content: "<b>Morbihan</b> <br /> Bretagne"}
		// },
		"ID": {
			tooltip: {
				content: "<b>Indonesia</b> <br /> Tempat Lahir Beta"
			},
			attrs: {
				fill: "#59d05d"
			},
			attrsHover: {
				fill: "#59d05d"
			}
		},
		"RU": {
			tooltip: {
				content: "<b>Russia</b>"
			},
			attrs: {
				fill: "#59d05d"
			},
			attrsHover: {
				fill: "#59d05d"
			}
		},
		"US": {
			tooltip: {
				content: "<b>United State</b>"
			},
			attrs: {
				fill: "#59d05d"
			},
			attrsHover: {
				fill: "#59d05d"
			}
		},
		"AU": {
			tooltip: {
				content: "<b>Australia</b>"
			},
			attrs: {
				fill: "#59d05d"
			},
			attrsHover: {
				fill: "#59d05d"
			}
		}
	},
});


// 好友性别饼图
function update_sex() {
	var sex_echartsPie;
	var json = [{
			value: 30,
			name: '女'
		},
		{
			value: 26,
			name: '保密'
		},
		{
			value: 24,
			name: '男'
		}
	];
	var option = {
		title: {
			text: '好友性别分析',
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