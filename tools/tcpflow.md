# Tcpflow



tcpflow是一个程序，它捕获作为TCP连接（流）的一部分传输的数据，并以方便协议分析和调试的方式存储数据。每个TCP流都存储在自己的文件中。因此，**典型的TCP流将存储在两个文件中，每个方向一个**。tcpflow还可以处理存储的“tcpdump”数据包流。

#### Tcpflow与Tcpdump的异同

1. **数据流显示单位不同**

   tcpflow以流为单位显示数据内容，tcpdump以包为单位显示数据内容

2. **数据存储格式不同**

   tcpflow的数据存储是将典型的TCP流存储在两个文件中，每个方向一个独立文件；Tcpdump直接将全部数据包存储在一个指定文件中。

3. **显示层级不同**

   tcpflow只显示应用层内容，tcpdump显示传输层和应用层内容。对于常见的HTTP流量分析来说tcpflow更方便。

### 基本使用

tcpflow常用参数如下：

~~~
tcpflow -i en0 -o out 'port 80'
~~~

其中：

- **-i**：指定要监控的显卡
- **-o**：指定输出目录，tcpflow默认会自动存储结果，输出到当前目录
- ‘**port 80**’：与tcpdump一致，tcpflow同样支持各种过滤器

其他常用参数还包括：

- **-b**：每个flow最大存储的比特数
- **-c**：只在控制台输出，不存储
- **-p**：不使用混杂模式
- **-r**：从tcpdump输出的文件中进行读取

### 数据存储格式

​	每个TCP流将按照两个方向存储为两个独立的文件，可使用-o选项指定文件生成目录，使用xx选项指定生成文件的命名，默认情况下生成文件的命名规则如下：

```shell
 [timestampT]sourceip.sourceport-destip.destport[cNNNN]
```

​	其中，timestampT表示看到第一个数据包的时间戳，`cNNN`表示相同时间、相同四元组时的连接技术，一般来说执行时间前缀时很少发生连接计数，最常见的就是标准的四元组表示。

​	使用下面的命令进行HTTP流量的捕获：

~~~shell
tcpflow -i en0 'port 80' -o out
~~~

​	捕获结果如下所示：

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.h5ybqp3bmee.png)

​	其中每两个对应的文件构成一个完整的TCP流。例如下面`010.017.046.191.62615-001.180.018.011.00080`文件表示从10.017.046.191的62615端口向1.180.018.011的80端口发起的访问连接，内容如下：

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.vtf6gm2wbpg.png)

​	1.180.018.011的80端口返回的TCP响应为：

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.n26yfs7gifj.png)

​	out文件夹中还包含了一个特殊的文件`report.xml`，该文件包含了tcpflow软件信息以及每个tcp流的源端口、目的端口、源IP、目的IP、传输比特数量、传输包数量以及每个比特流的MD5值（可选）。

