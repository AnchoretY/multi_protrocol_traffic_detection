# multi_protrocol_traffic_detection

最长进行研究的集中协议：
  1. HTTP
  2. DNS

## 常用工具
### 流量包解析

### IDS
  1. #### Snort
    最早的开源IDS/IPS,支持一种自身定义的格式规则编写，规则定义简单并且现在github上有众多现成的规则集，简单规则书写简单。  
    缺点：编写复杂规则比较繁琐
  2. #### Suricata
    支持多线程、处理速度更快、规则编写更加灵活的snort，能够编写一些Snort不能编写的复杂规则。
  3. #### Bro
    **使用脚本而不是规则来进行检测**，**输出不仅仅是告警，可以是任何定义好的类型的流量日志**，虽然Bro是一款IDS但是**更常用于记录网络行为**，因为使用Bro收集元数据不仅比抓包更有效地存储信息，还能以数据包捕获无法实现的方式进行搜索、索引、查询和报告
  
  
