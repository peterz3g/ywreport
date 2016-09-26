$(function () {
$("#page_footer_load").load("/weui_tabbar.html");
console.log(">>>in weui_tabbar.js")


$(document).on("pageinit",function(event){
  alert("触发 pageinit 事件！")
  $("#page_footer_load").load("/weui_tabbar.html");
});

$("#tabbar_itoms").on("tap",function(){
//  $(this).hide();
    window.location.href="chart_itoms.html";
});

});


