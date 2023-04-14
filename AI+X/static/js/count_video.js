    // 获取视频元素
const videoPlayer = document.getElementById('video-player');

// 监听播放事件
videoPlayer.addEventListener('play', () => {
  // 发送AJAX请求到后端视图函数中，以增加观看数
  const xhr = new XMLHttpRequest();
  xhr.open('POST', `{{ url_for('learn.increase_watch_count', video_id=video.id) }}`);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send();
});
// 获取当前观看数的<span>元素
const watchCountSpan = document.getElementById('watch-count');

// 监听AJAX请求返回的结果
xhr.addEventListener('load', () => {
  // 解析JSON并更新观看数
  const data = JSON.parse(xhr.responseText);
  watchCountSpan.innerText = data.watch_count;
});
