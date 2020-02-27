# DNS

DNS报文格式：https://jocent.me/2017/06/18/dns-protocol-principle.html

![](https://github.com/AnchoretY/images/blob/master/blog/DNS%E6%8A%A5%E6%96%87%E6%95%B4%E4%BD%93%E6%A0%BC%E5%BC%8F.png?raw=true)

1. #### 头部

   1. **会话标识（2字节）**

      &emsp;&emsp;是**DNS报文的ID标识**，对于请求报文和其对应的应答报文，这个字段是相同的，通过它可**以区分DNS应答报文是哪个请求的响应**

   2. **标志（2字节）**

   ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.png)

   | QR（1bit）     | 查询/响应标志，0为查询，1为响应                              |
   | -------------- | ------------------------------------------------------------ |
   | opcode（4bit） | 0表示标准查询，1表示反向查询，2表示服务器状态请求            |
   | AA（1bit）     | 表示授权回答                                                 |
   | TC（1bit）     | 表示可截断的                                                 |
   | RD（1bit）     | 表示期望递归                                                 |
   | RA（1bit）     | 表示可用递归                                                 |
   | rcode（4bit）  | 表示返回码，0表示没有差错，3表示名字差错，2表示服务器错误（Server Failure） |

   3. **数量字段（总共8字节）**

      &emsp;&emsp;Questions、Answer RRs、Authority RRs、Additional RRs 各自表示后面的四个区域的数目。Questions表示查询问题区域节的数量，Answers表示回答区域的数量，Authoritative namesversers表示授权区域的数量，Additional recoreds表示附加区域的数量

2. #### 正文

   1. **Queries区域**

      ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.4w4wl9m4tb.png)

      - 查询名

        &emsp;&emsp;长度不固定，且不使用填充字节，一般该字段表示的就是需要查询的域名（如果是反向查询，则为IP，反向查询即由IP地址反查域名）

        ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.sobuceaw77p.png)

        



## DNS常见的攻击

1. 拒绝服务攻击

   - DNS反射放大攻击

     &emsp;&emsp;**面向客户端**，通过伪造数据包，**伪装客户机发送解析请求，使得DNS回应包阻塞指定客户机的网络通路，目的是使得客户机无法正常工作**

     检测角度：主机向DNS服务器发送大量解析请求，且

   - DNS洪范攻击

     某些用户某一时间段内向某一服务器发送大量DNS解析请求，造成DNS服务器不能正常工作。

     **特征**：某一时间段内存在大量向某一服务器的请求，且造成DNS服务器不能正常工作。

2. DNS欺骗攻击

   - DNS劫持攻击
   - 中间人攻击
   - DNS缓存注入

3. DNS隐蔽信道
4. DNS区域传送利用
5. NSEC枚举









### 资料

1. [《DataCon大赛DNS方向writeup及总结反思》](https://www.anquanke.com/post/id/179680)清华大学在DataCon DNS恶意流量检测上的解题方案，带详细过程。

2. 