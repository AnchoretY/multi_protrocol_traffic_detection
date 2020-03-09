# editcap

&emsp;&emsp;editcap是wireshark常用命令行工具的三件套之一，主要用来完成按照指定的规则对数据包进行**切分、重组**。

> &emsp;&emsp;editcap的分包功能只能根据包个数、时间间隔、报文号三种方式进行分割，而不能使用ip端口号等协议内部信息。

### 常用命令

- -c <packets per file>  按照包个数进行pcap文件切分
- -i <seconds per file> 以时间间隔分割报文文件.
  - -A <start time> 选择输出报文的开始时间(格式:YYYY-MM-DD HH:MM:SS)
  - -B <stop time> 选择输出报文的结束时间(格式:YYYY-MM-DD HH:MM:SS)

- -r 反向选择
- -w 文件合并 格式:mergecap -w <输出文件> <源文件1> <源文件2> …



### 常见应用实例

1. ##### 将pcap 文件分割成数据包数目相同的多个文件

~~~shell
editcap -c <packets-per-file><input-pcap-file><output-prefix>
~~~

2. ##### 按照秒数分割报文文件

~~~shell
editcap -i <seconds-per-file><input-pcap-file><output-prefix>
~~~

3. ##### 提取第400-500个报文到新文件

~~~
editcap i.pcap o.pcap 401-500 
~~~

4. ##### 将多个pcap文件合并到一个pcap

~~~
mergecap -w compare.pcap a.pcap b.pcap
~~~



**注意：editcap并不能根据端口、IP等角度进行切分包**