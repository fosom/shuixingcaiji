#!/usr/bin/env python
# coding:utf-8
from multiprocessing import Pool
import tldextract,requests,time

def is_cms(url):

    is_cms_arr = [
    
        {"path":"/include/ckeditor/plugins/smiley/images/angel_smile.gif","text":"GIF89"},
        
        {"path":"/plus/ad_js.php","text":"Request"},
        
        {"path":"/plus/flink_add.php","text":"formbox"},
        
    ]
    
    for is_cms_a in is_cms_arr:
    
        is_cms_path = is_cms_a["path"]
        
        is_cms_text = is_cms_a["text"]
        
        url_cms_path = url + is_cms_path
        
        header = {
    
            'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
            
            'Referer':url_cms_path,
            
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
        
        }
        
        try:
        
            res = requests.get(url = url_cms_path,timeout = 15,headers = header,allow_redirects=False)
            
            if is_cms_text in res.text:
            
                return True
        
        except:
        
            return False
    
        time.sleep(0.5)

    return False


def hs(line):

    line = line.strip('\n')
    
    if(len(line) <= 2):
    
        return
        
    print(line)
    
    if is_cms(line):
    
        q = tldextract.extract(line)
        
        dic_txt = open("dic.txt","r")
        
        dic_text = dic_txt.readlines()
        
        dic_txt.close()
        
        for dic_x in dic_text:
        
            dic_x = dic_x.strip('\n')
            
            dic_x = dic_x.replace("#domain#",q.domain)
            
            url_path = line + "/" + dic_x + "/" + "login.php"
            
            print("检测：{}".format(url_path))
            
            header = {
    
                'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
                
                'Referer':url_path,
                
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
            
            }
            
            try:
            
                res = requests.get(url = url_path,timeout = 15,headers = header,allow_redirects=False)
                
                if "userid" in res.text:
                
                    print("存在后台: {}".format(url_path))
                
                    f = open("ok.txt","a+")
                    
                    f.write(url_path + "\n")
                    
                    f.close()
                    
                    return
            
            except:
            
                pass
    
            time.sleep(0.5)

if __name__ == '__main__':

    inFile = 'url.txt'
    
    urls = ['{}'.format(str(i)) for i in open(inFile)]
    
    pool = Pool(processes=300)
    
    pool.map(hs, urls)