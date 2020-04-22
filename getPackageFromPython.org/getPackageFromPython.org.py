# -*- coding: utf-8 -*-
import requests as req
import re,sys,io,os,threadpool,time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')#解决编码问题


def getPageSourceCode(url):
    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    headers = { "User-Agent": UA}
    response = req.get(url,headers=headers,timeout=None)
    return response.text
    
def findMatchedVersion(content):
    version=[]
    versionUrl=[]
    pattern = r'<a href="(.downloads.release.python.*?)">Python (.*?)</a>'
    match = re.finditer(pattern,content)
    for i in match:
        pythonVersion = i.group(2)
        if(pythonVersion.find("2.7",0,3)!=-1 or pythonVersion.find("3.5",0,3)!=-1 or pythonVersion.find("3.6",0,3)!=-1 or pythonVersion.find("3.7",0,3)!=-1 or pythonVersion.find("3.8",0,3)!=-1):
            version.append(pythonVersion)
            versionUrl.append("https://www.python.org"+i.group(1))
    return version,versionUrl

def findDownloadUrl(url):
    result = []
    content = getPageSourceCode(url)
    pattern = r'<td><a href="(.*?)">(.*?)</a></td>'
    match = re.finditer(pattern,content)
    for i in match:
        result.append(i.group(1))
    return result
    
def downloadFile(version,versionUrl):
    if(os.path.exists(version)):
        return
    os.mkdir(version)
    downloadUrl = findDownloadUrl(versionUrl)
    argsList=[]
    for url in downloadUrl:
        fileName = url.split('/')[-1]+"_下划线后全删除.deb"
        savePath = os.path.join(version,fileName)
        argsList.append(([url,savePath],None))
    task_pool = threadpool.ThreadPool(len(downloadUrl))
    requestList=threadpool.makeRequests(downloadSingleFile,argsList)
    for i in requestList:
        task_pool.putRequest(i)
    task_pool.wait()
    return
    
    
def downloadSingleFile(url,savePath):
    print(savePath)
    file = req.get(url) 
    with open(savePath, "wb") as code:
        code.write(file.content)
    return
    
    
    
if __name__ == "__main__":
    enterUrl = "https://www.python.org/downloads/"
    content = getPageSourceCode(enterUrl)
    version,versionUrl = findMatchedVersion(content)
    print(len(versionUrl))
    for i in range(len(versionUrl)):
        print("task: "+str(i))
        time.sleep(10)
        downloadFile(version[i],versionUrl[i])
        
