tshark主要功能包括：

1. 抓包
2. 包解析



### Tshark常用参数

#### 流量抓取常用参数：

- -i **指定网卡进行进行抓包、监听**
- -w 写入文件
- -r 读取文件
- -R 读过滤器
- -a 抓取流量多久，以秒为单位，例如-a duration:600
- -c 抓取多少个数据包
- -f 过滤指定类型的流量，可以<协议类型>和BPF过滤表达式两种方式进行过滤

#### 流量解析常用参数：

- -r xxx.pcap **需要分析的报文记录文件（pcap格式）**
- -T fields 输出格式，选fields按字段，也可以选json等其他格式，需结合-e 及 -E使用
- -e frame.time_relative 取出封包的相对时间
- -e ip.src 提取源IP
- -e ip.dst 提取目的IP
- -e ip.proto 提取协议名
- -e tcp.srcport 提取源Port
- -e tcp.dstport 提取目的Port
- -e frame.len 提取数据帧大小
- -E header=n 是否输出字段名称（cvs的第1行）
- -E separator=, 指定分割符，/t是tab，/s是一格空格
- -E quote=n 指定是否对字段用引号，d是双引号，s是单引号，n是不用
- -E occurrence=f 多值时是否保留，f是第一个值，l是最后一个值，a是所有值都列出，默认全部



### DNS流量抓取

&emsp;&emsp;对DNS协议的流量进行过滤使用udp目标端口为53和dns协议的报文进行，即：

~~~
-R 'udp.dstport==53 || dns'
~~~

&emsp;&emsp;在实际环境中使用的事例：

~~~
tshark -r test.cap -T fields -e frame.time -e ip.src -e ip.dst -e dns.qry.name -R 'udp.dstport==53 || dns'
~~~

### DNS解析

#### DNS解析常用参数对照表

| 字段                    | 含义                 | 字段                    | 含义                     |
| ----------------------- | -------------------- | ----------------------- | ------------------------ |
| frame.len               | 数据长度             | dns.flags.authenticated | 服务器是否为域权威服务器 |
| ip.src                  | 源 ip                | dns.flags.checkdisable  | 非认证数据是否可接收     |
| ip.dst                  | 目的 ip              | dns.flags.rcode         | DNS reply code           |
| udp.srcport             | 源 udp 端口号        | dns.count.queries       | s数据包中 DNS 请求数     |
| udp.dstport             | 目的 udp 端口号      | dns.count.answers       | 数据包中的应答数         |
| eth.src                 | 源 MAC 地址          | dns.count.auth_rr       | 数据包中权威记录数       |
| eth.dst                 | 目的 MAC 地址        | dns.count.add_rr        | 数据包中额外记录数       |
| dns.id                  | DNS Transaction ID   | dns.qry.name            | DNS 请求名               |
| dns.flags.response      | DNS请求/响应标志     | dns.qry.class           | DNS 请求类型             |
| dns.flags.opcode        | DNS opcode           | dns.resp.name           | DNS 响应名               |
| dns.flags.authoritative | 应答是否被服务器认证 | dns.resp.type           | DNS 回复类型             |
| dns.flags.truncated     | 消息是否剪裁         | dns.resp.ttl            | DNS 响应生存时间         |
| dns.flags.recdesired    | 是否递归查询         | dns.resp.z.do           | DNS 是否支持 DNSSEC      |
| dns.flags.reavail       | 服务器是否能递归查询 | frame.time_relative     | frame 的相对时间         |

**DNS解析代码:**

~~~shell
tshark -r q1_final.pcap -T fields -e frame.number -e frame.time_relative -e ip.src -e ip.dst -e frame.len -e eth.src -e eth.dst -e udp.srcport -e udp.dstport -e dns.id -e dns.flags.response -e dns.flags.opcode -e dns.flags.authoritative -e dns.flags.truncated -e dns.flags.recdesired -e dns.flags.recavail -e dns.flags.authenticated -e dns.flags.checkdisable -e dns.flags.rcode -e dns.count.queries -e dns.count.answers -e dns.count.auth_rr -e dns.count.add_rr -e dns.qry.name -e dns.qry.type -e dns.qry.class -e dns.resp.name -e dns.resp.type -e dns.resp.ttl -e dns.resp.z.do -E separator="," -E aggregator=" " -E header=y -E occurrence=f -E quote=d > q1_final.csv
~~~





