## HTTP流量解析



### 使用统计功能
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

  
