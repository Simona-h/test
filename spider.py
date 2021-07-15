import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os

headers = { "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

def GetWeb(url=None, headers=None):
    '''
    此函数用于获取网页内容
    
    input
    url：网页的url
    headers：网页请求头
    
    retrun
    soup：经过Beautiful Soup解析后的数据
    '''
    data = []
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        data = response.content.decode('utf-8')
        soup = BeautifulSoup(data,'lxml')
        return soup
    else:
        print('网页解析失败')
        return None
        
def GetMess(soup):
    bvid = []
    a=soup.find_all('li')
    for i in a:
        if type(i.get('data-id')) == str:
            bvid.append(i.get('data-id'))
    #print(len(bvid))
    return bvid
    
def GetPicture(bvid):
    url = []
    count = 0
    while(count<len(bvid)):
        search_url = 'https://search.bilibili.com/all?keyword=' + bvid[count] + '&from_source=nav_search_new'
        #print(search_url)
        response = requests.get(search_url,headers = headers) #获取网页源代码
        page_text = response.text
        a = page_text.find(r'"pic":"')
        b = page_text.find(r'webp')
        need_image = page_text[a+7:b+3].encode("utf-8").decode("unicode_escape")
        #print(page_text[a+7:b+3],'\n',need_image)
        count += 1
        url.append("https:" + str(need_image))
        #print(url)
    return url
  
def Save(pictures):
    for rank,image_url in enumerate(pictures):
        with open(str(rank+1) + '.webp','wb') as f:
            img = requests.get(image_url)
            f.write(img.content)
            f.close()        
    
def main():
    genres = ['music','dance']    # wait to add and then collect all data from rank
    for i in genres:
        # 已创建目录，注释mkdir
        #os.mkdir('pictures/{genres}new'.format(genres=i))
        os.chdir('pictures/{genres}'.format(genres=i))
        url =  'https://www.bilibili.com/v/popular/rank/{genres}'.format(genres=i)
        soup = GetWeb(url=url, headers=headers)
        bvid = GetMess(soup)
        with open('bvid.txt','w') as f:
            lists=[line+"\n" for line in bvid]
            f.writelines(lists)
        f.close()
        print(len(bvid),'bvid got!')
        pictures = GetPicture(bvid)
        with open('picture_url.txt','w') as f:
            lists=[line+"\n" for line in pictures]
            f.writelines(lists)
        f.close()
        print(len(pictures),'pictures got!')
        Save(pictures)
        print('Save all!')
    
if __name__ == '__main__':
    main()
