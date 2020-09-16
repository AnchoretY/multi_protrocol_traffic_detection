
## 1. 协议格式



### content-length  
&emsp;&emsp;请求体长度，不包含请求头的部分。

### content-type
post字段是
> 注意content-type是post字段才有的字段，get请求头中没有  
**（1）application/x-www-form-urlencoded**  
&emsp;&emsp;最常见的post提交数据的方式，会将表单内的数据拼接成key-value对形式，并且将其中非ASCII码内容进行编码。  下面以发送post请求内容`aaa=aaa，bbb=你的我的`为例，其post请求内容如下：
~~~
POST / HTTP/1.1
Host: www.bilibili.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 48

aaa=aaa&bbb=%E4%BD%A0%E7%9A%84%E6%88%91%E7%9A%84
~~~

**（2）multipart/form-data**  
&emsp;&emsp;将表单的数据处理为一条消息，以标签为单元，用分隔符分开。既可以上传键值对，也可以上传文件。 下面以发送 POST 请求，参数为：aaa=aaa，bbb=你的我的啊啊啊，file=图片为例：
~~~
POST / HTTP/1.1
Host: www.bilibili.com
Content-Type: multipart/form-data;boundary=------FormBoundary15e896376d1
Content-Length: 19532

------FormBoundary15e896376d1
Content-Disposition: form-data; name="aaa"

aaa
------FormBoundary15e896376d1
Content-Disposition: form-data; name="bbb"

你的我的啊啊啊
------FormBoundary15e896376d1
Content-Disposition: form-data; name="file"; filename="cat-icon.png"
Content-Type: image/png

[message-part-body; type:image/png, size:19201 bytes]
------FormBoundary15e896376d1--
~~~





## 2. HTTP流量解析
  [流量解析工具函数](./pcap_analysis_http.py)

