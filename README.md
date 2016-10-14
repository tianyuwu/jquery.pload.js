#[pload]pushstate+load实现无刷新分页

### 为什么要使用`pload`
- `pload`使用load来更新页面的数据，然后通过pushstate修改地址栏的url，使得页面数据和对应的url一致，实现了页面无刷新更新数据，拥有单页应用的体验。
- 在传统get请求翻页的模式下，后端代码可以不用做任何修改，快速切换为无刷新。

### 技术概览
#### HTML5 History API
HTML5在History里增加了pushState方法，这个方法会将当前的url添加到历史记录中，然后修改当前url为新url。当然这个方法只会修改地址栏的Url显示，但并不会发出任何请求。因此我们可以利用这个方法结合ajax实现单页面应用SPA，就是PushState+Ajax，人称Pjax。
- pushState：
```
history.pushState(state, title, url)
```
**state:** 可以放任意你想放的数据，它将附加到新url上，作为该页面信息的一个补充。
**title:** document.title。
**url:** 新url，也就是你要显示在地址栏上的url。
- replaceState
```
history.replaceState(state, title, url)
```
replaceState方法与pushState大同小异，区别只在于pushState会将当前url添加到历史记录，之后再修改url，而replaceState只是修改url，不添加历史记录。
- onpopstate
```
window.onpopstate
```
一般来说，每当url变动时，popstate事件都会被触发。但若是调用pushState来修改url，该事件则不会触发，因此，我们可以把它用作浏览器的前进后退事件。该事件有一个参数，就是上文pushState方法的第一个参数state。

#### jQuery.load()
jquery的load() 方法通过 AJAX 请求从服务器加载数据，并把返回的数据放置到指定的元素中。[查看ajax_load文档](http://www.w3school.com.cn/jquery/ajax_load.asp)
```
load(url,data,function(response,status,xhr))
```

### 快速入门
pload和jquery的其他插件使用方式一致，页面引入再调用就好了：

**sept1: pload依赖于jQuery,所以首先需要保证页面中加载了Jquery,然后引入jquery.pload.js**
```
<script src="http://cdn.bootcss.com/jquery/1.12.4/jquery.js"></script>
<script src="jquery.pload.js"></script>
```
**sept2: 对页码标签进行初始化**
```
$('a').pload({
    container:'#pload-container',
    start:function(){
        $(".loading").show();
    },
    onSuccess:function(){
        $(".loading").hide();
    }
});
```
主要的几个参数：

`a`:页码标签

`container`: 需要替换内容的容器元素

`url`: 需要跳转的地址，如果标签是a标签，url会自动选择href属性的value值

`start`: 当加载开始时的回调函数，可以用于开启加载动画，可选

`onSuccess`: 当加载完成成功时的回调函数，可以用于关闭加载动画，可选


下面是一个完整的DEMO，[点击查看示例](http://www.tyhub.com/pload)
```
<!DOCTYPE html>
<html>
<head>
    <!-- styles, scripts, etc -->
    <style type="text/css">
        .loading{
            display: none;
        }
    </style>
</head>
<body>
<h1>pload--pushstate+load实现无刷新分页</h1>
<div class="loading">加载中...</div>
<div class="container" id="pload-container">
    <p>这是第{{p}}页</p>
    Go to <a href="/?p={{p+1}}">next page</a>.
    <span style="cursor: pointer">跳到第三页</span>
</div>

<script src="http://cdn.bootcss.com/jquery/1.12.4/jquery.js"></script>
<script src="jquery.pload.js"></script>

<script>
    $('#pload-container a').pload({
        container:'#pload-container',
        start:function(){
            $(".loading").show();
        },
        onSuccess:function(){
            $(".loading").hide();
        }
    });

    $('span').pload({container:'#pload-container', url:'/?p=3'})
</script>

</body>
</html>
```
该html需要一个server，笔者选取的Python的tornado框架做为后端的服务器，大体就是渲染该页面，并将当前页码传入