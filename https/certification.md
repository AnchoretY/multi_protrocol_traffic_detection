ssl协议中的证书可以通过使用bro对pcap生成的证书日志来获取相关信息，生成的证书日志保存在文件x509.log中，其中包含的字段包括：

![image-20201207184045750](/Users/yhk/Library/Application Support/typora-user-images/image-20201207184045750.png)

| 字段                          | 含义                     |
| ----------------------------- | ------------------------ |
| ts                            | 时间戳                   |
| id                            | 证书id                   |
| certificate.                  |                          |
| .version                      | 证书版本号               |
| .certificate.serial           | 整数序列号               |
| .certificate.subject          | 证书主体                 |
| .certificate.issuer           | 证书签发机构             |
| .certificate.not_valid_before | 起始有效期               |
| .certificate.not_valid_after  | 结束有效期               |
| .certificate.key_alg          | 秘钥算法名称             |
| .certificate.sig_alg          | 签名算法名称             |
| .certificate.key_type         |                          |
| .certificate.key_length       | 秘钥长度（bits为单位）   |
| .certificate.exponent         |                          |
| .certificate.curve            |                          |
| san.                          | Subject Alternative Name |
| .dns                          |                          |
| .uri                          |                          |
| .email                        |                          |
| .ip                           |                          |
| basic_constraints.ca          |                          |
| basic_constraints.path_len    |                          |

![image-20201208101239499](/Users/yhk/Library/Application Support/typora-user-images/image-20201208101239499.png)



![image-20201208101148973](/Users/yhk/Library/Application Support/typora-user-images/image-20201208101148973.png)

![image-20201208100726471](/Users/yhk/Library/Application Support/typora-user-images/image-20201208100726471.png)

### conn.log、ssl.log和x509.log的关系

&emsp;&emsp;首先明确这几种日志的中分别记录什么信息：

- conn.log： IP、TCP、UDP以及ICMP连接的信息
- ssl.log： SSL握手信息
- X509.log： 证书相关信息

&emsp;&emsp;这几种证书对于使用ssl/tls协议来保证传输层安全的流量，存在下面的关系：

- con.log 中的uid信息用于标识连接，在ssl.log中使用uid来表明ssl握手信息是属于哪个连接的
- 

```
ts  uid    id.orig_h  id.orig_p  id.resp_h  id.resp_p  version    cipher curve  server_name    resumed    last_alert next_protocol  established    cert_chain_fuids   client_cert_chain_fuids    subject    issuer client_subject client_issuer  validation_status
```



### SAN

&emsp;&emsp;SLL证书通过为每个整数分配一个附加到服务器唯一域名的公、私钥对来自动识别和认证公共IP地址，但是并不意味着要为每个域名单独购买一张SSL证书，这是因为存在SAN证书。

&emsp;&emsp;SAN SSL也称为多域名SSL证书，在SAN SSL证书中，第一个域名被视为主域名，而其他域名则称为SAN域名，任何需要保护多个域名的网站都可以考虑使用SAN证。



### OCSP和



### 证书信息信息解读

&emsp;&emsp;下面是一个典型的证书中的信息。

~~~
CN=shusheng007, OU=sng, O=sng, L=tianjin, ST=jinan, C=cn
~~~

- CN: 名字和姓氏

- OU：组织单位名称

- O：组织名称

- L：所在城市或区域名称

- ST：所在省、市、自治区名称

- C: 国家或地区代码

  

### 证书验证

&emsp;&emsp;假设客户端表示为C，服务端表示为S，那么证书验证流程如下：

- C以HTTPS方式访问S
- S返回证书sngCer给C
- C使用内置的CA根证书验证SngCer，验证过程如下：
  - 将SngCer中的明文信息使用相同的





### 自签名证书

&emsp;&emsp;如果某个证书的签发机构是其本身，即certificate.subject=certificate.issuer，那么称该证书为自签名证书。一般自签名证书都不是由收信人的根证书颁发机构颁发的，因此系统无法验证其安全性，因此一般自签名证书都会被认为是伪造证书。













