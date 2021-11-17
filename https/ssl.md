# TLS协议

### TLS通信过程



![image-20211115111552573](/Users/yhk/Library/Application Support/typora-user-images/image-20211115111552573.png)





![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.iifxhl3ipj.png)

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.q8b9bfj7as.png)

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.nlw4jvc1rw.png)

### 常见拓展

### ssl协议拓展

#### SNI

&emsp;&emsp;SNI（Server Name Indication）是 TLS 的扩展，用来解决一个服务器拥有多个域名的情况下，与tls与哪个域名进行通信的问题，其中指定了要进行通信的域名。

> SNI域名字段的作用与HTTP中的Host字段作用基本一致

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.m9dbthyd3n.png)

&emsp;&emsp;在SSL handshake过程中，在client hello由客户端发送给服务器，指明在与通信IP的某个域名进行通信。在bro日志中处于ssl日志，用server name表示，没有该字段则认为没有启用该拓展。



### 证书拓展

#### SAN

&emsp;&emsp;SAN:是 SSL 标准 x509 中定义的一个扩展。使用了 SAN 字段的 SSL 证书，可以扩展此证书支持的域名，使得一个证书可以支持多个不同域名的解析。

> ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.53g7qu3deda.png)





#### 浏览器如何验证证书

当浏览器使用HTTPS连接到您的服务器时，他们会检查以确保您的SSL证书与地址栏中的主机名称匹配。

浏览器有三种找到匹配的方法：

- 1.主机名（在地址栏中）与证书**主题(Subject)**中的**通用名称(Common Name)**完全匹配。

- 2.主机名称与通配符通用名称相匹配。例如，www.example.com匹配通用名称* .example.com。

- 3.**主机名** 在**主题备用名称(SAN: Subject Alternative Name)**(SAN.DNS)字段中列出





#### 客户端使用服务端返回的信息验证服务器的**合法性**

- 证书是否过期    发行服务器证书的CA是否可靠    
- 返回的公钥是否能正确解开返回证书中的数字签名    
- 服务器证书上的域名是否和服务器的实际域名相匹配  -- 要核对CN或SAN,见上    
- 验证通过后，将继续进行通信，否则，终止通信



【参考文献】

- [HTTPS 深入浅出 - 什么是 SNI？](https://blog.csdn.net/firefile/article/details/80532161)

- [SSL证书真伪检测工具实现方法– 安全师](https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwiw54uKksPtAhWCMN4KHbdCC4gQFjADegQIARAC&url=https%3A%2F%2Fwww.secshi.com%2F16060.html&usg=AOvVaw3NuRdaBqYqCGgSpQzI3OAg)

- [基于机器学习的恶意软件加密流量检测研究分享](https://blog.riskivy.com/基于机器学习的恶意软件加密流量检测/)