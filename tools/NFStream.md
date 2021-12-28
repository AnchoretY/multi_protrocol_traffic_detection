# NFStream

### 概述

NFStream是一个快速进行**在线和离线**pcap分析的网络流量处理框架，可以快速灵活的将pcap文件转化为flow为单位的数据供流量分析人员进行分析。其中共包含三种基本数据结构：

- NFStream：驱动程序流程，负责设置整体工作流程，主要是并行计量流程的编排。
- NFPlugin：NFPlugin是扩展NFStream的主要类，用于自定义用户定义的分析功能。
- NFlow：NFStream中的流表示，它包含根据NFStreamer配置计算的所有流量功能。
- NFPacket：NFStream中的包表示，包含网络数据包中的基本信息。

特点：

- 高效
- 灵活配置

### NFStream

#### 使用实例

~~~ python
from nfstream import NFStreamer
my_streamer = NFStreamer(source="facebook.pcap",
                         decode_tunnels=True,
                         bpf_filter=None,
                         promiscuous_mode=True,
                         snapshot_length=1536,
                         idle_timeout=120,
                         active_timeout=1800,
                         accounting_mode=0,
                         udps=None,
                         n_dissections=20,
                         statistical_analysis=False,
                         splt_analysis=0,
                         n_meters=0,
                         performance_report=0)
~~~

#### 属性

| `source`               | `[default=None]`  | 数据包捕获源。Pcap文件路径或网络接口名称。                   |
| ---------------------- | ----------------- | ------------------------------------------------------------ |
| `decode_tunnels`       | `[default=True]`  | 启用/禁用GTP/CAPWAP/TZSP隧道解码。                           |
| `bpf_filter`           | `[default=None]`  | 指定用于过滤所选流量的[BPF](https://biot.com/capstats/bpf.html)过滤器。 |
| `promiscuous_mode`     | `[default=True]`  | 启用/禁用乱交捕获模式。                                      |
| `snapshot_length`      | `[default=1536]`  | 控制数据包切片大小（截断）以字节为单位。                     |
| `idle_timeout`         | `[default=120]`   | 在几秒钟内空闲（未收到数据包）超过此值的流将过期。           |
| `active_timeout`       | `[default=1800]`  | 以秒为单位超过此值的活跃流将过期。                           |
| `accounting_mode`      | `[default=0]`     | 指定用于报告字节相关功能的会计模式（0：链接层，1：IP层，2：传输层，3：有效负载）。 |
| `udps`                 | `[default=None]`  | 指定用于扩展NFStreamer的用户定义的NFPlugin。                 |
| `n_dissections`        | `[default=20]`    | 用于剖析L7可见性功能的每个流数据包的数量。当设置为0时，L7可见性功能将被禁用。 |
| `statistical_analysis` | `[default=False]` | 启用/禁用死后流程统计分析。                                  |
| `splt_analysis`        | `[default=0]`     | 指定第一批数据包长度的顺序，以便进行早期统计分析。设置为0时，splt_analysis将被禁用。 |
| `n_meters`             | `[default=0]`     | 指定并行计量过程的数量。当设置为0时，NFStreamer将根据运行主机上的可用物理核心自动缩放计量。 |
| `performance_report`   | `[default=0]`     | [**绩效报告**](https://github.com/nfstream/nfstream/blob/master/assets/PERFORMANCE_REPORT.md)间隔以秒为单位。设置为0时禁用。离线捕获忽略了。 |

#### 方法

- pandas dataframe转化

  ~~~python
  # columns_to_anonymize：要进行匿名话的列名
  my_dataframe = my_streamer.to_pandas(columns_to_anonymize=[])
  my_dataframe.head()
  ~~~

- 存储为csv文件

  ~~~python
  # columns_to_anonymize：要进行匿名话的列名
  # flows_pre_file: 每个文件存储的最大flow数，0表示全部生成在一个文件中
  total_flows_count = my_streamer.to_csv(path=None, columns_to_anonymize=[], flows_per_file=0)
  ~~~

  

### NFlow

NFlow是NFStream中的流表示，它包含根据NFStreamer中配置的全部信息。其中共包含：

- Core：核心功能，无论NFStream中如何指定一定会包含的信息。
- Decoded tunnel：隧道解码功能，需要NFStream中将设置属性`DECODE_TUNNELS=TRUE`才flow中才会计算该类属性。
- Netflow layer-7 visible：netflow中第7层可见性，需要NFStream中设置属性`N_DISSECTIONS>0`flow中才会计算该类属性。

- Statistics 

#### NFLOW CORE属性







### NFPlugin

