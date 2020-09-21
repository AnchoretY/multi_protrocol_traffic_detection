# Tshark

**tshark主要功能包括**：

1. 抓包
2. 包解析



### Tshark常用参数

#### 流量抓取常用参数：

- -i **指定网卡进行进行抓包、监听**

- -w 写入文件.这个参数不设置，tshark将会把解码结果输出到stdout。“-w-”表示把raw输出到stdout。如果要把解码结果输出到文件，使用重定向“>”而不要-w参数。

- -r 读取文件

- -a 抓取流量多久，以秒为单位，例如-a duration:600

- -c 抓取多少个数据包

- -f 设定**抓包过滤表达式（capture filter expression）**，该表达式书写和tcpdump一致，可以参考tcpdump

  

#### 流量解析常用参数：

- -r xxx.pcap **需要分析的报文记录文件（pcap格式）**

- -d 将指定的数据按有关协议解包输出。如要将tcp 8888端口的流量按http解包，应该写为“-d tcp.port==8888,http”。注意选择子和解包协议之间不能留空格。

- -R 设置**读取（显示）过滤表达式（read filter expression）**。

  > 注意:读取（显示）过滤表达式的语法和底层相关的抓包过滤表达式语法不相同，它的语法表达要丰富得多，请参考http://www.ethereal.com/docs/dfref/ 和 http://www.ethereal.com/docs/man-pages/ethereal-filter.4.html。

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

#### 其他常用参数

- -q 用来只显示统计信息，不显示各个包的信息  一般与-z联合使用

- -z 使用统计功能

  - http,stat, 计算HTTP统计信息，显示的值是HTTP状态代码和HTTP请求方法.

    > 注意这里最后stat后面的","

    ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.oa6pupkk5n.png)

  - http,tree 计算HTTP包分布。 显示的值是HTTP请求模式和HTTP状态代码的个数等信息。

    ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.s22apch9cz.png)

  - http_req,tree    计算每个HTTP请求的统计

    ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.kbf6m27aajb.png)

  - dns,tree   计算DNS包的统计信息，包括各种rcode、opcode、响应包返回包个数等

    ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.97adlcjj5j4.png)

  - io,phs 分层级统计在捕获文件中找到的所有协议

    ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.nhkvk3yk7h.png)

  -  ip_hosts,tree 显示每个IP地址并统计每个IP地址所占流量的比率

    ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.tagnbhghr7h.png)

  -  expert 从捕获中显示专家信息（对话，错误等）

    ![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.g615zf1giq.png)

  









liunx tshark中文手册：http://linux.51yip.com/search/tshark



