
    // 调整页面水平居中
    function resetContentPos(){
       var div = document.getElementById("container"); // 获取主容器
       var allWidth = document.body.clientWidth;  // 浏览器的宽度
       var n = parseInt(allWidth / 420);  // 按浏览器的宽度计算，能显示几个视频
       var contentWidth = n * 420; // 几个视频加起来的总宽度
       div.style.marginLeft = (allWidth-contentWidth)/2+"px"; // 主容器往右移动一般的剩余宽度，对进行居中
    }
    (function(){
        resetContentPos(); // 调整页面水平居中
    })();
    window.onresize = function(){
        resetContentPos(); // 调整页面水平居中
    }
