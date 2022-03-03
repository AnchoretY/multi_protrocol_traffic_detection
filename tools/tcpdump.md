



### 1. 基本语法和使用方法

`tcpdump` 的常用参数如下：

```
$ tcpdump -i eth0 -nn -s0 -v port 80
```

- **-i** : 选择要捕获的接口，通常是以太网卡或无线网卡，也可以是 `vlan` 或其他特殊接口。如果该系统上只有一个网络接口，则无需指定。
- **-nn** : 单个 n 表示不解析域名，直接显示 IP；两个 n 表示不解析域名和端口。这样不仅方便查看 IP 和端口号，而且在抓取大量数据时非常高效，因为域名解析会降低抓取速度。
- **-s0** : tcpdump 默认只会截取前 `96` 字节的内容，要想截取所有的报文内容，可以使用 `-s number`， `number`就是你要截取的报文字节数，如果是 0 的话，表示截取报文全部内容。
- **-v** : 使用 `-v`，`-vv` 和 `-vvv` 来显示更多的详细信息，通常会显示更多与特定协议相关的信息。
- `port 80` : 这是一个常见的端口过滤器，表示仅抓取 `80` 端口上的流量，通常是 HTTP。

额外再介绍几个常用参数：

- **-p** : 不让网络接口进入混杂模式。**默认情况下使用 tcpdump 抓包时，会让网络接口进入混杂模式**。如果设备接入的交换机开启了混杂模式，使用 `-p` 选项可以有效地过滤噪声。

  > 混在模式：当网卡工作在混杂模式下时，网卡将来自接口的所有数据都捕获并交给相应的驱动程序。一般计算机网卡都工作在非混杂模式下，此时网卡只接受来自网络端口的目的地址指向自己的数据。

- **-e** : 显示数据链路层信息。默认情况下 tcpdump 不会显示数据链路层信息，使用 `-e` 选项可以显示源和目的 MAC 地址，以及 VLAN tag 信息。

#### 抓取特定协议的数据

后面可以跟上协议名称来过滤特定协议的流量，以 UDP 为例，可以加上参数 udp 或 `protocol 17`，这两个命令意思相同。

```
$ tcpdump -i eth0 udp
$ tcpdump -i eth0 proto 17
```

#### 抓取特定主机的数据

使用过滤器 `host` 可以抓取特定目的地和源 IP 地址的流量。

```
$ tcpdump -i eth0 host 10.10.1.1复制代码
```

也可以使用 `src` 或 `dst` 只抓取源或目的地：

```
$ tcpdump -i eth0 dst 10.10.1.20
```

#### 将抓取的数据写入文件

使用 tcpdump 截取数据报文的时候，默认会打印到屏幕的默认输出，你会看到按照顺序和格式，很多的数据一行行快速闪过，根本来不及看清楚所有的内容。不过，tcpdump 提供了把截取的数据保存到文件的功能，以便后面使用其他图形工具（比如 wireshark，Snort）来分析。

`-w` 选项用来把数据报文输出到文件：

```
$ tcpdump -i eth0 -s0 -w test.pcap
```

#### 行缓冲模式

如**果想实时将抓取到的数据通过管道传递给其他工具来处理，需要使用 `-l` 选项来开启行缓冲模式**（或使用 `-c` 选项来开启数据包缓冲模式）。使用 `-l` 选项可以将输出通过立即发送给其他命令，其他命令会立即响应。

```
$ tcpdump -i eth0 -s0 -l port 80 | grep 'Server:'
```

### 2. tcpdump输出

![image-20220302175453526](/Users/yhk/Library/Application Support/typora-user-images/image-20220302175453526.png)

最基本也是最重要的信息就是数据报的源地址/端口和目的地址/端口，上面的例子第一条数据报中，源地址 ip 是 `10.254.124.178`，源端口是 `63435`，目的地址是 `123.129.198.226`，目的端口是 `80`。 `>` 符号代表数据的方向。

此外，上面的前三条数据还是 tcp 协议的三次握手过程，第一条就是 `SYN` 报文，这个可以通过 `Flags [S]` 看出。下面是常见的 TCP 报文的 Flags:

- `[S]` : SYN（开始连接）
- `[.]` : 没有 Flag
- `[P]` : PSH（推送数据）
- `[F]` : FIN （结束连接）
- `[R]` : RST（重置连接）

而第二条数据的 `[S.]` 表示 `SYN-ACK`，就是 `SYN` 报文的应答报文。

第四条数据表示正式开始HTTP数据传输，Flags[P.]或Flags[.]，传输内容为标准HTTP GET请求。

### 3. 集成输出

在实际使用中我们常常只想输出自己想要的内容，可以通过过滤器和ASCII输出并结合管道与grep、cut、awk等工具来实现。下面是一些常见数据处理的实例。

#### 抓取HTTP有效数据包

抓取 80 端口的 HTTP 有效数据包，排除 TCP 连接建立过程的数据包（SYN / FIN / ACK）：

~~~shell
tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)' -i utun3
~~~

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.rawrs9xf7eb.png)

#### 抓取DNS请求和响应

抓取标准使用53端口的DNS数据包：

~~~shell
tcpdump port 53 -s 0 -l -i utun3
~~~

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.ivmlir1c92n.png)



#### 提取 HTTP 请求的 URL

提取 HTTP 请求的主机名和路径：

```shell
tcpdump -s 0 -v -n -l -i en0| egrep -i "POST /|GET /|Host:"
```

![image](https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.9xwtskjb2fa.png)


【参考文献】

- https://juejin.cn/post/6844904084168769549