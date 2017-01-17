$(function () {
    // var curfile = $("#testp").text() + location.href;
    // $("#testp").text(curfile);

//defaut show itoms chart
//$("#page_main_content").load("/chart_itoms.html");

//$("#page_main_footer").load("/weui_tabbar.html");
    
    //增加底部导航选择效果
    $('#page_footer_load').on('click', '.weui_tabbar_item', function () {
        $(this).addClass('weui_bar_item_on').siblings('.weui_bar_item_on').removeClass('weui_bar_item_on');
    });

    $("#tabbar_itoms").on("tap", function () {
        // console.log('tabbar_itoms tap');
        $("#page_content_load").load("/static/html/itoms/chart_itoms.html", function (responseTxt, statusTxt, xhr) {
            if (statusTxt == "success") {
                // console.log("External content loaded successfully!");
            }
            if (statusTxt == "error")
                alert("Error: " + xhr.status + ": " + xhr.statusText);
        });
    });

    $("#tabbar_patrol").on("tap", function () {
        $("#page_content_load").load("/static/html/real_kpi/chart_itoms.html", function (responseTxt, statusTxt, xhr) {
            if (statusTxt == "success") {
                // console.log("External content loaded successfully!");
            }
            if (statusTxt == "error")
                alert("Error: " + xhr.status + ": " + xhr.statusText);
        });
    });

    $("#tabbar_suggest").on("tap", function () {
        // console.log('tabbar_patrol tap');
        alert("努力开发中,敬请期待...");
    });

    $("#tabbar_busi").on("tap", function () {
        // console.log('tabbar_patrol tap');
        alert("努力开发中,敬请期待...");
    });
    
    // $("#tabbar_patrol").trigger("tap");
    $("#tabbar_itoms").trigger("tap");
});


