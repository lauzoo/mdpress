##Markdown Editor By Vasquez

###项目介绍

这个项目是基于[Editor.md](https://pandao.github.io/editor.md/examples/index.html "Editor.md")创建的，主要在原有的基础上增加了保存功能，这样的话，你就可以直接在编辑完之后保存啦～～

###依赖

保存查看功能需要：tidy扩展
不需要保存查看功能无特殊依赖。

因为我们的保存功能解析标题是解析标签&lt;h2&gt;的标签为标题，所以使用到了HTML解析功能，这里使用的是[bupt1987](https://github.com/bupt1987/HtmlParser "bupt1987")同学提供的html-parser库。而这个库依赖于tidy扩展，所以你的PHP运行环境需要支持tidy.

###作者介绍
想知道更多关于我的东西，请访问我的网站：   [vasqueztech.info](http://vasqueztech.info "vasqueztech.info")

###联系我
欢迎戳邮件：liqianglau@outlook.com

###Updated History
#####创建项目，并且实现基本功能
	2015-02-18 14:38:03 星期三 <大年三十>
	
#####增加保存，查看功能
	2015-02-21 11:57:03 星期六 
