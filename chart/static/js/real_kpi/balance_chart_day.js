var CHART_HEIGHT = 380;  //图表默认高度
var CHART_VER_BAR_HEIGHT = 50;  //图表垂直柱状图高度

$(function () {
    console.log("balance_chart_today...");
    load_hor_chart('balance_chart_day', "hor_Xdate_Litype", 30)


});

//20161024: updated by zhangyang32
//function: 
function load_hor_chart(chart_div, chart_type, params) {
    var chart_dom = document.getElementById(chart_div);
    //设置容器ＤＯＭ的高度,这里直接设置正常容器为４００
    var my_height = CHART_HEIGHT;
    chart_dom.style.height = my_height.toString() + "px";

    var chart_ins = echarts.init(chart_dom, 'macarons');
    // var chart_ins = echarts.init(chart_dom,'dark');
    chart_ins.showLoading();
    chart_ins.resize();

    ndays = params
    x_axis_label = []
    for (var i = ndays; i > 0; i--) {
        // var myDate = new Date();

        var today = new Date();
        var beforMilliseconds = today.getTime() - 1000 * 3600 * 24 * i;
        var myDate = new Date();
        myDate.setTime(beforMilliseconds);

        yyyy = myDate.getFullYear();
        mm = myDate.getMonth() + 1;
        mm = mm.length == 1 ? ("0" + mm) : mm;
        dd = myDate.getDate();
        dd = dd.length == 1 ? ("0" + dd) : dd;

        date = yyyy + "-" + mm + "-" + dd

        x_axis_label.push(date)
    }
    // console.log(x_axis_label)
    chart_ins.setOption({
        title: {
            text: '',
        },
        legend: {
            data: [],
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
            // triggerOn: 'click',
            triggerOn: 'mousemove',
            hideDelay: '100',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'line'        // 默认为直线，可选为：'line' | 'shadow'
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
            max: 500,
            type: 'value'
        },
        xAxis: {
            type: 'category',
            // min: '00:00',
            // max: '23:59',
            scale: true,
            boundaryGap: true,
            // splitNumber: 1440,
            data: x_axis_label,
            axisLabel: {
                // interval: function (index, value) {
                    // var myDate = new Date();
                    // h = myDate.getHours();
                    // m = myDate.getMinutes();
                    // if (index == 0 || index == 720 || index == 1439 || index == h * 60 + m)
                    // return true
                    // else
                    //     return false
                // }
            },
        },
        series: []
    }, true);
    refresh_today()
    chart_ins.hideLoading();


    //定时刷新
    refresh_interval = 30000
    var x_count = 0

    function refresh_today() {
        // console.log("1222222")
        // console.log("aaaaaaaaaaaaaaaaaaaaa")

        if (x_count >= 1440)
            clearInterval(timeTicket)
        x_count += 1

        $.getJSON("/server_itoms",
            {chart_type: "hor_balance_day", params: "test|" + ndays},
            function (result) {
                // console.log(chart_dom.style.height);
                chart_ins.setOption({
                    title: {
                        text: result.title_text,
                    },
                    legend: {
                        data: result.legend_data,
                    },
                    series: result.series
                }, false);
            });

    }

    // timeTicket = setInterval(refresh_today, refresh_interval);

    // var isInput = true;
    // window.onblur = function () {
    //     setTimeout(function () {
    //         if (true) {
    //             console.log("失去焦点！");
    //
    //             isInput = false;
    //             clearInterval(timeTicket)
    //         }
    //     }, 500);
    // }
    // window.onfocus = function () {
    //     if (!isInput) {
    //         console.log("获得焦点！");
    //         timeTicket = setInterval(refresh_today, refresh_interval);
    //         isInput = true;
    //     }
    // }
}
