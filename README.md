# multi_protrocol_traffic_detection

#### 主要关注的几种协议：

1. [HTTP](./http)
2. [DNS](./dns)
3. [HTTPS](./https)

## 常用工具

### 流量抓取

1. #### [tcpdump](tools/tcpdump.md)

   &emsp;&emsp;最经典的流量**抓取**工具，采用即使输出的方式进行流量抓取，可处理的文件很大。

2. #### [tshark](tools/tshark.md)

   &emsp;&emsp;最常用的一种流量**抓取、解析**工具，进行pcap文件处理时要将整个文件读入内存，因此太大的文件很难进行解析。

> 二者在实际使用中的主要区别是：
>
> 1. 数据包深度解析只能使用tshark
> 2. 对于大规模的流量抓取，文件过滤只能使用tcmpdump

3. #### [editcap](tools/editcap.md)

   &emsp;&emsp;wireshark中的用来过滤pcap文件内容、重新进行pcap文件重组切分常用的工具，通常配合tshark使用。

4. #### [capinfos](tools/capinfos.md)

   &emsp;&emsp;Wireshark中命令行版本用来统计pcap文件中流量的统计信息的工具，通常与tshark配合使用。

5. [tcpflow](tools/tcpflow.md)

   

### 流量修改工具

1. Scapy



### NetFlow特征提取工具

1. #### CiCFlowMeter

   由加拿大安全研究所提出的一种flow特征提取框架，能够提取80余种特征，本身由java编写，也有python版本，但是python版本bug较多。

2. #### [NFStream](./tools/NFStream.md)

   一个灵活的网络流量分析框架，比CICFlowMeter更加灵活，好用，默认支持，并可以支持使用NFPlugin。

3. Zeek

   Zeek提供了已连接为单位的流量分析引擎，可以做NetFlow分析，由于是基于C语言的工具，理论上效率要更高。

 

### IDS

1. #### Snort

   &emsp;&emsp;最早开源的IDS/IPS,支持一种自身定义的格式规则编写，规则定义简单并且现在github上有众多现成的规则集，简单规则书写简单。

   缺点：编写复杂规则繁琐，处理效率低。

2. #### Suricata

   &emsp;&emsp;支持多线程、处理速度更快、规则编写更加灵活的snort，能够编写一些Snort不能编写的复杂规则。

3. #### [Bro(Zeek)](./ids/zeek.md)

   &emsp;&emsp;**使用脚本而不是规则来进行检测**，**输出不仅仅是告警，可以是任何定义好的类型的流量日志**，虽然Bro是一款IDS但是**更常用于记录网络行为**，因为使用Bro收集元数据不仅比抓包更有效地存储信息，还能以数据包捕获无法实现的方式进行搜索、索引、查询和报告。
   
   
### 数据处理工具
1. #### [urllib](tools/urllib.md)
  &emsp;&emsp;该
  
2. #### whois
  &emsp;&emsp;进行域名whois查询的Python工具包，该软件包可以很方便的查询到域名的注册者信息、域名注册时间等，返回信息格式为Dict，具体使用方式如下：
~~~Python
  # 安装 pip install python-whois
  import whois.whois as whois
  response = whois("baidu.com")
  print(response.registrar)
~~~
