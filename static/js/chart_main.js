$(function () {
    // var curfile = $("#testp").text() + location.href;
    // $("#testp").text(curfile);

//defaut show itoms chart
//$("#page_main_content").load("/chart_itoms.html");

//$("#page_main_footer").load("/weui_tabbar.html");

    $("#tabbar_itoms").on("tap", function () {
        // console.log('tabbar_itoms tap');
        $("#page_content_load").load("/chart_itoms.html", function (responseTxt, statusTxt, xhr) {
            if (statusTxt == "success") {
                // console.log("External content loaded successfully!");
            }
            if (statusTxt == "error")
                alert("Error: " + xhr.status + ": " + xhr.statusText);
        });
    });
    $("#tabbar_itoms").trigger("tap");

    $("#tabbar_patrol").on("tap", function () {
        // console.log('111111111111111111');
        alert("努力开发中,敬请期待...");
    });

    $("#tabbar_suggest").on("tap", function () {
        // console.log('tabbar_patrol tap');
        alert("努力开发中,敬请期待...");
    });

    $("#tabbar_busi").on("tap", function () {
        // console.log('tabbar_patrol tap');
        alert("努力开发中,敬请期待...");
    });
});


