## Search 

#### 搜索语法：

```python
search_string = value[&type:value]
type = cate|tag
value= string
'&'/','/':' 应该使用转义,转义后为: '\&'/'\,'/'\:'
```

#### Example:

```
cate:default&tag:flask,mysql mongo,k\&r,id\:123,you\,are&hello
```


#### 内部分析

```
cate:default&tag:flask,mysql mongo,k\&r,id\:123,you\,are&hello
```

被搜索引擎解析后，出来的其实是一个数组:

```python
[
  {
    "cate": [
      "default"
    ]
  }, 
  {
    "tag": [
      "flask", 
      "mysql mongo", 
      "k&r", 
      "id:123", 
      "you,are"
    ]
  }, 
  {
    "content": "hello"
  }
]
```

分类为: `default`
标签为: `flask`, `mysql mongo`, `k&r`, `id:123`, `you,are`
内容应该包含: `hello`


