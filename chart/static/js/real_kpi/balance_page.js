var CHART_HEIGHT = 380;  //图表默认高度
var CHART_VER_BAR_HEIGHT = 50;  //图表垂直柱状图高度

$(function () {
    $('#balance_page').on('click', '.weui_navbar_item', function () {
        $(this).addClass('weui_bar_item_on').siblings('.weui_bar_item_on').removeClass('weui_bar_item_on');
    });

    $("#balance_tab_today").on("tap", function () {
        console.log('today....');
        $("#balance_chart").load("/static/html/real_kpi/balance_chart_today.html",
            function (responseTxt, statusTxt, xhr) {
                if (statusTxt == "success") {
                    // console.log("External content loaded successfully!");
                }
                if (statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText);
            });
    });
    $("#balance_tab_day").on("tap", function () {
        console.log('day....');
        $("#balance_chart").load("/static/html/real_kpi/balance_chart_day.html",
            function (responseTxt, statusTxt, xhr) {
                if (statusTxt == "success") {
                    // console.log("External content loaded successfully!");
                }
                if (statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText);
            });
    });
    $("#balance_tab_month").on("tap", function () {
        console.log('month....');
        $("#balance_chart").load("/static/html/real_kpi/balance_chart_month.html",
            function (responseTxt, statusTxt, xhr) {
                if (statusTxt == "success") {
                    // console.log("External content loaded successfully!");
                }
                if (statusTxt == "error")
                    alert("Error: " + xhr.status + ": " + xhr.statusText);
            });
    });

    $("#balance_tab_today").trigger("tap");
});

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
    $.getJSON("/server_itoms",
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
