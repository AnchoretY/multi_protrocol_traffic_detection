# CICFlowerMeter

 



### 特征列表

|                 |                                                              |
| --------------- | ------------------------------------------------------------ |
| fl_dur          | 流持续时间                                                   |
| tot_fw_pk       | 前向包总数                                                   |
| tot_bw_pk       | 后向包总数                                                   |
| tot_l_fw_pkt    | 前向包总大小                                                 |
| fw_pkt_l_max    | 前向包中最大包大小                                           |
| fw_pkt_l_min    | 前向包中最小包大小                                           |
| fw_pkt_l_avg    | 前向包中平均包大小                                           |
| fw_pkt_l_std    | 前向包中包大小标准差                                         |
| Bw_pkt_l_max    | 后向包中最大包大小                                           |
| Bw_pkt_l_min    | 后向包中最小包大小                                           |
| Bw_pkt_l_avg    | 后向包中平均包大小                                           |
| Bw_pkt_l_std    | 后向包中包大小的标准差                                       |
| fl_byt_s        | 流字节率，flow中每秒发送的字节数                             |
| fl_pkt_s        | 流包发送率，flow中每秒发送的包数                             |
| fl_iat_avg      | Average time between two flows                               |
| fl_iat_std      | Standard deviation time two flows                            |
| fl_iat_max      | Maximum time between two flows                               |
| fl_iat_min      | Minimum time between two flows                               |
| fw_iat_tot      | flow中两个前向包发送时间间隔的总和                           |
| fw_iat_avg      | flow中两个前向包发送时间间隔的平均值                         |
| fw_iat_std      | flow中两个前向包发送时间间隔的标准差                         |
| fw_iat_max      | flow中两个前向包发送时间间隔的最大值                         |
| fw_iat_min      | flow中两个前向包发送时间间隔的最小值                         |
| bw_iat_tot      | flow中两个后向包发送时间间隔的标准差                         |
| bw_iat_avg      | flow中两个后向包发送时间间隔的平均值                         |
| bw_iat_std      | flow中两个后向包发送时间间隔的标准差                         |
| bw_iat_max      | flow中两个后向包发送时间间隔的最大值                         |
| bw_iat_min      | flow中两个后向包发送时间间隔的最小值                         |
| fw_psh_flag     | 前向包中包含psh标记的包总数                                  |
| bw_psh_flag     | 后向包中包含psh标记的包总数                                  |
| fw_urg_flag     | 前向包中包含urg标记的包总数                                  |
| bw_urg_flag     | 后向包中包含psh标记的包总数                                  |
| fw_hdr_len      | 前向包header大小总和                                         |
| bw_hdr_len      | 后向包header大小总和                                         |
| fw_pkt_s        | 前向包发送速率，每秒发送的前向包数                           |
| bw_pkt_s        | 后向包发送速率，每秒发送的后向包数                           |
| pkt_len_min     | 双向流中最小包长度                                           |
| pkt_len_max     | 双向流中最大包长度                                           |
| pkt_len_avg     | 双向流中平均包长度                                           |
| pkt_len_std     | 双向流中包长度标准差                                         |
| pkt_len_va      | 双向流中包长度方差                                           |
| fin_cnt         | 包含FIN标记的包数量                                          |
| syn_cnt         | 包含SYN标记的包数量                                          |
| rst_cnt         | 包含RST标记的包数量                                          |
| pst_cnt         | 包含PUSH标记的包数量                                         |
| ack_cnt         | 包含ACK标记的包数量                                          |
| urg_cnt         | 包含URG标记的包数量                                          |
| cwe_cnt         | 包含CWE标记的包数量                                          |
| ece_cnt         | 包含ECE标记的包数量                                          |
| down_up_ratio   | 下载数据量与上传数据量的比率                                 |
| pkt_size_avg    | 平均包大小                                                   |
| fw_seg_avg      |                                                              |
| bw_seg_avg      |                                                              |
| fw_byt_blk_avg  | Average number of bytes bulk rate in the forward direction   |
| fw_pkt_blk_avg  | Average number of packets bulk rate in the forward direction |
| fw_blk_rate_avg | Average number of bulk rate in the forward direction         |
| bw_byt_blk_avg  | Average number of bytes bulk rate in the backward direction  |
| bw_pkt_blk_avg  | Average number of packets bulk rate in the backward direction |
| bw_blk_rate_avg | Average number of bulk rate in the backward direction        |
| subfl_fw_pk     | The average number of packets in a sub flow in the forward direction |
| subfl_fw_byt    | The average number of bytes in a sub flow in the forward direction |
| subfl_bw_pkt    | The average number of packets in a sub flow in the backward direction |
| subfl_bw_byt    | The average number of bytes in a sub flow in the backward direction |
| fw_win_byt      | Number of bytes sent in initial window in the forward direction |
| bw_win_byt      | # of bytes sent in initial window in the backward direction  |
| Fw_act_pkt      | # of packets with at least 1 byte of TCP data payload in the forward direction |
| fw_seg_min      | Minimum segment size observed in the forward direction       |
| atv_avg         | Mean time a flow was active before becoming idle             |
| atv_std         | Standard deviation time a flow was active before becoming idle |
| atv_max         | Maximum time a flow was active before becoming idle          |
| atv_min         | Minimum time a flow was active before becoming idle          |
| idl_avg         | Mean time a flow was idle before becoming active             |
| idl_std         | Standard deviation time a flow was idle before becoming active |
| idl_max         | Maximum time a flow was idle before becoming active          |
| idl_min         | Minimum time a flow was idle before becoming active          |
|                 |                                                              |
|                 |                                                              |
|                 |                                                              |
|                 |                                                              |
|                 |                                                              |

















为每个流构建一个标志叫Flow ID:192.168.31.100-183.232.231.174-46927-443-6，由源地址、目的地址、协议号组成。
fl_dur	流动持续时间
tot_fw_pk	正向总包数
tot_bw_pk	反向总包数
tot_l_fw_pkt	正向数据包的总大小
fw_pkt_l_max	正向数据包的最大大小
fw_pkt_l_min	正向包的最小大小
fw_pkt_l_avg	正向数据包的平均大小
fw_pkt_l_std	正向数据包的标准偏差大小
Bw_pkt_l_max	反向包的最大大小
Bw_pkt_l_min	反向包的最小大小
Bw_pkt_l_avg	反向包的平均大小
Bw_pkt_l_std	反向包的标准偏差大小
fl_byt_s	流字节率，即每秒传输的数据包数
fl_pkt_s	流包速率，即每秒传输的包数
fl_iat_avg	两个流之间的平均时间
fl_iat_std	两个流的标准差时间
fl_iat_max	两个流之间的最长时间
fl_iat_min	两个流之间的最短时间
fw_iat_tot	前向发送的两个数据包之间的总时间
fw_iat_avg	前向发送的两个数据包之间的平均时间
fw_iat_std	前向发送的两个数据包之间的标准偏差时间
fw_iat_max	前向发送的两个数据包之间的最大时间
fw_iat_min	前向发送的两个数据包之间的最短时间
bw_iat_tot	反向发送的两个数据包之间的总时间
bw_iat_avg	反向发送的两个数据包之间的平均时间
bw_iat_std	反向发送的两个数据包之间的标准偏差时间
bw_iat_max	反向发送的两个数据包之间的最大时间
bw_iat_min	反向发送的两个数据包之间的最短时间
fw_psh_flag	在正向传输的数据包中设置 PSH 标志的次数（UDP 为 0）
bw_psh_flag	在反向传输的数据包中设置 PSH 标志的次数（UDP 为 0）
fw_urg_flag	在正向传输的数据包中设置 URG 标志的次数（UDP 为 0）
bw_urg_flag	在反向传输的数据包中设置 URG 标志的次数（UDP 为 0）
fw_hdr_len	用于前向数据包头部的总字节数
bw_hdr_len	用于反向数据包头部的总字节数
fw_pkt_s	每秒前向数据包数
bw_pkt_s	每秒反向数据包数
pkt_len_min	流的最小长度
pkt_len_max	流的最大长度
pkt_len_avg	流的平均长度
pkt_len_std	流的标准偏差长度
pkt_len_va	数据包最小到达间隔时间
fin_cnt	带FIN的数据包数
syn_cnt	带有 SYN 的数据包数
rst_cnt	带有 RST 的数据包数
pst_cnt	PUSH的数据包数
ack_cnt	带有 ACK 的数据包数
urg_cnt	带有 URG 的数据包数量
cwe_cnt	带有 CWE 的数据包数
ece_cnt	带有 ECE 的数据包数
down_up_ratio	下载上传比例
pkt_size_avg	数据包平均大小
fw_seg_avg	前向的平均尺寸
bw_seg_avg	反向的平均尺寸
fw_byt_blk_avg	前向平均字节数批量速率
fw_pkt_blk_avg	前向平均包块率
fw_blk_rate_avg	前向平均散货率
bw_byt_blk_avg	反向平均字节数批量速率
bw_pkt_blk_avg	反向平均包块率
bw_blk_rate_avg	反向平均散货率
subfl_fw_pk	前向子流中的平均数据包数
subfl_fw_byt	前向子流的平均字节数
subfl_bw_pkt	反向子流中的平均数据包数
subfl_bw_byt	反向子流的平均字节数
fw_win_byt	前向初始窗口中发送的字节数
bw_win_byt	反向初始窗口中发送的字节数
Fw_act_pkt	前向具有至少 1 字节 TCP 数据有效载荷的数据包的数量
fw_seg_min	前向观察到的最小段大小
atv_avg	流在变为空闲之前处于活动状态的平均时间
atv_std	流在空闲之前处于活动状态的标准偏差时间
atv_max	流在变为空闲之前处于活动状态的最长时间
atv_min	流在变为空闲之前处于活动状态的最短时间
idl_avg	流在变为活动之前处于空闲状态的平均时间
idl_std	流在变为活动之前空闲的标准偏差时间
idl_max	流在变为活动之前空闲的最长时间
idl_min	流在变为活动之前空闲的最短时间