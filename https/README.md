https://michaelyou.github.io/2017/08/13/ssl-traffic-analysis/

HTTPS协议即在TCP与HTTP层之间加入了一个TLS层（传输层安全），提供内容加密、身份认证和保护数据完整性保护三大功能。

TLS握手完整的握手过程需要两个RTT

前向安全性问题：





解析工具：

- Bro

  - Bro日志字段及含义：http://gauss.ececs.uc.edu/Courses/c6055/pdf/bro_log_vars.pdf

- TCPflow 

  以流为单位进行流量数据分析。

- JA3（客户端指纹识别）

  ​	JA3方法用于收集Client Hello数据包中以下字段的十进制字节值：**版本、可接受的密码、扩展列表、椭圆曲线密码和椭圆曲线密码格式**。然后，**它将这些值串联在一起，使用“,”来分隔各个字段，同时，使用“-”来分隔各个字段中的各个值。**然后，**会计算这些字符串的MD5哈希值，以生成易于使用和共享的长度为32字符的指纹。它们就是JA3 TLS客户端的指纹。**

- JA3S（服务端指纹识别）

  ​	JA3S方法会收集Server Hello数据包中以下各个字段的十进制字节值：版本、可接受的加密算法和扩展列表。然后，它将这些值串联在一起，使用“,”来分隔各个字段，并通过“-”来分隔每个字段中的各个值。然后，会计算这些字符串的MD5哈希值，以生成易于使用和共享的长度为32字符的指纹。它们就是JA3S的指纹。

  为什么还需要JA3S来识别服务端指纹？

  > 如果客户端程序使用公共库或操作系统套接字来进行通信（如python或windows套接字），其JA3在环境中很常见，那么单单使用JA3S就并不能对这种恶意通信进行有效的识别，这是可以再加上JA3S服务端指纹来识别恶意通信。
  >
  > ​	例如：etaSploit的Meterpreter和CobaltStrike的Beacon都使用Windows套接字来启动TLS通信。对于Windows10来说，JA3=72a589da586844d7f0818ce684948eea（转到IP地址时），JA3=a0e9f5d64349fb13191bc781f81f42e1（转到域名时）。由于Windows上的其他合法应用程序都使用相同的套接字，因此，我们很难识别其中的恶意通信。但是，Kali Linux上的C2服务器对该客户端应用程序的响应方式与Internet上的普通服务器对该套接字的响应方式相比来说是独一无二的。因此，如果我们结合JA3+JA3，那么我们就能够识别这种恶意通信，而不用考虑目的地IP、域名或证书等细节信息。
  >
  > Metasploit Win10 至Kali：
  > (JA3=72a589da586844d7f0818ce684948eea 或 JA3=a0e9f5d64349fb13191bc781f81f42e1) 且 JA3S=70999de61602be74d4b25185843bd18e
  >
  > Cobalt Strike Win10 至 Kali:
  > (JA3=72a589da586844d7f0818ce684948eea 或 JA3=a0e9f5d64349fb13191bc781f81f42e1) 且 JA3S=b742b407517bac9536a77a7b0fee28e9
  >
  > ​	**这种判断方法也存在着误判的风险。**我们可以将JA3看作用户代理字符串的TLS等效项。即使某软件或恶意软件具有一个特定的字符串，那也不意味着该字符串永远是该软件所特有的。其他软件也可能使用相同的字符串。但是，这仍然不足以构成拒绝使用该字符串来增强我们的指纹分析和检测的理由。**就像其他网络元数据一样，通过加入JA3，能够进一步丰富我们的数据信息。**在使用JA3的情况下，当寻找特定内容的时候，JA3S可以显著降低误报水平。

【数据集】

- [tratosphere Research Laboratory ](https://www.stratosphereips.org/datasets-malware)





【参考文献】

-  [三种解密 HTTPS 流量的方法介绍](https://imququ.com/post/how-to-decrypt-https.html)
- [ETI：最有前景的加密流量检测方法](https://www.secrss.com/articles/25907)
- [利用JA3和JA3S实现TLS指纹识别](https://xz.aliyun.com/t/3889)
- [Wireshark分析TLS1.2通信过程](http://www.hackpluto.xyz/2020/07/27/Wireshark分析TLS1-2通信过程/)
- [基于机器学习的TLS恶意流量监测](http://www.hackpluto.xyz/2020/07/27/基于机器学习的恶意流量监测及特征提取/)

