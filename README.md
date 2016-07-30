##mdpress

### [中文介绍](README-zhCN.md)
### Introduction

Another blog system writen by Flask and Redis. Not Mysql or Mongodb. I develop it for wordpress lower speed and i want to focus on writting blog and sometime i can try difference template, and add some widgets.

Mdpress can fullfill my requirements, and it's blog editor base on [Editor.md](https://pandao.github.io/editor.md/examples/index.html "Editor.md").

### demo: 

[Angiris Council](http://mdpress-tyraeldemo.rhcloud.com/)

### Solved Problem

- [x] Fast Load Speed
- [x] Beauty Display And Theme Support
- [ ] Post Search 
- [ ] Images Links Manager

### Feature

- [x] Strong Diretory(Category Levels) Support
- [ ] Super good search support
- [ ] Code highlight
- [ ] Convenience images upload
- [ ] Unicon images admin

###Dependence

	Python == 2.7
	Reids >= 3.0.0

and some python lib dependences can be installed by pip.


###About Me
Want to know more about author, please visit： [liuliqiang.info](http://liuliqiang.info)

###Conract

Please Mailto：liqianglau@outlook.com


###Screen Shoot
**Index**
![](http://ooo.0o0.ooo/2016/07/27/579978371acf9.jpg)
**Archive**
![](http://ooo.0o0.ooo/2016/07/27/5799783689c9f.jpg)

**Admin Login**
![1.pi](http://ooo.0o0.ooo/2016/07/27/5799783457de9.jpg)
**Admin Main**
![2.pi](http://ooo.0o0.ooo/2016/07/27/5799783ceb8a4.jpg)
**Post List**
![3.pi](http://ooo.0o0.ooo/2016/07/27/5799783a4fa9d.jpg)
**Post Editing**
![4.pic_hd](http://ooo.0o0.ooo/2016/07/27/5799783c46069.jpg)
**Tags List**
![5.pi](http://ooo.0o0.ooo/2016/07/27/579978398a840.jpg)


### TODOs

- [ ] dashboard data correct
- [x] convert markdown to html          -- 2016-7-30 00:42:08
- [x] import wordpress html to markdown -- 2016-7-30 23:43:16
- [x] import wordpress post title html decode -- 2016-7-31 00:10:31
- [ ] duosuho configs
- [ ] image admins
- [ ] category level manager
- [ ] post search
- [ ] code highlight
- [ ] template manager


###Updated History

- v0.1 
	- 2015-02-18 14:38:03 
	
	create project, and implement base feature
	
- v0.2 
	- 2015-02-21 11:57:03 

	add save and view post feature

- v0.3 
	- 2016-06-04 13:03:31 

	refactor whole project structure

- v0.4
	- 2016-7-28 22:34:36
	
	add redis models support 
	add theme and jade template support 

