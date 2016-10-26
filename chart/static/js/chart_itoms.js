var CHART_HEIGHT = 380;  //图表默认高度
var CHART_VER_BAR_HEIGHT = 50;  //图表垂直柱状图高度

$(function () {
    //通用图表设置模板，其余设置可在此基础上进行覆盖
    var com_option = {
        // backgroundColor: '#d9ead3',
        title: {
            text: "a"
        },
        legend: {
            data: ['a'],
            left: 'center',
            bottom: '3%'
        },
        grid: {
            show: true,
            left: '3%',
            right: '3%',
            bottom: '10%',
            containLabel: true,
            // shadowColor: '#224b13',
            // shadowBlur: 10
        },
        tooltip: {
            trigger: 'axis',
            triggerOn: 'click',
            hideDelay: '100',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            enterable: true,
        },
        toolbox: {
            show: true,
            itemSize: 20,
            feature: {
                // restore: {show: false},
                myReturn: {
                    show: true,
                    title: '返回',
                    //path是SVG图，我是从网上ｄｏｗｎ的
                    icon: 'path://M186.988,252.656H490v-15.312H186.988L265.53,47.056L0,245l265.53,197.944L186.988,252.656z M230.212,92.482L167.261,245  l62.951,152.517L25.629,245L230.212,92.482z',
                    onclick: function (a, b, c, d) {
                        //一共可以看到有４个参数
                        //a-可以得到当前option: a.option.title[0]['text'])
                        //b-可以得到当前Dom: ins=echarts.getInstanceByDom(b.getDom())
                        //c-可以得到当前自定义工具名字，即myReturn
                        //d-可以得到当前事件类型
                        // console.log("--------tool box func------");
                        var dom = b.getDom(); //对象可以打印出来，在控制台看变量的内部结构与值
                        // load_line_chart(dom.id, com_option, "line", "chg");
                        toolbox_return_btn(dom.id, com_option);
                    }
                },
                magicType: {show: true, type: ['stack', 'tiled', 'line', 'bar']},
            }
        },
        series: [{
            // name: 'a',
            type: 'line', //在载入数据后,改变此值,可以强制刷新数据,避免显示的bug
            // data: ['1'],
        }],
        yAxis: {
            // type: 'category',
            // data: ['1'],
            // boundaryGap: true,
            // splitNumber: 12
        },
        xAxis: {
            // type: 'value'
        },
    }

    console.log("enter chart_itoms.js ");
    load_hor_chart('itoms_chg_emgc', "hor_Xdate_Litype", "紧急变更")
    load_hor_chart('itoms_para_mod', "hor_Xdate_Litype", "参数修改")
    load_hor_chart('itoms_chg', "hor_Xdate_Litype", "变更工单")
    load_hor_bar_chart('itoms_xbank', com_option, "hor_bar", "Xbank事件工单");
});

//加载水平方向排列的柱状图,用于1级子图显示.
function load_hor_bar_chart(chart_div, com_option, chart_type, itoms_type) {
    var chart_dom = document.getElementById(chart_div);
    var chart_ins = echarts.init(chart_dom, 'macarons');
    // var chart_ins = echarts.init(chart_dom,'dark');
    chart_ins.showLoading();
    // console.log('4', new Date());
    $.getJSON("/ec/server_itoms",
        {chart_type: chart_type, itoms_type: itoms_type},
        function (result) {
            // console.log("iiiiiiiiiiiiiid");
            // console.log(chart_dom.style.height);
            //设置容器ＤＯＭ的高度,这里直接设置正常容器为４００
            var my_height = CHART_HEIGHT;
            chart_dom.style.height = my_height.toString() + "px";
            chart_ins.resize();
            // 填入数据
            chart_ins.setOption(com_option, true);
            //在setOption时需要原来就有模板，并且需要修改模板类型才能刷新．我的模板时line,因此需要更新为par．其他类型可以不用
            chart_ins.setOption({
                series: [{
                    type: 'bar',

                }]
            });
            chart_ins.setOption({
                title: {
                    text: result.title_text,
                },
                legend: {
                    data: result.legend_data,
                },
                yAxis: {
                    type: 'value'
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    splitNumber: 12,
                    data: result.xAxis_data,
                },
                series: result.series
            });
            chart_ins.hideLoading();

            //设置下钻
            chart_ins.on('click', function (params) {
                // console.log('===============');
                // console.log(params);
                // console.log(params.seriesName);  //系列名称如工单类型
                // console.log(params.name);        //系列坐标,如日期
                // console.log(params.dataIndex);
                // console.log(params.data);
                // console.log(params.dataType);
                // console.log(params.value);

                // chart_chg.showLoading();
                //下钻选定两个值：
                // params.seriesName=工单类型,是legend维；
                // params.name=日期，是横坐标维;
                if (chart_div == 'itoms_chg')
                    load_ver_bar_chart(chart_div, com_option, "ver_bar", params.seriesName, params.name);
                else if (chart_div == 'itoms_xbank')
                    load_geo_chart(chart_div, com_option, "geo", params.seriesName, params.name);
                else if (chart_div == 'itoms_chg_emgc')
                    load_pie_chart(chart_div, com_option, params.seriesName, params.name);
                // load_geo_chart(chart_div, com_option, "geo", "Xbank事件工单", '20160701');


            });
        });
}


//20161013: created by zhangyang32
//function: load生成垂直延伸的图表，如线，柱等; 通用函数
//chart_div: 画布控件
//chart_type: 说明显示一个什么样的报表，如:ver_Ysys_Lstatus 代表Ｙ轴为系统，legend为工单状态．需配合下一个参数才有意义
//params: 与chart_type匹配的参数列表,用"|"分隔. 如: "紧急变更|20160901"
function load_hor_chart(chart_div, chart_type, params) {
    var chart_dom = document.getElementById(chart_div);
    var chart_ins = echarts.init(chart_dom, 'macarons');
    // var chart_ins = echarts.init(chart_dom,'dark');
    chart_ins.showLoading();
    // console.log('4', new Date());
    $.getJSON("/ec/server_itoms",
        {chart_type: chart_type, params: params},
        function (result) {
            // console.log(result);
            // console.log(chart_dom.style.height);
            //设置容器ＤＯＭ的高度,这里直接设置正常容器为４００
            var my_height = CHART_HEIGHT;
            chart_dom.style.height = my_height.toString() + "px";
            chart_ins.resize();
            // 填入数据
            // chart_ins.setOption(com_option, true);
            //在setOption时需要原来就有模板，并且需要修改模板类型才能刷新．我的模板时line,因此需要更新为par．其他类型可以不用
            // chart_ins.setOption({
            //     series: [{
            //         type: 'bar',
            //
            //     }]
            // });

            chart_ins.setOption({
                title: {
                    text: result.title_text,
                },
                legend: {
                    data: result.legend_data,
                    left: 'center',
                    bottom: '3%'
                },
                grid: {
                    show: true,
                    left: '3%',
                    right: '3%',
                    bottom: '10%',
                    containLabel: true,
                    // shadowColor: '#224b13',
                    // shadowBlur: 10
                },
                tooltip: {
                    trigger: 'axis',
                    triggerOn: 'click',
                    hideDelay: '100',
                    axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    },
                    enterable: true,
                },
                toolbox: {
                    show: true,
                    itemSize: 20,
                    feature: {
                        // restore: {show: false},
                        myReturn: {
                            show: true,
                            title: '返回',
                            //path是SVG图，我是从网上ｄｏｗｎ的
                            icon: 'path://M186.988,252.656H490v-15.312H186.988L265.53,47.056L0,245l265.53,197.944L186.988,252.656z M230.212,92.482L167.261,245  l62.951,152.517L25.629,245L230.212,92.482z',
                            onclick: function (a, b, c, d) {
                                //一共可以看到有４个参数
                                //a-可以得到当前option: a.option.title[0]['text'])
                                //b-可以得到当前Dom: ins=echarts.getInstanceByDom(b.getDom())
                                //c-可以得到当前自定义工具名字，即myReturn
                                //d-可以得到当前事件类型
                                // console.log("--------tool box func------");
                                // var dom = b.getDom(); //对象可以打印出来，在控制台看变量的内部结构与值
                                // load_line_chart(dom.id, com_option, "line", "chg");
                                // toolbox_return_btn(dom.id, com_option);
                                if (chart_div == 'itoms_xbank')
                                    load_hor_bar_chart(chart_div, "hor_bar", "Xbank事件工单");
                                else
                                    load_hor_chart(chart_div, chart_type, params);
                            }
                        },
                        magicType: {show: true, type: ['stack', 'tiled', 'line', 'bar']},
                    }
                },
                yAxis: {
                    type: 'value'
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: true,
                    splitNumber: 12,
                    data: result.xAxis_data,
                },
                series: result.series
            });
            chart_ins.hideLoading();

            //设置下钻
            chart_ins.on('click', function (params) {
                // console.log('===============');
                // console.log(params);
                // console.log(params.seriesName);  //系列名称如工单类型
                // console.log(params.name);        //系列坐标,如日期
                // console.log(params.dataIndex);
                // console.log(params.data);
                // console.log(params.dataType);
                // console.log(params.value);

                // chart_chg.showLoading();
                //下钻选定两个值：
                // params.seriesName=工单类型,是legend维；
                // params.name=日期，是横坐标维;
                if (chart_div == 'itoms_chg') {
                    in_params = params.name + "|" + params.seriesName
                    load_ver_chart(chart_div, "ver_Ysys_Lstatus_by_date", in_params);
                }
                else if (chart_div == 'itoms_xbank')
                    load_geo_chart(chart_div, com_option, "geo", params.seriesName, params.name);
                else if (chart_div == 'itoms_chg_emgc') {
                    in_params = params.name + "|" + params.seriesName;
                    load_pie_chart(chart_div, "pie_LemgcReasons_by_date", in_params);
                }
                else if (chart_div == 'itoms_para_mod') {
                    in_params = params.name + "|" + params.seriesName;
                    load_pie_chart(chart_div, "pie_itoms_para_mod_w_date_type_Lreason", in_params);
                }
            });
        });
}

//加载垂直方向排列的柱状图,用于2级子图显示.
function load_ver_bar_chart(chart_div, com_option, chart_type, itoms_type, itoms_date) {
    var chart_dom = document.getElementById(chart_div);
    // var chart_ins = echarts.init(chart_dom,'dark');
    var chart_ins = echarts.init(chart_dom, 'macarons');
    chart_ins.showLoading();
    // console.log('4', new Date());
    $.getJSON("/ec/server_itoms",
        {chart_type: chart_type, itoms_type: itoms_type, itoms_date: itoms_date},
        function (result) {
            //根据返回的ｙ轴维度数量，设置容器ＤＯＭ的高度
            var my_height = result.yAxis_count * CHART_VER_BAR_HEIGHT;
            if (my_height < CHART_HEIGHT) my_height = CHART_HEIGHT;
            // console.log(chart_dom.id);
            chart_dom.style.height = my_height.toString() + "px";
            chart_ins.resize();
            // 填入数据
            chart_ins.setOption(com_option, true);
            chart_ins.setOption({
                title: {
                    text: result.title_text,
                    subtext: itoms_date + " 长按切换子系统状态",
                },
                legend: {
                    data: result.legend_data,
                },
                xAxis: {
                    type: 'value'
                },
                yAxis: {
                    type: 'category',
                    boundaryGap: true,
                    splitNumber: 12,
                    data: result.yAxis_data,
                },
                series: result.series
            });

            //增加超时设置,是为了在手机端click时,屏蔽掉鼠标按下操作
            var intervalTimer = null;
            chart_ins.on('click', function (param) {
                clearTimeout(intervalTimer); //取消上次延时未执行的方法
            });

            chart_ins.on('mousedown', function (param) {
                clearTimeout(intervalTimer); //取消上次延时未执行的方法
                intervalTimer = setTimeout(function () {
                    // console.log("----mousedown---------");
                    // console.log(param);
                    yAxis_name = param.name;
                    yAxis_index = param.dataIndex;
                    // mousedown 事件的处理,由于2级子图已经获取到数据,因此不必再访问服务端,在本地处理即可
                    if (chart_div == 'itoms_chg')
                        load_pie_chart_local(chart_div, com_option, chart_type, itoms_type, itoms_date, result, yAxis_index);
                    else if (chart_div == 'itoms_chg_emgc')
                        load_pie_chart(chart_div, com_option, itoms_type, itoms_date);
                }, 1000);
            });

            chart_ins.hideLoading();
        });
}

//20161010: created by zhangyang32
//function: load生成垂直延伸的图表，如线，柱等; 通用函数
//chart_div: 画布控件
//chart_type: 说明显示一个什么样的报表，如:ver_Ysys_Lstatus 代表Ｙ轴为系统，legend为工单状态．需配合下一个参数才有意义
//params: 与chart_type匹配的参数列表,用"|"分隔. 如: "紧急变更|20160901"
function load_ver_chart(chart_div, chart_type, params) {
    var chart_dom = document.getElementById(chart_div);
    // var chart_ins = echarts.init(chart_dom,'dark');
    var chart_ins = echarts.init(chart_dom, 'macarons');
    chart_ins.showLoading();
    $.getJSON("/ec/server_itoms",
        {chart_type: chart_type, params: params},
        function (result) {
            //根据返回的ｙ轴维度数量，设置容器ＤＯＭ的高度
            var my_height = result.yAxis_count * CHART_VER_BAR_HEIGHT;
            if (my_height < CHART_HEIGHT) my_height = CHART_HEIGHT;
            // console.log(chart_dom.id);
            chart_dom.style.height = my_height.toString() + "px";
            chart_ins.resize();
            // 填入数据
            // chart_ins.setOption(com_option, true);
            chart_ins.setOption({
                title: {
                    text: result.title_text,
                    subtext: "长按图表项可进行切换",
                },
                legend: {
                    data: result.legend_data,
                    left: 'center',
                    bottom: '3%'
                },
                grid: {
                    show: true,
                    left: '3%',
                    right: '3%',
                    bottom: '10%',
                    containLabel: true,
                    // shadowColor: '#224b13',
                    // shadowBlur: 10
                },
                tooltip: {
                    trigger: 'axis',
                    triggerOn: 'click',
                    hideDelay: '100',
                    axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    },
                    enterable: true,
                },
                toolbox: {
                    show: true,
                    itemSize: 20,
                    feature: {
                        // restore: {show: false},
                        myReturn: {
                            show: true,
                            title: '返回',
                            //path是SVG图，我是从网上ｄｏｗｎ的
                            icon: 'path://M186.988,252.656H490v-15.312H186.988L265.53,47.056L0,245l265.53,197.944L186.988,252.656z M230.212,92.482L167.261,245  l62.951,152.517L25.629,245L230.212,92.482z',
                            onclick: function (a, b, c, d) {
                                //一共可以看到有４个参数
                                //a-可以得到当前option: a.option.title[0]['text'])
                                //b-可以得到当前Dom: ins=echarts.getInstanceByDom(b.getDom())
                                //c-可以得到当前自定义工具名字，即myReturn
                                //d-可以得到当前事件类型
                                // console.log("--------tool box func------");
                                // var dom = b.getDom(); //对象可以打印出来，在控制台看变量的内部结构与值
                                // load_line_chart(dom.id, com_option, "line", "chg");
                                // toolbox_return_btn(dom.id, com_option);
                                if (chart_div == 'itoms_xbank')
                                    load_hor_bar_chart(chart_div, "hor_bar", "Xbank事件工单");
                                else if (chart_div == 'itoms_chg')
                                    load_hor_chart(chart_div, "hor_Xdate_Litype", "变更工单")
                                else if (chart_div == 'itoms_chg_emgc')
                                    load_hor_chart(chart_div, "hor_Xdate_Litype", "紧急变更")
                                else if (chart_div == 'itoms_para_mod')
                                    load_hor_chart(chart_div, "hor_Xdate_Litype", "参数修改")
                            }
                        },
                        magicType: {show: true, type: ['stack', 'tiled', 'line', 'bar']},
                    }
                },
                xAxis: {
                    type: 'value'
                },
                yAxis: {
                    type: 'category',
                    boundaryGap: true,
                    splitNumber: 12,
                    data: result.yAxis_data,
                },
                series: result.series
            });

            //增加超时设置,是为了在手机端click时,屏蔽掉鼠标按下操作
            var intervalTimer = null;
            chart_ins.on('click', function (param) {
                clearTimeout(intervalTimer); //取消上次延时未执行的方法
            });

            chart_ins.on('mousedown', function (param) {
                clearTimeout(intervalTimer); //取消上次延时未执行的方法
                intervalTimer = setTimeout(function () {
                    // console.log("----mousedown---------");
                    // console.log(param);
                    yAxis_name = param.name;
                    yAxis_index = param.dataIndex;
                    // mousedown 事件的处理,由于2级子图已经获取到数据,因此不必再访问服务端,在本地处理即可
                    if (chart_div == 'itoms_chg')
                        load_pie_chart(chart_div, "pie_itoms_chg_where_data_type_sys_Lstatus", params.split("|")[0] + "|" + params.split("|")[1] + "|" + param.name);
                    else if (chart_div == 'itoms_chg_emgc')
                        load_pie_chart(chart_div, "pie_LemgcReasons_by_date", params.split("|")[0] + "|" + params.split("|")[1]);
                    else if (chart_div == 'itoms_para_mod')
                        load_pie_chart(chart_div, "pie_itoms_para_mod_w_date_type_Lreason", params.split("|")[0] + "|" + params.split("|")[1]);
                }, 1000);
            });

            chart_ins.hideLoading();
        });
}


//2016-07-22加载地图数据. 用于2级子图显示.
function load_geo_chart(chart_div, com_option, chart_type, itoms_type, itoms_date) {
    var chart_dom = document.getElementById(chart_div);
    var chart_ins = echarts.init(chart_dom, 'macarons');
    // var chart_ins = echarts.init(chart_dom,'dark');
    chart_ins.showLoading();
    var curIndx = 0;
    var mapType = [
        'china',
        // 23个省
        '广东', '青海', '四川', '海南', '陕西',
        '甘肃', '云南', '湖南', '湖北', '黑龙江',
        '贵州', '山东', '江西', '河南', '河北',
        '山西', '安徽', '福建', '浙江', '江苏',
        '吉林', '辽宁', '台湾',
        // 5个自治区
        '新疆', '广西', '宁夏', '内蒙古', '西藏',
        // 4个直辖市
        '北京', '天津', '上海', '重庆',
        // 2个特别行政区
        '香港', '澳门'
    ];
    // console.log('4', new Date());
    $.getJSON("/ec/server_itoms",
        {chart_type: chart_type, itoms_type: itoms_type, itoms_date: itoms_date},
        function (result) {
            //设置容器ＤＯＭ的高度,这里直接设置正常容器为４００
            // echarts.registerMap('china', result);
            var my_height = CHART_HEIGHT;
            chart_dom.style.height = my_height.toString() + "px";
            chart_ins.resize();
            // 填入数据
            // chart_ins.setOption(com_option, true);
            //在setOption时需要原来就有模板，并且需要修改模板类型才能刷新．我的模板时line,因此需要更新为par．其他类型可以不用
            // console.log(result);
            geo_option = {
                // backgroundColor: '#d9ead3',
                legend: {
                    data: ['当天', '当月', '月TOP'],
                    // left: 'center',
                    left: 'right',
                    // bottom: '3%'
                    top: 'bottom',
                    selectedMode: 'single',
                    selected: {'当天': true}
                },
                tooltip: {
                    trigger: 'itom',
                    triggerOn: 'click',
                    hideDelay: '100',
                    enterable: true,
                    formatter: function (params) {
                        // console.log("------111111112-------------");
                        // console.log(params);
                        if (params.value.length > 1)
                            return params.seriesName + "<br />" + params.name + ":" + params.value[2]
                        else {
                            // return '<a href="/test1.html">link</a>'
                            //     +params.seriesName + "<br />" + params.name + ":" + params.value
                            return params.seriesName + "<br />" + params.name + ":" + params.value
                        }
                    },
                },
                toolbox: {
                    show: true,
                    itemSize: 20,
                    feature: {
                        // restore: {show: false},
                        myReturn: {
                            show: true,
                            title: '返回',
                            //path是SVG图，我是从网上ｄｏｗｎ的
                            icon: 'path://M186.988,252.656H490v-15.312H186.988L265.53,47.056L0,245l265.53,197.944L186.988,252.656z M230.212,92.482L167.261,245  l62.951,152.517L25.629,245L230.212,92.482z',
                            onclick: function (a, b, c, d) {
                                //一共可以看到有４个参数
                                //a-可以得到当前option: a.option.title[0]['text'])
                                //b-可以得到当前Dom: ins=echarts.getInstanceByDom(b.getDom())
                                //c-可以得到当前自定义工具名字，即myReturn
                                //d-可以得到当前事件类型
                                // console.log("--------tool box func------");
                                var dom = b.getDom(); //对象可以打印出来，在控制台看变量的内部结构与值
                                // load_line_chart(dom.id, com_option, "line", "chg");
                                toolbox_return_btn(dom.id, com_option);
                            }
                        },
                        // myToggleMap: {
                        //     show: true,
                        //     title: '省级地图切换',
                        //     //path是SVG图，我是从网上ｄｏｗｎ的
                        //     icon: 'path://M186.988,252.656H490v-15.312H186.988L265.53,47.056L0,245l265.53,197.944L186.988,252.656z M230.212,92.482L167.261,245  l62.951,152.517L25.629,245L230.212,92.482z',
                        //     onclick: function (a, b, c, d) {
                        //         //一共可以看到有４个参数
                        //         //a-可以得到当前option: a.option.title[0]['text'])
                        //         //b-可以得到当前Dom: ins=echarts.getInstanceByDom(b.getDom())
                        //         //c-可以得到当前自定义工具名字，即myReturn
                        //         //d-可以得到当前事件类型
                        //         // console.log("--------tool box func------");
                        //         // console.log(a)
                        //         // console.log(b)
                        //         // console.log(c)
                        //         // console.log(d)
                        //         // var dom = b.getDom(); //对象可以打印出来，在控制台看变量的内部结构与值
                        //         // load_line_chart(dom.id, com_option, "line", "chg");
                        //         // toolbox_return_btn(dom.id, com_option);
                        //         chart_ins = echarts.getInstanceByDom(b.getDom())
                        //         chart_ins.setOption(geo_option, true);
                        //         if (geo_option.series[1].mapType != 'china') {
                        //             // geo_option.series[0].mapType = 'china';
                        //             // geo_option.series[1].mapType = 'china';
                        //         }
                        //     }
                        // },
                        magicType: {
                            show: false, type: ['stack', 'tiled', 'line', 'bar']
                        },
                    }
                },
                title: {
                    text: result.title_text,
                    subtext: itoms_date + " 长按切换省级地图",
                },
                visualMap: {
                    type: 'piecewise', // 定义为分段型 visualMap
                    min: result.visualMap_min_day,
                    max: result.visualMap_max_day,
                    // min: 0,
                    // max: 100,
                    left: 'left',
                    top: 'bottom',
                    color: ['#d94e5d', '#eac736', '#50a3ba'],
                    // text: ['高', '低'],           // 文本，默认为数值文本
                    calculable: true
                },
                geo: {
                    map: 'china',
                    // map: '四川',
                    label: {
                        normal: {
                            show: false
                        },
                        emphasis: {
                            show: true
                        }
                    },
                    selectedMode: 'single',
                },
                series: [
                    //map type,用于地图区域的展示
                    {
                        name: '当天',
                        type: 'map',
                        mapType: 'china',
                        selectedMode: 'single',
                        // mapType: '四川',
                        roam: false,
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        data: result.series_data_day,
                        // [
                        // {name: '西藏', value: 100},
                        // {name: '西安', value: 100},
                        // {name: '成都市', value: 100},
                        // ]
                    },
                    {
                        name: '当月',
                        type: 'map',
                        mapType: 'china',
                        selectedMode: 'single',
                        // mapType: '四川',
                        roam: false,
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        data: result.series_data_month,
                        // [
                        // {name: '西藏', value: 100},
                        // {name: '西安', value: 100},
                        // {name: '成都市', value: 100},
                        // ]
                    },
                    //scatter type,用于TOP N  的展示
                    {
                        name: '月TOP',
                        type: 'effectScatter',
                        coordinateSystem: 'geo',
                        // selectedMode: 'multiple',
                        // center: locations[1].coord,
                        // zoom: 4,
                        // roam:true,
                        showEffectOn: 'render',
                        rippleEffect: {
                            brushType: 'stroke'
                        },
                        hoverAnimation: true,
                        label: {
                            normal: {
                                formatter: '{b}',
                                position: 'right',
                                show: true
                            },
                            // emphasis: {
                            //     formatter: '+++{b}++',
                            //     position: 'right',
                            //     show: true
                            // }
                        },
                        itemStyle: {
                            normal: {
                                // color: '#f4e925',
                                shadowBlur: 10,
                                shadowColor: '#333'
                            }
                        },
                        zlevel: 1,
                        data: result.series_data_mtop,
                        // {name: '广东', selected: true},
                        // {name: '西安', value: 400},
                        // {name: '西安', value: [108.95,34.27, 500]},
                        symbolSize: function (val) {
                            return val[2] / 8;
                        },
                    },
                ]
            };

            //先定义,后使用
            chart_ins.on('legendselectchanged', function (params) {
                if (params.name == '当天') {
                    geo_option.visualMap.max = result.visualMap_max_day;
                    geo_option.visualMap.min = result.visualMap_min_day;
                    geo_option.legend.selected = {'当天': true};

                    // console.log(geo_option);
                    delete geo_option['geo'];   //需要清除TOP用到的地图数据,不然不同的legend互相干扰,省级地图时不要显示大地图
                    // chart_ins.dispatchAction('legendToggleSelect', '当天' );
                }
                else if (params.name == '当月') {
                    geo_option.visualMap.max = result.visualMap_max_month;
                    geo_option.visualMap.min = result.visualMap_min_month;
                    geo_option.legend.selected = {'当月': true};
                    delete geo_option['geo'];   //需要清除TOP用到的地图数据
                    // chart_ins.dispatchAction('legendToggleSelect', '当天' );
                }
                else if (params.name == '月TOP') {
                    geo_option.visualMap.max = result.visualMap_max_mtop;
                    geo_option.visualMap.min = result.visualMap_min_mtop;
                    geo_option.legend.selected = {'月TOP': true};
                    //恢复被清楚的GEO数据
                    geo_option.geo = {
                        map: 'china',
                        // map: '四川',
                        label: {
                            normal: {
                                show: false
                            },
                            emphasis: {
                                show: true
                            }
                        },
                        selectedMode: 'single',
                    };
                    // geo_option.tooltip = {
                    //     trigger: 'itom',
                    //     triggerOn: 'click',
                    //     hideDelay: '100',
                    //     enterable: true,
                    //     formatter: '{b}: {c}',
                    // }
                }
                // console.log("--------------")
                // console.log(geo_option);
                chart_ins.setOption(geo_option, true);
                // chart_ins.resize();
            });

            // 地图钻取功能,单机用自带的功能显示数量,长按钻取
            //

            //增加超时设置,是为了在手机端click时,屏蔽掉鼠标按下操作
            var intervalTimer = null;
            chart_ins.on('click', function (param) {
                clearTimeout(intervalTimer); //取消上次延时未执行的方法
            });

            chart_ins.on('mousedown', function (param) {
                // console.log(param);
                clearTimeout(intervalTimer); //取消上次延时未执行的方法
                intervalTimer = setTimeout(function () {
                    // click 事件的处理

                    var len = mapType.length;
                    var mt = mapType[curIndx % len];
                    if (mt == 'china') {
                        // 全国选择时指定到选中的省份
                        // var selected = param.selected;
                        var selected = param.name;
                        var selected_value = param.value;
                        if (selected_value >= 1) {
                            mt = selected;
                        }
                        //获取当前的地图省份索引
                        while (len--) {
                            if (mapType[len] == mt) {
                                curIndx = len;
                            }
                        }
                        // geo_option.tooltip.formatter = '滚轮切换省份或点击返回全国<br/>{b}';
                        // geo_option.series[0].label.normal = {"show": true};
                        // geo_option.series[1].label.normal = {"show": true};
                    }
                    else {
                        //如果在
                        curIndx = 0;
                        mt = 'china';
                        // geo_option.series[0].label.normal = {"show": false}; //大地图不显示地名
                        // geo_option.series[1].label.normal = {"show": false}; //大地图不显示地名
                        // geo_option.tooltip.formatter = '滚轮切换或点击进入该省<br/>{b}';
                    }
                    // console.log(geo_option);
                    // if geo_option.legend.selected==''
                    // console.log(geo_option.legend.selected);
                    var legend_name = ""
                    for (var i in geo_option.legend.selected) {
                        legend_name = i;
                        break;
                    }
                    // if (legend_name == "当天") {
                    //     geo_option.series[0].mapType = mt;
                    //     geo_option.series[1].mapType = mt;
                    // }
                    // else if (legend_name == "当月") {
                    geo_option.series[0].mapType = mt;
                    geo_option.series[1].mapType = mt;
                    // }
                    // geo_option.series[0].mapType = mt;
                    // geo_option.title.subtext = mt + ' （滚轮或点击切换）';
                    chart_ins.setOption(geo_option, true); //改到toolbox中进行触发
                }, 1000);
            });


            //触发一次lengend切换,删除geo数据
            chart_ins.setOption(geo_option);
            chart_ins.dispatchAction({
                type: 'legendToggleSelect',
                name: '当天'
            });
            chart_ins.hideLoading();
        });
}

//2016-07-25加载饼图数据. 用于3级子图显示.
function load_pie_chart_local(chart_div, com_option, chart_type, itoms_type, itoms_date, result, series_idx) {
    //某工单,某天,某类别(系统 or 地区)
    //使用verbarChart的数据,然后取一个系统出来即可.
    var chart_dom = document.getElementById(chart_div);
    var chart_ins = echarts.init(chart_dom, 'macarons');
    // var chart_ins = echarts.init(chart_dom,'dark');
    chart_ins.showLoading();
    // console.log('4', new Date());
    //设置容器ＤＯＭ的高度,这里直接设置正常容器为４００
    // echarts.registerMap('china', result);
    var my_height = CHART_HEIGHT;
    chart_dom.style.height = my_height.toString() + "px";
    chart_ins.resize();
    // 填入数据
    // chart_ins.setOption(com_option, true);
    //在setOption时需要原来就有模板，并且需要修改模板类型才能刷新．我的模板时line,因此需要更新为par．其他类型可以不用
    // console.log(result);
    // console.log("----pie-----");
    // console.log(result);

    var pie_series_data = [];
    var pie_legend_data = [];
    for (var i = 0; i < result.legend_data.length; i++) {
        //过滤掉值为0的维度
        if (result.series[i].data[series_idx] < 1)
            continue;
        pie_series_data.push(
            {
                "value": result.series[i].data[series_idx],
                "name": result.legend_data[i],
            }
        );
        pie_legend_data.push(result.legend_data[i]);
    }
    // console.log(pie_series_data);

    pie_option = {
        // backgroundColor: '#d9ead3',
        legend: {
            data: pie_legend_data,
            left: 'center',
            top: 'bottom',
        },
        tooltip: {
            trigger: 'itom',
            triggerOn: 'click',
            hideDelay: '100',
            enterable: true,
            formatter: function (params) {
                // console.log("------111111112-------------");
                // console.log(params);
                if (params.value.length > 1)
                    return params.seriesName + "<br />" + params.name + ":" + params.value[2] + " " + params.percent + "%"
                else {
                    // return '<a href="/test1.html">link</a>'
                    //     +params.seriesName + "<br />" + params.name + ":" + params.value
                    return params.seriesName + "<br />" + params.name + ":" + params.value + " " + params.percent + "%"
                }
            },
        },
        toolbox: {
            show: true,
            itemSize: 20,
            feature: {
                // restore: {show: false},
                myReturn: {
                    show: true,
                    title: '返回',
                    //path是SVG图，我是从网上ｄｏｗｎ的
                    icon: 'path://M186.988,252.656H490v-15.312H186.988L265.53,47.056L0,245l265.53,197.944L186.988,252.656z M230.212,92.482L167.261,245  l62.951,152.517L25.629,245L230.212,92.482z',
                    onclick: function (a, b, c, d) {
                        //一共可以看到有４个参数
                        //a-可以得到当前option: a.option.title[0]['text'])
                        //b-可以得到当前Dom: ins=echarts.getInstanceByDom(b.getDom())
                        //c-可以得到当前自定义工具名字，即myReturn
                        //d-可以得到当前事件类型
                        // console.log("--------tool box func------");
                        var dom = b.getDom(); //对象可以打印出来，在控制台看变量的内部结构与值
                        // load_line_chart(dom.id, com_option, "line", "chg");
                        toolbox_return_btn(dom.id, com_option);
                    }
                },
                magicType: {
                    show: false, type: ['stack', 'tiled', 'line', 'bar']
                },
            }
        },
        title: {
            // text: result.title_text,
            text: result.yAxis_data[series_idx] + "工单状态",
            subtext: itoms_date + " 长按切换子系统状态",
            // subtext: itoms_date + " 长按切换省级地图",
        },
        series: [
            {
                name: "工单状态",
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: pie_series_data.sort(function (a, b) {
                    return a.value - b.value
                }),
                // roseType: 'angle',
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };


    //增加超时设置,是为了在手机端click时,屏蔽掉鼠标按下操作
    var intervalTimer = null;
    chart_ins.on('click', function (param) {
        clearTimeout(intervalTimer); //取消上次延时未执行的方法
    });

    chart_ins.on('mousedown', function (param) {
        // console.log(param);
        clearTimeout(intervalTimer); //取消上次延时未执行的方法
        intervalTimer = setTimeout(function () {
            // click 事件的处理
            // console.log(param);
            load_ver_bar_chart(chart_div, com_option, chart_type, itoms_type, itoms_date);
        }, 1000);
    });

    chart_ins.setOption(pie_option, true);
    chart_ins.hideLoading();
}

//20161010: created by zhangyang32
//function: load生成饼图
//chart_div: 画布控件
//chart_type: 说明显示一个什么样的报表，如:pie_LemgcReasons_by_date 代表Ｙ轴为系统，legend为工单状态．需配合后面的传入参数才有意义
//params: 与chart_type匹配的参数列表,用"|"分隔. 如: "紧急变更|20160901"
function load_pie_chart(chart_div, chart_type, params) {
    var chart_dom = document.getElementById(chart_div);
    var chart_ins = echarts.init(chart_dom, 'macarons');
    chart_ins.showLoading();

    //设置容器ＤＯＭ的高度,这里直接设置正常容器为４００
    var my_height = CHART_HEIGHT;
    chart_dom.style.height = my_height.toString() + "px";
    chart_ins.resize();

    // 填入数据,当前是itoms的前端，对应访问itoms的后端数据服务,这里时按业务逻辑来划分模块
    $.getJSON("/ec/server_itoms",
        {chart_type: chart_type, params: params},
        function (result) {
            // console.log('==in=============');
            // console.log(result);
            pie_option = {
                // backgroundColor: '#d9ead3',
                legend: {
                    data: result.legend_data,
                    left: 'center',
                    top: 'bottom',
                },
                tooltip: {
                    trigger: 'itom',
                    triggerOn: 'click',
                    hideDelay: '100',
                    enterable: true,
                    formatter: function (params) {
                        // console.log("------111111112-------------");
                        // console.log(params);
                        if (params.value.length > 1)
                            return params.seriesName + "<br />" + params.name + ":" + params.value[2] + "(" + params.percent + "%)"
                        else {
                            // return '<a href="/test1.html">link</a>'
                            //     +params.seriesName + "<br />" + params.name + ":" + params.value
                            return params.seriesName + "<br />" + params.name + ":" + params.value + "(" + params.percent + "%)"
                        }
                    },
                },
                toolbox: {
                    show: true,
                    itemSize: 20,
                    feature: {
                        // restore: {show: false},
                        myReturn: {
                            show: true,
                            title: '返回',
                            //path是SVG图，我是从网上ｄｏｗｎ的
                            icon: 'path://M186.988,252.656H490v-15.312H186.988L265.53,47.056L0,245l265.53,197.944L186.988,252.656z M230.212,92.482L167.261,245  l62.951,152.517L25.629,245L230.212,92.482z',
                            onclick: function (a, b, c, d) {
                                //一共可以看到有４个参数
                                //a-可以得到当前option: a.option.title[0]['text'])
                                //b-可以得到当前Dom: ins=echarts.getInstanceByDom(b.getDom())
                                //c-可以得到当前自定义工具名字，即myReturn
                                //d-可以得到当前事件类型
                                // console.log("--------tool box func------");
                                // var dom = b.getDom(); //对象可以打印出来，在控制台看变量的内部结构与值
                                // load_line_chart(dom.id, com_option, "line", "chg");
                                // toolbox_return_btn_to_origin(dom.id);
                                if (chart_div == 'itoms_xbank')
                                    load_hor_bar_chart(chart_div, "hor_bar", "Xbank事件工单");
                                else if (chart_div == 'itoms_chg')
                                    load_hor_chart(chart_div, "hor_Xdate_Litype", "变更工单")
                                else if (chart_div == 'itoms_chg_emgc')
                                    load_hor_chart(chart_div, "hor_Xdate_Litype", "紧急变更")
                                else if (chart_div == 'itoms_para_mod')
                                    load_hor_chart(chart_div, "hor_Xdate_Litype", "参数修改")
                            }
                        },
                        magicType: {
                            show: false, type: ['stack', 'tiled', 'line', 'bar']
                        },
                    }
                },
                title: {
                    text: result.title_text,
                    subtext: "长按图表项可进行切换",
                },
                series: result.series
            };

            chart_ins.setOption(pie_option, true);
            chart_ins.hideLoading();

            //增加超时设置,是为了在手机端click时,屏蔽掉鼠标按下操作
            var intervalTimer = null;
            chart_ins.on('click', function (param) {
                clearTimeout(intervalTimer); //取消上次延时未执行的方法
            });

            chart_ins.on('mousedown', function (param) {
                // chart_ins.on('dblclick', function (param) {
                // console.log(params);
                // console.log(params.split("|")[1]);

                clearTimeout(intervalTimer); //取消上次延时未执行的方法
                intervalTimer = setTimeout(function () {
                    //     click 事件的处理
                    // console.log(param);
                    // load_ver_bar_chart(chart_div, com_option, "ver_bar", itoms_type, itoms_date);
                    if (chart_div == 'itoms_chg_emgc') {
                        in_params = params.split("|")[0] + "|" + params.split("|")[1] + "|" + param.name
                        load_ver_chart(chart_div, "ver_Ysys_Lstatus_by_date_reason", in_params);
                    }
                    else if (chart_div == 'itoms_chg') {
                        in_params = params.split("|")[0] + "|" + params.split("|")[1]
                        load_ver_chart(chart_div, "ver_Ysys_Lstatus_by_date", in_params)
                    }
                    else if (chart_div == 'itoms_para_mod') {
                        in_params = params.split("|")[0] + "|" + params.split("|")[1] + "|" + param.name
                        load_ver_chart(chart_div, "ver_itoms_para_mod_w_date_type_reason_Lstatus_Ysys", in_params);
                    }
                }, 1000);
                // load_ver_bar_chart(chart_div, com_option, "ver_bar", itoms_type, itoms_date);
            });
        }
    )
}

//echart 工具箱,自定义返回函数
function toolbox_return_btn(chart_div, com_option) {
    // console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>');
    // console.log(chart_div);
    if (chart_div == 'itoms_chg')
        load_hor_bar_chart('itoms_chg', com_option, "hor_bar", "变更工单");
    else if (chart_div == 'itoms_xbank')
        load_hor_bar_chart('itoms_xbank', com_option, "hor_bar", "Xbank事件工单");
    else if (chart_div == 'itoms_chg_emgc')
        load_hor_bar_chart('itoms_chg_emgc', com_option, "hor_bar", "紧急变更");
}

