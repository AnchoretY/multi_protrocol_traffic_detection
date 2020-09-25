import pyshark
import os
import time
import pandas as pd
from joblib import Parallel,delayed

def pyshark_parser(input_file,output_file):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[{}]\tStart {} http traffic analysis...".format(start_time,input_file))
    capture = pyshark.FileCapture(input_file,keep_packets=False,display_filter='http and (tcp.reassembled.length<100000 or not tcp.reassembled.length)')
    fo = open(output_file, "w")

    column_name_list = [
        'timestamp',
        'request',
        'http_version',
        'src_ip',
        'dst_ip',
        'src_port',
        'dst_port',
        'next_seq',
        'ack',
        'request_method',
        'host',
        'uri',
        'user_agent',
        'cookie',
        'referer',
        'content_type',
        'content_length',
        'response_code',
        'file_data',
        'highest_layer'
    ]

    fo.write("\t".join(column_name_list)+'\n')

    for pkt in capture:
        timestamp = ""
        src_ip = ""
        dst_ip = ""
        src_port = ""
        dst_port = ""

        nextseq = ""
        ack = ""
        
        http_version = ""
        request = "1"
        request_method = ""

        uri = ""
        host = ""
        referer = ""
        content_type = ""
        cookie = ""
        user_agent = ""
        file_data = ""
        content_length = ""
        response_code = ""
        highest_layer = ""
        
        
        
        timestamp = pkt.sniff_timestamp
        if "ip" == pkt.layers[1]._layer_name:
            src_ip = pkt.ip.src
            dst_ip = pkt.ip.dst
        else:
            src_ip = pkt.ipv6.src
            dst_ip = pkt.ipv6.dst

        src_port = pkt.tcp.srcport
        dst_port = pkt.tcp.dstport
        nextseq = pkt.tcp.nxtseq
        ack = pkt.tcp.ack
           
            
        if hasattr(pkt.http, "request_version"):
            http_version = pkt.http.request_version
        if hasattr(pkt.http, "request_uri"):
            uri = pkt.http.request_uri
        if hasattr(pkt.http, "response"):
            request = "0"
        if hasattr(pkt.http, "request_method"):
            request_method = pkt.http.request_method
        if hasattr(pkt.http, "user_agent"):
            user_agent = pkt.http.user_agent
        if hasattr(pkt.http, "host"):
            host = pkt.http.host
        if hasattr(pkt.http, "cookie"):
            cookie = pkt.http.cookie
        if hasattr(pkt.http, "referer"):
            referer = pkt.http.referer
        if hasattr(pkt.http, "content_type"):
            content_type = pkt.http.content_type
        if hasattr(pkt.http, "file_data"):
            file_data = pkt.http.file_data.replace("\t","").replace("\n","")
        if hasattr(pkt.http, "content_length"):
            content_length = pkt.http.content_length
        if hasattr(pkt.http, "response_code"):
            response_code = pkt.http.response_code
        if hasattr(pkt, "highest_layer"):
            highest_layer = pkt.highest_layer
            
        # 解析结果写入文件
        data_list = [timestamp,request,http_version,src_ip, dst_ip, src_port, dst_port,nextseq,ack,request_method,host,uri,user_agent,cookie,referer,content_type,content_length,response_code,file_data,highest_layer]
        fo.write("\t".join(data_list)+'\n')
    fo.close()
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[{}]\tanalysis success!tmp file save to {}".format(end_time,input_file,output_file))

    
def merge_response_request(input_file,output_file):
    start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[{}]\tStart merge requerst and response to a Conversation...".format(start_time))
    # 请求包响应包合并成一个会话
    df = pd.read_csv(open(input_file,errors='ignore'),sep='\t')
    
    df = df.rename(columns={"src_post":"src_port"})
    # 获取请求报文
    df_request = df[df["request"]==1]
    df_request = df_request.rename(columns ={'content_type':'request_content_type','file_data':'post_data','content_length':'request_content_length'})
    df_request = df_request.drop(axis=1,columns=['request','ack','response_code'])

    # 获取响应报文，srcip、dstip、srcport、dstport对换，tcp.ack换成tcp.nxtseq，准备与请求进行匹配
    df_response = df[df["request"]==0][["src_ip","dst_ip","src_port","dst_port","ack","response_code","content_type","content_length","file_data"]]
    df_response = df_response.rename(columns={
        "src_ip":"dst_ip",
        "dst_ip":"src_ip",
        "src_port":"dst_port",
        "dst_port":"src_port",
        "ack":"next_seq",
        "content_type":"response_conetent_type",
        "content_length":"response_content_length",
        "file_data":"response_data"
    })

    df_result = pd.merge(df_request,df_response,on=["src_ip","dst_ip","src_port","dst_port","next_seq"],how='left')
    df_result = df_result.drop(axis=1,columns=['next_seq'])

    df_result.to_csv(output_file,index=False,sep='\t')
    
    end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print("[{}]\tCompleted Conversation merge！".format(end_time))
    print("[{}]\tExtract {} http info to{}!".format(end_time,input_file,output_file))
    
    return df_result




def http_pcap2csv(input_file):
    """
        将单个pcap包中的HTTP流量进行解析。
        解析思路为：首先将pcap流量中的HTTP请求进行解析，提取全部关键字并标明该条数据是response还是request，然后根据然后使用
            request数据的src_ip、dst_ip、src_port、dst_port、nxtseq与response数据的dst_ip、src_ip、dst_port、src_port、ack进
            行匹配，匹配成功的数据则合并为一条完整的请求响应报文。        
        
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
    
    pyshark_parser(input_file,tmp_file)
    merge_response_request(tmp_file,output_file)



def floder_pcap_analysis_http(path,n_jobs=5):
    """
        对整个文件夹中的pcap文件中http流量进行多进程解析
        Parameters:
        --------------------------
            path: pcap文件存储路径
            n_jobs: 进程数
    """
    filename_l = os.listdir(path)
    file_l = []
    for filename in filename_l:
        if filename[0]!=".":
            file = os.path.join(path,filename)
            file_l.append(file)
    print(file_l)

    Parallel(n_jobs=n_jobs)(delayed(http_pcap2csv)(file) for file in file_l)
    
floder_pcap_analysis_http("./data/raw/")  
