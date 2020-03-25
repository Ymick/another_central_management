#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2019/8/1 4:02 PM
# @Author  : lij021
# @File    : config.py

SECRET_KEY = 'some secret words'

# LDAP配置
LDAP_HOST = '39.105.128.88'
LDAP_DOMAIN = 'baidu.cn'

LDAP_BASE_DN = 'ou=people,dc=baidu,dc=cn'
LDAP_USERNAME = 'cn=admin,dc=baidu,dc=cn'
LDAP_USER_OBJECT_FILTER = '(&(objectclass=inetOrgPerson)(cn=%s))'
LDAP_OPENLDAP = True
LDAP_PASSWORD = '123456'

# Groups
LDAP_GROUP_MEMBERS_FIELD = "uniquemember"
LDAP_GROUP_OBJECT_FILTER = "(&(objectclass=groupOfUniqueNames)(cn=%s))"
LDAP_GROUP_MEMBER_FILTER = "(&(cn=*)(objectclass=groupOfUniqueNames)(uniquemember=%s))"
LDAP_GROUP_MEMBER_FILTER_FIELD = "cn"

# 将所有模块的配置文件和配置文件的路径放在这里
ELASTIC_CONFIGURATION_LIST = {
    "kibana": (("kibana.yml", "/etc/kibana/kibana.yml"),),
    "elasticsearch": (
        ("elasticsearch.yml", "/etc/elasticsearch/elasticsearch.yml"),
        ("jvm.options", "/etc/elasticsearch/jvm.options"),
        ("log4j2.properties", "/etc/elasticsearch/log4j2.properties"),
    ),
    "logstash": (
        ("logstash.yml", "/etc/logstash/logstash.yml"),
        ("basic.conf", "/etc/logstash/conf.d/basic.conf"),
        ("test.conf", "/etc/logstash/conf.d/test.conf"),
        ("jvm.options", "/etc/logstash/jvm.options"),
        ("log4j2.properties", "/etc/logstash/log4j2.properties"),
        ("extra", "/usr/share/logstash/patterns/extra"),
    ),
    "filebeat": (("filebeat.yml", "/etc/filebeat/filebeat.yml"),),
    "apm-server": (("apm-server", "/etc/apm-server/apm-server.yml"),),
    "apm-client": (("elastic.properties", "/elastic.properties"),),
    "kafka": (("server.properties", "/opt/kafka/config/server.properties"),),
    "zookeeper": (("zoo.cfg", "/opt/zookeeper/conf/zoo.cfg"),),
}
