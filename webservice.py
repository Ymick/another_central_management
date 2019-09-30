#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2019/6/26 4:31 PM
# @Author  : lij021
# @File    : webservice.py
import os
import functools
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, request, jsonify, g, redirect, url_for, session
from flask import make_response
from flask_cors import CORS
from flask_simpleldap import LDAP
from cmreslogging.handlers import CMRESHandler

import config

from ansible_cli_wrapper import *

app = Flask(__name__, static_folder="frontend/dist", static_url_path='', template_folder="./frontend/dist")
app.debug = True

app.config.from_object(config)

ldap = LDAP(app)

# 用于保存从服务器上拖回的配置文件，文件以'类型+inventory-hostname'命名
TEMP_PATH = './tmp/'

# 配置文件的模版目录
CONFIGURATION_TEMPLATE_PATH = './roles/update_configuration/templates/'
SOFTWARE_REPOSITORY_PATH = './install_repository/'
LEGAL_SERVICE = ["elasticsearch", "logstash", "kibana", "apm-server", "apm-javaclient", "kafka",
                             "zookeeper", "curator"]

def configure_logger(app):
    logs_folder = app.config.get('LOG_PATH')
    if not logs_folder:
        logs_folder = os.getcwd()
    logs_folder = os.path.join(logs_folder, 'ecm_logs')
    if not os.path.isdir(logs_folder):
        os.makedirs(logs_folder)

    handler = RotatingFileHandler(
            os.path.join(logs_folder, 'ecm.log'),
            maxBytes=1 * 1024 * 1024,
            backupCount=10,
            encoding='UTF-8'
    )

    # 如果不是debug模式，则捕捉INFO以上的日志信息，默认NOTSET
    if not app.config.get('DEBUG'):
        handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)

    logging_format = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)d] [%(message)s]'
    )
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    es_handler = CMRESHandler(hosts=[{'host': 'localhost', 'port': 9200}],
                              auth_type=CMRESHandler.AuthType.NO_AUTH,
                              es_index_name="central_management_log")
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(es_handler)
    return


# 配置日志
configure_logger(app)


def logged(message, level=None):
    def decorate(func):
        msg = message if message else func.__name__
        lev = level if level else logging.INFO

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            app.logger.log(lev, msg)
            return func(*args, **kwargs)

        return wrapper

    return decorate


@app.before_request
def before_request():
    # 当g.user为None时，@ldap.login_required会调用app.config['LDAP_LOGIN_VIEW']指定的函数进行校验
    if request.method == 'OPTIONS':
        g.user = {}
        return

    g.user = None

    if 'user_id' in session:
        # This is where you'd query your database to get the user info.
        g.user = {}
        g.id = int(time.time() * 10000)
        # Create a global with the LDAP groups the user is a member of.

        app.logger.log(logging.INFO,
                       "|%s|%s|%s|%s|%s|%s|" % (
                           g.id, session['user_id'], request.method, request.path, request.query_string.decode("utf-8"),
                           request.data.decode("utf-8"),))
        try:
            g.ldap_groups = ldap.get_user_groups(user=session['user_id'])
        except Exception as e:
            print(e)


@app.after_request
def after_request(response):
    try:
        if response.response and len(response.response) > 0:
            pb_result = json.loads(response.response[0])
            message = "result|%s|%s|%s|%s" % (
                pb_result['id'], pb_result['_status'], pb_result['_task_status'], pb_result['message'])
            app.logger.log(logging.INFO, "%s" % message)
    except:
        pass
    return response


@app.route('/')
def index():
    return 'Successfully logged in!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = request.json['username']
        passwd = request.json['password']
        test = ldap.bind_user(user, passwd)
        if test is None or passwd == '':
            return make_response(jsonify({"message": "用户名或者密码不正确"}), 401)
        else:
            resp = jsonify({
                "userName": request.json['username'],
                "token": "123456",
                "roles": [],
                "avatorImgPath": ''
            })

            session['user_id'] = request.json['username']
            return resp

    return make_response("未认证", 401)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


@app.route('/api/list_inventory', methods=['GET'])
@ldap.login_required
def list_inventory():
    try:
        result = os.listdir(INVENTORY_PATH)
        result.sort()

        return jsonify(result)
    except Exception as e:
        return make_response(e)


@app.route('/api/get_inventory', methods=['GET'])
@ldap.login_required
def get_inventory():
    try:
        args = request.args
        filename = args['name']
        component = args['type']
        result = pb_get_inventory(host_file=filename, component=component)
        return jsonify(result)
    except Exception as e:
        return jsonify(pb_get_inventory())


def get_config_file_path(component, filename):
    config_list = app.config.get('ELASTIC_CONFIGURATION_LIST')[component]
    for name, path in config_list:
        if name == filename:
            return path
    return ''


@app.route('/api/download_config', methods=['GET'])
@ldap.login_required
def download_config():
    try:
        args = request.args
        inventory = args['inventory']
        component = args['component']
        host = args['host']
        filename = args['filename']
        task = create_task(g.id)
        config_path = get_config_file_path(component, filename)
        print(filename, config_path)
        play_get_etc_config(task, inventory, host, component, config_path, filename)

        return jsonify(task)
    except Exception as e:
        logger.exception(e)
        return make_response("请求异常", 400)


@app.route('/api/list_config', methods=['GET'])
@ldap.login_required
def list_config():
    try:
        args = request.args
        component = args['component']
        if component:
            config_list = app.config.get('ELASTIC_CONFIGURATION_LIST')[component]
            result = []
            for name, path in config_list:
                result.append(name)
            return jsonify(result)
        else:
            return make_response("请求的类型不存在")
    except Exception as e:
        logger.error(e)
        return make_response("请求的类型不存在")


@app.route('/api/get_config', methods=['GET'])
@ldap.login_required
def fetch_config():
    try:
        args = request.args
        filename = args['filename']
        component = args['component']
        if filename and component:
            with open('./tmp/' + component + '-' + filename, 'r') as f:
                fs = f.read()
            return make_response(fs)
        else:
            return make_response("请求的文件不存在，请重新下载")
    except Exception as e:
        logger.error(e)
        return make_response("请求的文件不存在，请重新下载")


@app.route('/api/upload_config', methods=['POST'])
@ldap.login_required
def upload_config():
    try:
        args = request.args
        component = args['component']
        host = args['host']
        inventory = args['inventory']
        filename = args['filename']
        update_only = args['updateOnly']
        use_template = args['template']
        config_path = get_config_file_path(component, filename)
        content = request.data
        task = create_task(g.id)
        result = pb_upload_reset_config(task, inventory=inventory, component=component, host=host,
                                        content=content, update_only=update_only, use_template=use_template,
                                        config_path=config_path, file_name=filename)

        if result:
            return jsonify(task)
        else:
            return make_response("异常", 500)

    except Exception as e:
        logger.exception(e)
        return make_response("请求异常", 400)


@app.route('/api/config/list_template', methods=['GET'])
@ldap.login_required
def list_config_template():
    try:
        args = request.args
        component_type = args['component']
        templates = os.listdir(os.path.join(CONFIGURATION_TEMPLATE_PATH + component_type))
        result = []
        for t in templates:
            result.append(t)
        return jsonify(result)
    except Exception as e:
        logger.error(e)
        return make_response("请求的文件不存在", 404)


@app.route('/api/config/get_template', methods=['GET'])
@ldap.login_required
def get_config_template():
    try:
        args = request.args
        filename = args['filename']
        component = args['component']
        if filename and component:
            with open(os.path.join(CONFIGURATION_TEMPLATE_PATH + component, filename), 'r') as f:
                fs = f.read()
            return make_response(fs)
        else:
            return make_response("请求的文件不存在", 404)
    except Exception as e:
        logger.error(e)
        return make_response("请求的文件不存在", 404)


@app.route('/api/get_version_available', methods=['GET'])
# @ldap.login_required
def get_software_available():
    try:
        args = request.args
        component = args['component']

        if component:
            packages = os.listdir(os.path.join(SOFTWARE_REPOSITORY_PATH + component))
            result = []
            for p in packages:
                result.append(p)
            return jsonify(result)
        else:
            return make_response("请求的类型不存在", 404)
    except Exception as e:
        logger.error(e)
        return make_response("请求的文件不存在", 404)


@app.route('/api/check_rpm', methods=['GET'])
@ldap.login_required
def check_rpm():
    try:
        args = request.args
        inventory = args['inventory']
        component = args['component']
        host = args['host']
        task = create_task(g.id)
        pb_result = pb_check_rpm(task, inventory, host, component)
        result = []
        if pb_result:
            for m in task['message']:
                # print(m['host'], m['message']['results'])
                if m['message'].__contains__("results"):
                    if len(m['message']['results']):
                        tmp = m['message']['results'][0]
                    else:
                        tmp = {
                            "version": "未安装",
                            "yumstate": False
                        }
                else:
                    tmp = {
                        "version": "查询异常",
                        "yumstate": False
                    }
                tmp['host'] = m['host']
                result.append(tmp)
            return jsonify(result)
        else:
            make_response("执行脚本异常", 500)
    except Exception as e:
        logger.exception(e)
        return make_response("执行脚本异常", 500)


@app.route('/api/service', methods=['PUT'])
# @ldap.login_required
def service_control():
    try:

        args = request.args
        inventory = args['inventory']
        component = args['component']
        host = args['host']
        state = args['state']
        task = create_task(123)
        if component in LEGAL_SERVICE:
            check = False
            if state == "status":
                check = True
                state = "started"
            pb_result = play_service(task, inventory, host, component, state, check=check)
            if pb_result == 0:
                for m in task['message']:
                    # print(m['host'], m['message']['results'])
                    if m['message'].__contains__("state") and m['message'].__contains__("name") and \
                            m['message'].__contains__("status"):
                        m['message'] = {
                            "name": m['message']['name'],
                            "state": m['message']['state'],
                            "status": m['message']['status']['ExecStart'],
                        }
                return jsonify(result)

            else:
                return make_response(jsonify(task['message']), 500)
        else:
            return make_response("不支持的服务", 400)
    except Exception as e:
        logger.exception(e)
        return make_response("执行脚本异常", 500)


@app.route('/api/service/status', methods=['GET'])
# @ldap.login_required
def service_status():
    try:

        args = request.args
        inventory = args['inventory']
        component = args['component']
        host = args['host']
        task = create_task(123)
        if component in LEGAL_SERVICE:
            pb_result = play_service(task, inventory, host, component, "started", check=True)
            result = []
            if pb_result == 0:
                for m in task['message']:
                    # print(m['host'], m['message']['results'])
                    if m['message'].__contains__("state") and m['message'].__contains__("name") and \
                            m['message'].__contains__("status"):
                        tmp = {
                            "name": m['message']['name'],
                            "state": "inactive" if m['message']['changed'] == True else "active",
                            "status": m['message']['status']['ExecStart'],
                        }
                    else:
                        tmp = {
                            "name": m['message']['name'],
                            "state": "执行异常",
                            "status": "",
                        }
                    tmp['host'] = m['host']
                    print(tmp)
                    result.append(tmp)
                return jsonify(result)

            else:
                return make_response(jsonify(task['message']), 500)
        else:
            return make_response("不支持的服务", 400)
    except Exception as e:
        logger.exception(e)
        return make_response("执行脚本异常", 500)

@app.route('/api/deploy_software', methods=['GET'])
@ldap.login_required
def deploy_software():
    try:
        args = request.args
        inventory = args['inventory']
        component = args['component']
        version = args['version']
        host = args['host']
        task = create_task(g.id)
        pb_result = pb_deploy_software(task, inventory, host, component, version)
        if pb_result:
            return jsonify(task)
        else:
            make_response("执行脚本异常", 500)
    except Exception as e:
        logger.exception(e)
        return make_response("执行脚本异常", 500)


@app.route('/api/undeploy_software', methods=['GET'])
@ldap.login_required
def undeploy_software():
    try:
        args = request.args
        inventory = args['inventory']
        component = args['component']
        host = args['host']
        task = create_task(g.id)
        pb_result = pb_undeploy_software(task, inventory, host, component)
        if pb_result:
            return jsonify(task)
        else:
            make_response("执行脚本异常", 500)
    except Exception as e:
        logger.exception(e)
        return make_response("执行脚本异常", 500)


@app.route('/', methods=['GET', 'POST'])
def root():
    render = render_template('index.html')
    print(render)
    return render


if __name__ == '__main__':
    # 前后端分离架构，在调试阶段，需要允许ajax,axios等接口跨域获取cookie
    CORS(app, supports_credentials=True)
    app.run(host='0.0.0.0', port=3389)
