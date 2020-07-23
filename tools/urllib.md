### urllib.parse
1. urlparse
  &emsp;&emsp;将完整的url解析为`<scheme>://<netloc>/<path>;<params>?<query>#<fragment>`六个部分。
~~~Python
  from urllib.parse import urlparse
  print(urlparse("https://flashgene.com/archives/102149.html?a=1&b=2#sfdf"))
  
  output:
    ParseResult(scheme='https', netloc='flashgene.com', path='/archives/102149.html', params='', query='a=1&b=2', fragment='sfdf')
~~~
2. parse_qs和parse_qsl
  &emsp;&emsp;parse_qs用于将参数字符串转换为字典型的key、value对，key为请求参数，参数为请求参数内容。
~~~Python
  from urllib.parse import urlparse,parse_qs
  query = urlparse("https://flashgene.com/archives/102149.html?a=1&b=2#sfdf").query
  print(parse_qs(query))
  
  output:
    {'a': ['1'], 'b': ['2']}
~~~
3. unquote
  &emsp;&emsp;unquote用于对url进行解码。quote用于url编码。
~~~Python
  from urllib.parse import quote,unquote
  
  print(unquote(www.baidu.com/fdf.html%3Fname%3Da%20))
  
  output:
    www.baidu.com/fdf.html?name=a c
~~~
