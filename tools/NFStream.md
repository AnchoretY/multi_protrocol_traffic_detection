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

- NFlow Core特征：核心功能，无论NFStream中如何指定一定会包含的特征。
- 隧道解码功能特征：需要NFStream中将设置属性`DECODE_TUNNELS=TRUE`才flow中才会计算该类特征。
- Netflow layer-7可见性特征：需要NFStream中设置属性`N_DISSECTIONS>0`flow中才会计算该类特征。

- 完整流统计特征：需要在整个flow结束后才能进行统计的特征，需要NFStream中设置属性`STATISTICAL_ANALYSIS=TRUE`flow中才会计算该类特征。
- SPLT特征：包大小、包时间间隔特征， 需要NFStream中设置属性`SPLT_ANALYSIS>0`flow中才会计算该类特征

##### NFLOW CORE特征

|             特征              | 类型  |                             描述                             |
| :---------------------------: | :---: | :----------------------------------------------------------: |
|             `id`              | `int` |                          流程标识符                          |
|        `expiration_id`        | `int` | 流量过期触发器的标识符。idle_timeout可以是0，active_timeout可以是1，自定义到期可以是-1。 |
|           `src_ip`            | `str` |                     源IP地址字符串表示。                     |
|           `src_mac`           | `str` |                    源MAC地址字符串表示。                     |
|           `src_oui`           | `str` |                 源组织唯一标识符字符串表示。                 |
|          `src_port`           | `int` |                        传输层源端口。                        |
|           `dst_ip`            | `str` |                    目标IP地址字符串表示。                    |
|           `dst_mac`           | `str` |                   目标MAC地址字符串表示。                    |
|           `dst_oui`           | `str` |              目标组织上唯一的标识符字符串表示。              |
|          `dst_port`           | `int` |                       传输层目标端口。                       |
|          `protocol`           | `int` |                         传输层协议。                         |
|         `ip_version`          | `int` |                           IP版本。                           |
|           `vlan_id`           | `int` |                      虚拟局域网标识符。                      |
| `bidirectional_first_seen_ms` | `int` |         第一流双向数据包上的时间戳（以毫秒为单位）。         |
| `bidirectional_last_seen_ms`  | `int` |       最后一个流双向数据包上的时间戳（以毫秒为单位）。       |
|  `bidirectional_duration_ms`  | `int` |               以毫秒为单位的双向流动持续时间。               |
|    `bidirectional_packets`    | `int` |                     流双向数据包累加器。                     |
|     `bidirectional_bytes`     | `int` |         流双向字节累加器（取决于accounting_mode）。          |
|    `src2dst_first_seen_ms`    | `int` |       第一流src2dst数据包上的时间戳（以毫秒为单位）。        |
|    `src2dst_last_seen_ms`     | `int` |      最后一个流src2dst数据包的时间戳（以毫秒为单位）。       |
|     `src2dst_duration_ms`     | `int` |            流量src2dst持续时间（以毫秒为单位）。             |
|       `src2dst_packets`       | `int` |                   流src2dst数据包蓄电池。                    |
|        `src2dst_bytes`        | `int` |        流src2dst字节累加器（取决于accounting_mode）。        |
|    `dst2src_first_seen_ms`    | `int` |        第一流dst2src数据包的时间戳（以毫秒为单位）。         |
|    `dst2src_last_seen_ms`     | `int` |      最后一个流dst2src数据包的时间戳（以毫秒为单位）。       |
|     `dst2src_duration_ms`     | `int` |            流量dst2src持续时间（以毫秒为单位）。             |
|       `dst2src_packets`       | `int` |                   流dst2src数据包蓄电池。                    |
|        `dst2src_bytes`        | `int` |        流dst2src字节累加器（取决于accounting_mode）。        |

##### Netflow 隧道解码特征（DECODE_TUNNELS=TRUE）

|    特征     | 类型  |                         描述                          |
| :---------: | :---: | :---------------------------------------------------: |
| `tunnel_id` | `int` | 隧道标识符（O：无隧道，1：GTP，2：CAPWAP，3：TZSP）。 |

##### Netflow layer-7可见性特征（N_DISSECTIONS>0）

|            特征             | 类型  |                             描述                             |
| :-------------------------: | :---: | :----------------------------------------------------------: |
|     `application_name`      | `str` |                   nDPI检测到应用程序名称。                   |
| `application_category_name` | `str` |                 nDPI检测到应用程序类别名称。                 |
|  `application_is_guessed`   | `int` |         指示检测结果是基于纯解剖还是基于端口的猜测。         |
|   `requested_server_name`   | `str` |           请求的服务器名称（SSL/TLS、DNS、HTTP）。           |
|    `client_fingerprint`     | `str` | 客户端指纹（DHCP指纹，SSL/TLS的[JA3](https://github.com/salesforce/ja3)和SSH的[HASH](https://github.com/salesforce/hassh)）。 |
|    `server_fingerprint`     | `str` | 服务器指纹（SSL/TLS的[JA3](https://github.com/salesforce/ja3)和SSH的[HASH](https://github.com/salesforce/hassh)）。 |
|        `user_agent`         | `str` |          HTTP的提取用户代理或QUIC的用户代理标识符。          |
|       `content_type`        | `str` |                     提取的HTTP内容类型。                     |

#### 完整流统计特征（STATISTICAL_ANALYSIS=TRUE）

|              特征              |  类型   |                             描述                             |
| :----------------------------: | :-----: | :----------------------------------------------------------: |
|     `bidirectional_min_ps`     |  `int`  |       流双向最小数据包大小（取决于accounting_mode）。        |
|    `bidirectional_mean_ps`     | `float` |       流双向平均数据包大小（取决于accounting_mode）。        |
|   `bidirectional_stddev_ps`    | `float` |   流双向数据包大小样本标准偏差（取决于accounting_mode）。    |
|     `bidirectional_max_ps`     |  `int`  |       流双向最大数据包大小（取决于accounting_mode）。        |
|        `src2dst_min_ps`        |  `int`  |      流src2dst最小数据包大小（取决于accounting_mode）。      |
|       `src2dst_mean_ps`        | `float` |     流量src2dst平均数据包大小（取决于accounting_mode）。     |
|      `src2dst_stddev_ps`       | `float` | 流程src2dst数据包大小样本标准偏差（取决于accounting_mode）。 |
|        `src2dst_max_ps`        |  `int`  |     流量src2dst最大数据包大小（取决于accounting_mode）。     |
|        `dst2src_min_ps`        |  `int`  |      流程dst2src最小数据包大小（取决于accounts_mode）。      |
|       `dst2src_mean_ps`        | `float` |     Flow dst2src平均数据包大小（取决于accounts_mode）。      |
|      `dst2src_stddev_ps`       | `float` | 流程dst2src数据包大小样本标准偏差（取决于accounting_mode）。 |
|        `dst2src_max_ps`        |  `int`  |     流量dst2src最大数据包大小（取决于accounting_mode）。     |
|  `bidirectional_min_piat_ms`   |  `int`  |                到达时间之间的双向最小数据包。                |
|  `bidirectional_mean_piat_ms`  | `float` |                 流量双向平均数据包到达时间。                 |
| `bidirectional_stddev_piat_ms` | `float` |             流动双向数据包到达时间样本标准偏差。             |
|  `bidirectional_max_piat_ms`   |  `int`  |                到达时间之间的双向最大数据包。                |
|     `src2dst_min_piat_ms`      |  `int`  |            到达时间之间的流量src2dst最小数据包。             |
|     `src2dst_mean_piat_ms`     | `float` |                流量src2dst平均包裹到达时间。                 |
|    `src2dst_stddev_piat_ms`    | `float` |           流量src2dst数据包到达时间样本标准偏差。            |
|     `src2dst_max_piat_ms`      |  `int`  |              流量src2dst到达时间的最大数据包。               |
|     `dst2src_min_piat_ms`      |  `int`  |            流量dst2src到达时间之间的最小数据包。             |
|     `dst2src_mean_piat_ms`     | `float` |                Flow dst2src表示包裹到达时间。                |
|    `dst2src_stddev_piat_ms`    | `float` |           流量dst2src数据包到达时间样本标准偏差。            |
|     `dst2src_max_piat_ms`      |  `int`  |            流量dst2src到达之间的最大数据包时间。             |
|  `bidirectional_syn_packets`   |  `int`  |                      双向流syn包数量。                       |
|  `bidirectional_cwr_packets`   |  `int`  |                       双向流cwr包数量                        |
|  `bidirectional_ece_packets`   |  `int`  |                       双向流ece包数量                        |
|  `bidirectional_urg_packets`   |  `int`  |                       双向流urg包数量                        |
|  `bidirectional_ack_packets`   |  `int`  |                       双向流ack包数量                        |
|  `bidirectional_psh_packets`   |  `int`  |                       双向流psh包数量                        |
|  `bidirectional_rst_packets`   |  `int`  |                       双向流rst包数量                        |
|  `bidirectional_fin_packets`   |  `int`  |                       双向流fin包数量                        |
|     `src2dst_syn_packets`      |  `int`  |                      src2dst的syn包数量                      |
|     `src2dst_cwr_packets`      |  `int`  |                      src2dst的cwr包数量                      |
|     `src2dst_ece_packets`      |  `int`  |                      src2dst的ece包数量                      |
|     `src2dst_urg_packets`      |  `int`  |                      src2dst的urg包数量                      |
|     `src2dst_ack_packets`      |  `int`  |                      src2dst的ack包数量                      |
|     `src2dst_psh_packets`      |  `int`  |                      src2dst的psh包数量                      |
|     `src2dst_rst_packets`      |  `int`  |                      src2dst的fin包数量                      |
|     `src2dst_fin_packets`      |  `int`  |                      dst2src的syn包数量                      |
|     `dst2src_syn_packets`      |  `int`  |                      dst2src的syn包数量                      |
|     `dst2src_cwr_packets`      |  `int`  |                      dst2src的cwr包数量                      |
|     `dst2src_ece_packets`      |  `int`  |                      dst2src的ect包数量                      |
|     `dst2src_urg_packets`      |  `int`  |                      dst2src的urg包数量                      |
|     `dst2src_ack_packets`      |  `int`  |                      src2dst的ack包数量                      |
|     `dst2src_psh_packets`      |  `int`  |                      dst2src的psh包数量                      |
|     `dst2src_rst_packets`      |  `int`  |                      dst2src的rst包数量                      |
|     `dst2src_fin_packets`      |  `int`  |                      dst2src的fin包数量                      |

#### SPLT统计特征（SPLT_ANALYSIS>0）

|       属性       |  类型  |                             描述                             |
| :--------------: | :----: | :----------------------------------------------------------: |
| `splt_direction` | `list` | N（splt_analysis=N）第一个流包方向列表（0：src2dst，1：dst2src，-1：无数据包）。 |
|    `splt_ps`     | `list` | N（splt_analysis=N）第一个流数据包大小列表（在没有数据包时取决于accounting_mode，-1）。 |
|  `splt_piat_ms`  | `list` | N（splt_analysis=N）第一个流数据包到达时间列表（第一个数据包总是0，没有数据包时总是-1）。 |

### NFPlugin

