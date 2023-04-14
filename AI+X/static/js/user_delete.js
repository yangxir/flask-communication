//confirmDelete 函数：

// 获取所有删除按钮元素
var deleteBtns = document.querySelectorAll(".btn-danger");

// 为每个删除按钮添加事件监听器
deleteBtns.forEach(function(deleteBtn) {
    deleteBtn.addEventListener('click', confirmDelete);
});

// 弹出确认删除对话框
function confirmDelete(event) {
    var target = event.target;
    var user_id = target.dataset.id;
    var username = target.dataset.username;
    var email = target.dataset.email;

    var message = "您确认要删除 " + username + "（邮箱：" + email + "） 吗？";
    if (confirm(message)) {
        // 向服务器发出 POST 请求
        fetch('/admin_user/delete/' + user_id, {
            method: 'POST',
        }).then(function() {
            // 重新载入页面
            location.reload();
        });
    }
}