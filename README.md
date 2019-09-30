# elastic-Central-Management

## 说明

该项目的主要目的是提供一个可视化的操作界面来对elastic集群进行维护，包括配置修改，集群升级等功能。

主要目的为：
- 让运维人员能够方便快捷的对elastic集群进行维护
- 面向用户界面，而非面向大量的ansible脚本
- 只要能访问web UI即可对集群进行运维，不需要在本地安装ansible和下载大量的ansible脚本


该项目采用前后端分离的方式，前端使用了iview admin，后端使用了python + ansible

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190705105607572.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9sZXgtbGVlLmJsb2cuY3Nkbi5uZXQ=,size_16,color_FFFFFF,t_70)

## 用法

下载：
```shell
git clone https://github.com/oldcodeoberyn/elastic-Central-Management.git
```

注意：目前还属于POC阶段，代码会持续变动。

要使用该程序，首先需要添加合适的inventory文件到`/inventory`目录, 文件内容包含你elastic集群的机器：

```
[all:vars]
ansible_ssh_private_key_file=~/.ssh/id_rsa
ansible_user=root
ansible_port=22

[kibana]
kibana_1 ansible_host=39.105.128.88

[elasticsearch]
elasticsearch_master ansible_host=39.105.128.66
elasticsearch_data_1 ansible_host=39.105.128.67
elasticsearch_data_2 ansible_host=39.105.128.68

[logstash]
logstash_1 ansible_host=39.105.128.90
logstash_2 ansible_host=39.105.128.91

[filebeat]
filebeat_[1:100] ansible_host=39.105.128.[1:100]

```

### dev

```shell
cd elastic-Central-Management
python3 webservice.py
cd frontend
npm run dev
```

然后访问 http://localhost:8081/

### dev

```shell
cd elastic-Central-Management
python3 webservice.py
cd frontend
npm run build
```

然后访问 http://localhost:3389/

### 示例

![在这里插入图片描述](https://img-blog.csdnimg.cn/20190705161221119.gif)



