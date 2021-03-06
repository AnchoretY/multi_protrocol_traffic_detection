# DNS
![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.xux6fd9vt4e.png)
**端口：53**

DNS报文格式：https://jocent.me/2017/06/18/dns-protocol-principle.html  
DNS报文解析：[dns_traffic_analysis.md](./dns_traffic_analysis.md)

![](https://github.com/AnchoretY/images/blob/master/blog/DNS%E6%8A%A5%E6%96%87%E6%95%B4%E4%BD%93%E6%A0%BC%E5%BC%8F.png?raw=true)

1. #### 头部

   1. **会话标识（2字节）**

      &emsp;&emsp;是**DNS报文的ID标识**，对于请求报文和其对应的应答报文，这个字段是相同的，通过它可**以区分DNS应答报文是哪个请求的响应**

   2. **标志（2字节）**

   ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.png)

   |   QR（1bit）   |               查询/响应标志，0为查询，1为响应                |       攻击       |
   | :------------: | :----------------------------------------------------------: | :--------------: |
   | opcode（4bit） | 0表示标准查询，1表示反向查询，2表示服务器状态请求 **5表示更新** | 未授权的动态更新 |
   |   AA（1bit）   |                         表示授权回答                         |                  |
   |   TC（1bit）   |                         表示可截断的                         |                  |
   |   RD（1bit）   |                         表示期望递归                         |                  |
   |   RA（1bit）   |                         表示可用递归                         |                  |
   | rcode（4bit）  | 返回码，0表示没有差错，2表示服务器错误（Server Failure），**3表示域名不存在**，4表示功能未实现,5拒绝 |    投毒、Ddos    |

   3. **数量字段（总共8字节）**

      &emsp;&emsp;Questions、Answer RRs、Authority RRs、Additional RRs 各自表示后面的四个区域的数目。Questions表示查询问题区域节的数量，Answers表示回答区域的数量，Authoritative namesversers表示授权区域的数量，Additional recoreds表示附加区域的数量

2. #### 正文

   1. **Queries区域**

      ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.4w4wl9m4tb.png)

      - **查询名**

        &emsp;&emsp;长度不固定，且不使用填充字节，一般该字段表示的就是需要查询的域名（如果是反向查询，则为IP，反向查询即由IP地址反查域名）

        ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.sobuceaw77p.png)

      - **查询类型**

        | 助记符 |                             说明                             | 类型 |     攻击     |
        | :----: | :----------------------------------------------------------: | ---- | :----------: |
        |   A    |                      由域名获得IPv4地址                      | 1    |              |
        |   NS   |                        查询域名服务器                        | 2    |              |
        | CNAME  | 查询规范名称(返回另一个域名，即当前查询的域名是另一个域名的跳转) | 5    |              |
        |  SOA   |                           开始授权                           | 6    |     投毒     |
        |  PTR   |                      把IP地址转换成域名                      | 12   |              |
        | HINFO  |                           主机信息                           | 13   |              |
        |   MX   |                           邮件交换                           | 15   |              |
        |  TXT   |                           文本记录                           | 16   |   隐蔽信道   |
        |  AAAA  |                      由域名获得IPv6地址                      | 28   |              |
        |  NSEC  |                             NSEC                             | 47   |   NSEC枚举   |
		| NSEC3  |                            NSEC3                             | 50   |              |
       |  IXFR  |                         增量区域传送                         | 251  | 区域传送攻击 |
      |  AXFR  |                       传送整个区的请求                       | 252  | 区域传送攻击 |
       |  ANY   |                 传回所有服务器已知类型的记录                 | 255  |   放大攻击   |
   
   - **查询类**
   
     通常为1，表明是Internet数据。
   
2. **资源记录区域**（**包括回答区域，授权区域和附加区域**）
  
   ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.zz04rjm1a8c.png)
   
   &emsp;&emsp;该区域有三个，但格式都是一样的。这三个区域分别是：回答区域，授权区域和附加区域
   
   - **域名**
   
     &emsp;&emsp;**格式和Queries区域的查询名字字段是一样**，有一点**不同就是，当报文中域名重复出现的时候，该字段使用2个字节的偏移指针来表示**。比如，在资源记录中，域名通常是查询问题部分的域名的重复，因此用2字节的指针来表示，具体格式是最前面的**两个高位是 11，用于识别指针**。其余的14位从DNS报文的开始处计数（从0开始），指出该报文中的相应字节数。
   
   - **查询类型**
   
     &emsp;&emsp;表明资源纪录的类型，类型名与查询类型名一致。
   
   - **查询类**
   
     &emsp;&emsp;对于Internet信息，总是IN
   
   - **生存时间**
   
     &emsp;&emsp;以秒为单位，表示的是资源记录的生命周期，一般用于当地址解析程序取出资源记录后决定保存及使用缓存数据的时间，它同时也可以表明该资源记录的稳定程度，极为稳定的信息会被分配一个很大的值（比如86400，这是一天的秒数）。
   
      - **资源数据**
   
        &emsp;&emsp;该字段是一个可变长字段，表示按照查询段的要求返回的相关资源记录的数据。可以是Address（表明查询报文想要的回应是一个IP地址）或者CNAME（表明查询报文想要的回应是一个规范主机名）等。
	
## 数据拓展
  &emsp;&emsp;DNS常用的拓展数据及其作用【[DNS数据拓展](./dns_extension.md)】

## DNS常见的攻击

1. ### 拒绝服务攻击

   - #### DNS反射放大攻击

     &emsp;&emsp;**面向客户端**，通过伪造数据包，**伪装客户机发送解析请求，使得DNS回应包阻塞指定客户机的网络通路，目的是使得客户机无法正常工作**

     **检测角度**：主机向DNS服务器发送大量解析请求，且**Queries的查询类型为ANY**，同时返回包大小远远大于正常的返回包。

   - #### DNS洪范攻击

     某些用户某一时间段内向某一服务器发送大量DNS解析请求，造成**DNS服务器不能正常**工作。

     **检测角度**：某一时间段内存在大量向某一服务器的请求，且造成DNS服务器不能正常工作。

2. ### DNS欺骗攻击

   - #### DNS劫持攻击
    &emsp;&emsp;DNS劫持是通过篡改DNS服务器上的数据来来返回给用户一个错误的查询结果IP的攻击方式，这种攻击能够**在保持URL栏不变的情况下，重新定向到另一个网站。**
   - #### 中间人攻击
     
   - #### DNS缓存注入
      - 客户端直接注入  
         &emsp;&emsp;直接对客户机的解析请求伪造响应包，将目标IP直接注入
      - 缓存投毒  
         &emsp;&emsp;这种攻击方式是攻击者**首先伪装客户机解析一个服务器一定不存在的域名，然后在服务器进行递归解析时，攻击者向服务器发送伪造的响应包，同时将域名的权威服务器加入额外字段，一旦服务器将其缓存，则被投毒**。  
         **检测角度**:**某一主机向服务器解析大量不存在域名**，**响应包中包含大量相同的SOA记录。**
   
3. ### DNS隐蔽信道
   利用DNS查询请求越过防火墙进行数据传输。
   **检测角度**：一般使用**TXT**和A类进行传输。
   
4. ### DNS区域传送利用
  
   &emsp;一般DNS区域传送操作只在网络里真的有备用域名DNS服务器时才有必要用到，但许多DNS服务器却被错误地配置成只要有client发出请求，就会向对方提供一个zone数据库的详细信息，即**允许不受信任的因特网用户执行DNS区域传送操作。** 
   
   **危害:** 便于快速判断出某个特定区域的所有主机，获取域信息，如网络拓扑结构、服务器ip地址，为攻击者的入侵提供大量敏感信息。
   
   **攻击步骤**:
   
   - 首先,查询一个域名的ns记录.
   - 然后,对权威服务器进行axfr或者ixfr查询
   
   **检测角度**：查询类型值为251(IFXR，增量区域传送)、252（AFXR，整体区域传送），并且对大量DNS服务器发出该种类型的请求
   
5. ### NSEC枚举
  
   &emsp;**&emsp;在未使用NSEC3的NSEC DNS服务器中**，若查询区文件中不存在的域名，会以NSEC记录的形式提供靠近其的最近的下一条域名，这就使攻击者可以来重复获取下一个dns记录，从而达到泄漏的作用。
   
   **检测角度**：获取全部查询类型为NSEC类型的数据

6. ### 非法DNS动态更新

   &emsp;&emsp;**正常情况下，系统管理员为DNS配置仅安全动态更新，即通过仅允许可信域客户端计算机自动向DNS服务器注册自身**，同时减少管理开销，显着降低了安全风险。**但是，在某些情况下，管理员选择使用非Active Directory集成区域以保持与组织的策略兼容。此时，任何计算机都可以向DNS服务器发送注册请求。**即使计算机不属于同一DNS域，DNS服务器也会自动在DNS数据库中添加请求计算机的记录。

   **检测角度**：opcode为5+人工分析








### 资料

1. [《DataCon大赛DNS方向writeup及总结反思》](https://www.anquanke.com/post/id/179680)清华大学在DataCon DNS恶意流量检测上的解题方案，带详细过程。
2. [ Datacon DNS攻击流量识别 内测笔记](http://momomoxiaoxi.com/数据分析/2019/04/24/datacondns1/) 具有非常详细的攻击过程、表现分析以及过滤表达式的书写。
3. [DNS参数对照表](https://www.iana.org/assignments/dns-parameters/dns-parameters.xhtml)
4.  [DATACON 2019大数据安全分析比赛WRITEUP收集](https://ixyzero.com/blog/archives/4473.html)

