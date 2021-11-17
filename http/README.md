
## 1. 协议格式



| 字段             | 请求/响应 | 含义                                                         |                                                              |
| ---------------- | --------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| content-length   |           | 请求体长度                                                   |                                                              |
| Content-type     |           | 请求体类型                                                   |                                                              |
| Accept-Encoding  | 请求      | 表明客户端可以支持的内容编码格式                             |                                                              |
| Content-Encoding | 响应      | 服务端选用的内容所选的编码格式，客户端将按照该格式对服务端返回的报文内容进行解析 | 1. **代表报文内容的编码方式而不包含头部**，在HTTP 1.x头部中固定以ASCII进行传输，不进行任何编码，HTTP 2.x中则可以采用头部压缩技术  2. **服务器返回内容也可以不进行任何编码，那样的话则没有Content-Encoding字段** |
|                  |           |                                                              |                                                              |
|                  |           |                                                              |                                                              |





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

