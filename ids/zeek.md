

# Zeek使用手册

## 系统结构

在大体上可以将Zeek划分为将packet stream转化为更高级别的网络event stream的**event engine**和用于表达安全策略的**policy script Interpreter**，zeek系统的结构如下图所示，为了实现实时不丢包的越处于低层数据量越大，因此处理越为简单高效；越处于高层，数据被聚合的更少，因此可以执行一些复杂的操作。

<img src="https://raw.githubusercontent.com/AnchoretY/images/master/blog/image.wjxt1x8bsv.png" alt="image" style="zoom:50%;" />

### 事件引擎

过滤后的数据报流被传递到zeek系统的事件引擎层，该层首先执行几个完整性检查，确保数据报头部格式正确（检验IP头校验和），如果检查失败，zeek产生一个报错事件，丢弃该数据报。在检验时候，zeek同时重新组装IP分片，得到完整的IP数据报。

如果检查成功，则事件引擎将查找与两个IP地址、两个TCP端口号（或者两个UDP端口号）的元组关联的连接状态，如果不存在，则创建新的连接状态。然后，它将数据报分派给相应连接的处理程序。zeek维护一个tcpdump追踪文件，该文件与通信量相关联，连接处理程序在返回时告知引擎（1）是否应该将整个数据报记录到追踪文件中，（2）仅仅记录数据报头部，（3）根本不记录任何内容，这些分类权衡了流量跟踪的完整性和其生成追踪文件的大小与时间。

【参考文献】

- [zeek(bro) ——一种实时检测网络入侵的系统](https://segmentfault.com/a/1190000020660416)



## 概述

Zeek是一种基于事件的流量分析工具。

扩展名为`.zeek`
默认目录：`share/zeek`
放在`share/zeek/site`的不会在升级时被覆盖或者修改
zeek生成的事件可以参考：`base/bif/event.bif.zeek`
`*.bif`是zeek的内建函数文件，也是生成在线文档的基础。
zeek脚本语法参考：https://docs.zeek.org/en/current/script-reference/index.html
框架参考：https://docs.zeek.org/en/current/frameworks/index.html

## Zeek脚本中基础元素

### @load

定义脚本使用的库

~~~shell
@load base/frameworks/files
@load base/frameworks/notice
@load frameworks/files/hash-all-files
~~~


确保zeek加载了文件框架，通知框架和hash所有文件的脚本

### module

定义命名空间

```shell
module TeamCymruMalwareHashRegistry;
```

### export

解释自定义变量，作为脚本命令空间的一部分



```shell
export {
    redef enum Notice::Type += {
        ## The hash value of a file transferred over HTTP matched in the
        ## malware hash registry.
        Match
    };


## File types to attempt matching against the Malware Hash Registry.
option match_file_types = /application\/x-dosexec/ |
                         /application\/vnd.ms-cab-compressed/ |
                         /application\/pdf/ |
                         /application\/x-shockwave-flash/ |
                         /application\/x-java-applet/ |
                         /application\/jar/ |
                         /video\/mp4/;

## The Match notice has a sub message with a URL where you can get more
## information about the file. The %s will be replaced with the SHA-1
## hash of the file.
option match_sub_url = "https://www.virustotal.com/en/search/?query=%s";

## The malware hash registry runs each malware sample through several
## A/V engines.  Team Cymru returns a percentage to indicate how
## many A/V engines flagged the sample as malicious. This threshold
## allows you to require a minimum detection rate.
option notice_threshold = 10;
}
```

重新定义了一个可枚举的常量，描述了将使用通知框架生成的通知类型。
定义一些常量用作阈值等

### function

函数

    function do_mhr_lookup(hash: string, fi: Notice::FileInfo)
        {
        local hash_domain = fmt("%s.malware.hash.cymru.com", hash);
    
        when ( local MHR_result = lookup_hostname_txt(hash_domain) )
            {
            # Data is returned as "<dateFirstDetected> <detectionRate>"
            local MHR_answer = split_string1(MHR_result, / /);
    
            if ( |MHR_answer| == 2 )
                {
                local mhr_detect_rate = to_count(MHR_answer[1]);
    
                if ( mhr_detect_rate >= notice_threshold )
                    {
                    local mhr_first_detected = double_to_time(to_double(MHR_answer[0]));
                    local readable_first_detected = strftime("%Y-%m-%d %H:%M:%S", mhr_first_detected);
                    local message = fmt("Malware Hash Registry Detection rate: %d%%  Last seen: %s", mhr_detect_rate, readable_first_detected);
                    local virustotal_url = fmt(match_sub_url, hash);
                    # We don't have the full fa_file record here in order to
                    # avoid the "when" statement cloning it (expensive!).
                    local n: Notice::Info = Notice::Info($note=Match, $msg=message, $sub=virustotal_url);
                    Notice::populate_file_info2(fi, n);
                    NOTICE(n);
                    }
                }
            }
        }


### event

针对特定事件执行的内容

~~~shell
event file_hash(f: fa_file, kind: string, hash: string)
    {
    if ( kind == "sha1" && f?$info && f$info?$mime_type &&
         match_file_types in f$info$mime_type )
        do_mhr_lookup(hash, Notice::create_file_info(f));
~~~

file_hash事件处理程序，传递file，哈希算法的种类，哈希值
zeek执行异步操作不影响性能时使用when语句块

### 事件队列和事件处理器：

zeek的脚本语言是事件驱动的，zeek的核心功能是把事件放入有序的事件队列中，允许事件处理程序在先到先服务的基础上处理事件。
当zeek检测到发起的dns请求时，触发dns_request事件，并传递数据





### http.log日志文件介绍



http.log中的每一条记录都是由一个唯一连接标识符UID和一个连接四元组组成（源IP、源端口、目的IP、目的端口）。

> UID可用于多个日志文件内相同连接的相互关联

```shell
# ts          uid          orig_h        orig_p  resp_h         resp_p
1311627961.8  HSH4uV8KVJg  192.168.1.100 52303   192.150.187.43 80
```

剩余部分则为由HTTP定义的需要记录的HTTP协议相关信息。

```shell
# method   host         uri  referrer  user_agent
GET        zeek.org  /    -         <...>Chrome/12.0.742.122<...>
```

具体HTTP协议相关的可用字段可以参考Zeek’s [HTTP script reference](https://zeek-docs-cn.readthedocs.io/zh_CN/chinese/scripts/base/protocols/http/main.zeek.html).













# 配置框架

Zeek存在一个重要的特性，就是能够通过“配置框架”来自定义生成日志的脚本文件。”配置框架中包含下面：

- option声明
- 运行时更改options
- 一组函数
- config.log文件，其中包含了options值的每个改变。

### 声明options

- **option：**用于声明变量。option与全局变量类似，不能声明在函数、hook、event handler内部。 **在进行声明时必须进行初始化，但不一定指定具体值。**

  ```shell
  module TestModule;
  
  export {
      option my_networks: set[subnet] = {};
      option enable_feature = F;
      option hostname = "testsystem";
      option timeout_after = 1min;
      option my_ports: vector of port = {};
  }
  ```

- **redef**：用于变量赋值。初始化过的option变量可以使用redef进行赋值。

  ```shell
  redef TestModule::enable_feature = T;
  redef TestModule::my_networks += { 10.1.0.0/16, 10.2.0.0/16 };
  ```

### 改变Options

配置框架支持运行时从外部文件读取新的option值。在Zeek中一般option值改变来源于分为配置文件和Config::set_value函数两种。

- **配置文件更改options**

  配置文件中通常包含option名和值的映射关系，采用下面格式指定映射关系：

  $$[option name][tab/spaces][new value]$$

  然后在需要引用配置文件的文件中使用`Config::config_files`来指定要导入配置文件，例如到config.dat文件可以使用

  ```shell
  redef Config::config_files += { "/path/to/config.dat" };
  ```

- **Config::set_value函数更改options**

  另外一种可以在运行时对option值进行更改的方式为直接在文件内部使用`Config::set_value`函数设置一个新的值。

  ```shell
  module TestModule;
  
  export {
      option host_port: table[addr] of port = {};
  }
  
  event zeek_init() {
      local t: table[addr] of port = { [10.0.0.2] = 123/tcp };
      Config::set_value("TestModule::host_port", t);
  }
  ```

### Change handlers

change handler是一个在每次opiton值变化使自动调用的用户自定义函数，一般使用`Option::set_change_handler`进行绑定。`Option::set_change_handler`函数共有三个参数：

- option名
- 要绑定的change handler名
- 绑定的change handler优先级

下面是一个为名为testaddr和option注册change handler的例子：

```shell
module TestModule;

export {
    option testaddr = 127.0.0.1;
}

# Note: the data type of 2nd parameter and return type must match
function change_addr(ID: string, new_value: addr): addr
    {
    print fmt("Value of %s changed from %s to %s", ID, testaddr, new_value);
    return new_value;
    }

event zeek_init()
    {
    Option::set_change_handler("TestModule::testaddr", change_addr);
    }
```

每次testaddr被**改变之前**是都会先调用注册的change handler函数change_addr。

> 注意handler函数的第二个参数的类型必须与返回值类型一致。

多个change handler函数可以绑定在一个option上，这些change handler会组成一个链，第一个change handler产生的返回值将会传递给下一个。除此之外，还能通过handler绑定函数`Option::set_change_handler`的第三个参数指定handler的优先级。



# 通知框架









# 日志框架

Zeek自带一个灵活的基于键值对的日志接口，能够很好地控制日志中什么被记录，什么不被记录。Zeek的日志接口主要围绕三个抽象对象：

- **Stream**：一个日志的steam对应着一个单独的日志文件，它定义了一个日志由什么字段组成以及字段的类型是什么。例如：`conn`  steam是连接记录的总结；`http` stream是http活动的记录
- **Filter**:每个stream上都关联许多filter来决定哪些信息将被输出到日志文件中。默认具有一个filter，将全部内容直接输出输出到日志文件。
- **Writer**：每个filter都具有一个writer，writer负责定义输出到日志文件中信息的具体格式。默认写入tab分割的ascii编码格式。

Zeek中可以通过下面几种方式创建日志：

- 创建一个新的log stream
- 使用新的字段拓展已有日志文件
- 将filter应用到已经存在的log stream
- 通过设置log writer修改日志输出格式

## Streams

在一个新的log stream中，下面这些是需要做的：

- 定义一个名为`record`（Info类型）变量，这个变量中需要包含全部需要记录的字段名。
- 定义一个stream ID（enum类型），stream ID必须在每一个log stream文件中都不同。
- 必须使用`Log::create_stream`函数创建log stream
- 当要记录到log中的数据可用时，要`Log::write`被调用

下面是一个通过一个名为Foo的module创建log stream的实例：

```shell
module Foo;

export {
    redef enum Log::ID += { LOG };

    type Info: record {
        ts: time        &log;
        id: conn_id     &log;
        service: string &log &optional;
        missed_bytes: count &log &default=0;
    };
}

redef record connection += {
    foo: Info &optional;
};

event zeek_init() &priority=5
    {
    # Create the stream. This adds a default filter automatically.
    Log::create_stream(Foo::LOG, [$columns=Info, $path="foo"]);
    }

event connection_established(c: connection)
    {
    local rec: Foo::Info = [$ts=network_time(), $id=c$id];
    c$foo = rec;	# 将foo stream备份到connection中
    Log::write(Foo::LOG, rec);
    }
```

在上面代码中

-  `Info`记录定义中，`&log`属性表示写入日记中，`optional`属性表示可以没有值被写入，`&default`属性指出了默认值。
- `Log::create_stream`的第一个参数指定该log stream的ID，第二个参数定义了log stream的属性，`columns`指定了日志记录的对象，`path`定义生成日志文件的名称。
- `Log::write`具体写在哪里取决于日志中要记录的对象在那里可用，这上面的例子中`connection_established`提供了我们需要记录的数据，因此这里将`connection`记录中的信息独取出来田中到log中。

运行上面的zeek脚本后一个`foo.log`日志文件将被创建。虽然我们在Info记录中只创建了4个字段，但日志文件中将有7个字段，因为其中id字段也未record类型，其中包含了四个字段。

> 在输出的日志文件中的字段名名方式与Zeek脚本文件中的命名有所不同，Zeek脚本中的`id$orig_h`在输出的日志文件将被记录为`id.orig_h`

### 在日志文件中增加字段

还可以在日志模块定义的外部文件中增加日志文件中的字段。下面以在`conn.log`文件中增加`is_private`字段标识连接是否由私有IP发起为例：

```shell
# 增加is_private到Conn::Info中
redef record Conn::Info += {
    ## Indicate if the originator of the connection is part of the
    ## "private" address space defined in RFC1918.
    is_private: bool &default=F &log;
};
# 在连接状态值被移除时，填充is_private值
event connection_state_remove(c: connection)
    {
    if ( c$id$orig_h in Site::private_address_space )
        c$conn$is_private = T;
    }
```

> 大部分的Zeek 脚本都将他们的日志附加到`connection`记录上，使其可以被方便的访问，例如：conn log stream的CONN::INFO被附加到`connection`上，使用`c$conn`访问;http log stream的HTTP::INFO附加到`connection`上，使用`c$http`访问。



### 定义log事件

有时候需要在每次创建log stream时都制定一定的操作，这时可以使用log event来实现。下面是一个当检查日志连接中是否存在5min以下的连接的log事件：

```shell
module Foo;
export {
    redef enum Log::ID += { LOG };

    type Info: record {
        ts: time     &log;
        id: conn_id  &log;
        service: string &log &optional;
        missed_bytes: count &log &default=0;
	duration: interval &log;
    };

    global log_foo: event(rec: Info);
}

redef record connection += {
    # By convention, the name of this new field is the lowercase name
    # of the module.
    foo: Info &optional;
};


event zeek_init() &priority=5
    {
    # 通过第三个参数关联log event
    Log::create_stream(Foo::LOG, [$columns=Info, $ev=log_foo,
                       $path="foo"]);
    }

event connection_established(c: connection)
    {
    local rec: Foo::Info = [$ts=network_time(),$id=c$id,$duration=c$duration];
    c$foo = rec;	# 将foo stream备份到connection中
    Log::write(Foo::LOG, rec);
    }

# 增加一种notice提示类型
redef enum Notice::Type += {
    Long_Conn_Found		# 类型名自定义，在notice中调用
};
# 定义当前log stream的log event
event Foo::log_foo(rec: Foo::Info)
    {
    if ( rec?$duration && rec$duration < 5mins )
        NOTICE([$note=Long_Conn_Found,
                $msg=fmt("unusually long conn to %s", rec$id$resp_h),
                $id=rec$id]);
    }
```

调用下面脚本时，除了会生成`foo.log`以外，还会生成`notice.log`文件记录连接持续时间小于5min的记录。

![image-20211116174024069](/Users/yhk/Library/Application Support/typora-user-images/image-20211116174024069.png)

## Filters

每个log stream都会关联一个以上的filter，**当一个stream被创建时，就会自动出案件一个默认filter关联在其上**，可以使用`Log::add_filter`或`Log::remove_filter`增加或删除filter，通过filter可**以完成重命名log文件、将一个日志切分为多个日志、过滤写入log的记录、设置**



### 重命名Log文件

使用filter**可以更改log stream生成log文件名**。具体可以参考下面代码：

```shell
event zeek_init()
    {
    ...
    local f = Log::get_filter(Conn::LOG, "default");  # 获取默认filter
    f$path = "myconn"; # 更改生成的log file名称
    Log::add_filter(Conn::LOG, f);	# 将filter写回log stream
    }
```

### 额外生成Log文件

使用filter通过创建新的filter，增加到log stream上做到使一个log stream生成多个日志文件。具体实现可以参考下面代码：

```shell
event zeek_init()
    {
    ...
    local filter: Log::Filter = [$name="orig-only", $path="origs",
                                 $include=set("ts", "id.orig_h")];
    Log::add_filter(Conn::LOG, filter);
    }
```

`Log::Filter`包含三个属性，`name`表示filter name，`path`表示生成的日志文件名称，`include`表示生成的日志文件中包含的字段。通过上面的代码可以是现在原有的日志文件基础上额外生成一个只有ts、id.orig_h两列的origs.log日志文件。

如果只想保留origs.log文件，那么可以使用下面的方式去掉默认filter：

```shell
event zeek_init()
    {
    Log::remove_filter(Conn::LOG, "default");
    }
```

### 动态决定Log文件名

除了上面使用filter的`path`属性静态指定生成的日志文件名称，还可以通过filter的`path_func`属性指定日志文件名生成函数。

```shell
redef Site::local_nets = { 192.168.0.0/16 };

function myfunc(id: Log::ID, path: string, rec: Conn::Info) : string
    {
    local r = Site::is_local_addr(rec$id$orig_h) ? "local" : "remote";
    return fmt("%s-%s", path, r);
    }

event zeek_init()
    {
    local filter: Log::Filter = [$name="conn-split",
             $path_func=myfunc, $include=set("ts", "id.orig_h")];
    Log::add_filter(Conn::LOG, filter);
    }
```

通过上面的代码可以生成conn-local.log和conn-remote.log两个日志文件。



### 过滤Log记录

Zeek的hook机制允许Zeek决定哪些条记录将被写到日志中。

```shell
type Log::PolicyHook: hook(rec: any, id: ID, filter: Filter);
```



# 摘要统计框架

总结统计框架主要围绕三个抽象对象。

- **Observation**
- **Reducer**
- **Sumstat**：





#### 【参考文献】

- 

