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

        var movie_items = document.getElementsByClassName('movie'); // 获取所有class含有movie的项，即所有视频
        for(var i=0;i<movie_items.length;i++){ // 遍历视频
             movie_items[i].addEventListener('play',function(t){ // 绑定视频的播放事件
                  var filename = t.target.dataset.file; // 获取data-file的值
                  var xhr = new XMLHttpRequest();
                  xhr.open('GET','countMovie?name='+filename);
                  xhr.setRequestHeader('Content-Type', 'text/plain');
                  // 监听服务器响应事件
                  xhr.onreadystatechange = function(){
                      //响应完成，请求成功
                      if(xhr.readyState == 4 && xhr.status == 200){
                           console.log(xhr.responseText);
                      }
                  }
                  // 发送到服务器
                  xhr.send(null);
             })
        }
    })();
    window.onresize = function(){
        resetContentPos(); // 调整页面水平居中
    }
