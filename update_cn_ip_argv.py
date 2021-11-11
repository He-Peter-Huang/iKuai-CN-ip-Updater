import  requests
import hashlib
import sys

iKuaiHostIP="192.168.1.1"
username="admin"
password="admin"
groupName="CN_ip_list"
groupID="1"


for arg in sys.argv:
    if arg=="-h":
        iKuaiHostIP=sys.argv[sys.argv.index("-h")+1]
    if arg=="-u":
        username=sys.argv[sys.argv.index("-u")+1]
    if arg=="-p":
        password=sys.argv[sys.argv.index("-p")+1]
    if arg=="-gn":
        groupName=sys.argv[sys.argv.index("-gn")+1]
    if arg=="-gid":
        groupID=sys.argv[sys.argv.index("-gid")+1]

md5passwd=hashlib.md5(password.encode()).hexdigest()
ipList=requests.get("https://ispip.clang.cn/all_cn.txt").text
ipList=ipList.replace("\n",",")
if ipList[-1]==',':
    ipList=ipList[:-1]
ipgroup="id={} comment=, group_name={} addr_pool={}".format(groupID,groupName,ipList)
session = requests.Session()
session.post("http://{}/Action/login".format(iKuaiHostIP),json={
    "username":username,
    "passwd":md5passwd
})
files = {'ipgroup.txt': ipgroup.encode()}
session.post("http://{}/Action/upload".format(iKuaiHostIP), files=files)
session.post("http://{}/Action/call".format(iKuaiHostIP),json={"func_name":"ipgroup","action":"IMPORT","param":{"filename":"ipgroup.txt","append":0}})