import os

def http_pcap2csv(input_file):
    """
        将单个pcap包中的HTTP流量进行解析。
        解析思路为：首先将pcap流量中的HTTP请求进行解析，提取全部关键字并标明该条数据是response还是request，然后根据然后使用
            request数据的src_ip、dst_ip、src_port、dst_port、nxtseq与response数据的dst_ip、src_ip、dst_port、src_port、ack进
            行匹配，匹配成功的数据则合并为一条完整的请求响应报文。
        Request报文中使用的字段：
            src_ip：源IP
            dst_ip：目的IP
            src_port: 源端口
            dst_port：目的端口
            host：主机
            uri： 统一资源定位符
            method：请求方法
            user_agent：客户端代理值
            cookie：cookie值
            referer：页面跳转的源头
            
        Response报文中使用的字段：
            response_code： 响应码
            content_type： 相应文件类型
            content_length： 相应报文长度         
        
        Parameters:
        -------------------------------------------
            input_fille: 要进行解析的文件名。
              
        
    """
    tmp_path = "./data/tmp/"
    output_path = "./data/output/"
    
    input_file_name = input_file.split("/")[-1].split(".")[0]
    tmp_file = "{}{}.csv".format(tmp_path,input_file_name)
    output_file = "{}{}.csv".format(output_path,input_file_name)
    
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    
    # 使用tshark进行pcap包解析
    print("Start {} http traffic analysis...".format(input_file))
    tshark_flag = os.system(
        "tshark -r {} -Y http  -T fields -e http.response -e ip.src -e ip.dst  -e tcp.srcport -e tcp.dstport \
        -e tcp.nxtseq -e tcp.ack  -e http.host -e http.request.uri  -e http.request.method \
        -e http.content_type -e http.content_length -e http.cookie -e http.referer -e http.user_agent -e http.response.code -e http.date \
        -E separator=\"\t\" -E aggregator=\" \" -E header=y  -E occurrence=f -E quote=d > {}".format(input_file,tmp_file)
    )
    
    if tshark_flag==0:
        print("{} analysis success!tmp file save to {}".format(input_file,tmp_file))
    else:
        print("sorry, {} analysis fail!")
    
    # 请求包响应包合并成一个会话
    print("Start merge requerst and response to a Conversation...")
    df = pd.read_csv(open(tmp_file,errors='ignore'),error_bad_lines=False,encoding='utf-8',sep='\t')


    # 获取请求报文
    df_request = df[df["http.response"].isna()]
    df_request = df_request.drop(axis=1,columns=['http.response','tcp.ack','http.response.code','http.content_type','http.content_length'])

    # 获取响应报文，srcip、dstip、srcport、dstport对换，tcp.ack换成tcp.nxtseq，准备与请求进行匹配
    df_response = df[~df["http.response"].isna()][["ip.src","ip.dst","tcp.srcport","tcp.dstport","tcp.ack","http.response.code","http.content_type","http.content_length"]]
    df_response = df_response.rename(columns={
        "ip.src":"ip.dst",
        "ip.dst":"ip.src",
        "tcp.srcport":"tcp.dstport",
        "tcp.dstport":"tcp.srcport",
        "tcp.ack":"tcp.nxtseq"
    })

    df_result = pd.merge(df_request,df_response,on=["ip.dst","ip.src","tcp.dstport","tcp.srcport","tcp.nxtseq"],how='left')
    df_result = df_result.drop(axis=1,columns=['tcp.nxtseq'])
    
    
    df_result.to_csv(output_file,index=False)
    
    print("Completed Conversation merge！")
    print("Extract {} http info to{}!".format(input_file,output_file))
