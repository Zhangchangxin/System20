
## 新版本计划（v2.4）
目标： 改善视觉效果
1. 增加页面、对话框弹出动画
1. 右侧滚动条在顶部导航条之下
1. 左侧导航条菜单项点击区域受到文本长短影响

## 知识点

## 想一想
1. 为什么提出`dialog-background`的样式类？
1. 对比学生信息对话框和确认对话框两者实现思路的区别？确认对话框思路在实现上有那些改进？
1. 下面这两段程序有什么不同，效果和原理是什么？

第一段
```js
onOk: () => {
    (async () => {
        let response = await fetch(`/api/student/${item.stu_sn}`, {
            method: "DELETE",
        });
        
        ....

        renderList();
    })();
},
```

第二段
```js
onOk: () => {
    (async () => {
        let response = await fetch(`/api/student/${item.stu_sn}`, {
            method: "DELETE",
        });
        ....
    })();

    renderList();

},
```
<th class="col-cou_no">课程编号</th>


        tdEl = document.createElement("td");
        tdEl.innerText = item.cou_no;
        tdEl.className = "col-cou_no";
        trEl.append(tdEl);