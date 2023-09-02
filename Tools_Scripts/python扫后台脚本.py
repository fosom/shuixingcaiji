#!/usr/bin/env python
# coding:utf-8
from multiprocessing import Pool
import requests,time

def hs(line):

    line = line.strip('\n')
    
    if(len(line) <= 2):
    
        return
        
    
    if("http" not in line):
    
        line = "http://" + line
    
    
    url_path = line + "/admin.php"
    
    print(url_path)

    try:
    
        res = requests.get(url = url_path,timeout = 15)
        
        if "pbootcms" in res.text:
        
            print("存在: {}".format(url_path))
        
            f = open("ok.txt","a+")
            
            f.write(url_path + "\n")
            
            f.close()
            
            return
    
    except:
    
        pass

        #time.sleep(1)

if __name__ == '__main__':

    inFile = 'url.txt'
    
    urls = ['{}'.format(str(i)) for i in open(inFile)]
    
    pool = Pool(processes=300)
    
    pool.map(hs, urls)
    #hs("http://myyycmdm.com")
    
