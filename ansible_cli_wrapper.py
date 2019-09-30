#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time    : 2019/6/26 4:01 PM
# @Author  : lij021
# @File    : ansible_cli_wrapper.py

import ansible
from ansible.cli.playbook import PlaybookCLI
from ansible.plugins.callback import CallbackBase
import json
from ansible.cli import CLI
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible import context
from ansible.utils.context_objects import CLIArgs
from ansible import constants as C
from logging import getLogger
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from optparse import Values
import time

logger = getLogger('ansible_wrapper')

INVENTORY_PATH = './inventory/'


# 因为ansible module里面的代码使用了immutableDict，导致参数不能二次初始化，即不能运行多次，需要修改这部分代码
def _init_global_context(cli_args):
    """Initialize the global context objects"""
    context.CLIARGS = CLIArgs.from_options(cli_args)


context._init_global_context = _init_global_context


def create_task(id):
    return {
        'id': id,
        'message': [],
        '_task_status': 'ok',
        '_status': 'start'

    }


class ResultCallback(CallbackBase):
    def __init__(self, result_buffer):
        super().__init__()
        self.result_buffer = result_buffer

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host.get_name()
        self.result_buffer['message'].append({
            "host": host,
            "color" : '#19be6b',
            "title" : "%s %s: %s" % (str(host), result.task_name, 'ok'),
            "message": result._result
        })
        self.result_buffer['_task_status'] = 'ok'
        print(result.task_name, result._result)

    def v2_runner_on_failed(self, result, **kwargs):
        host = result._host.get_name()
        self.runner_on_failed(host, result._result, False)
        self.result_buffer['message'].append({
            "host": host,
            "color" : '#ed4014',
            "title": "%s %s: %s" % (str(host), result.task_name, 'failed'),
            "message": result._result
        })
        self.result_buffer['_task_status'] = 'failed'
        print(result.task_name, result._result)

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        self.result_buffer['message'].append({
            "host": host,
            "color" : '#c5c8ce',
            "title": "%s %s: %s" % (str(host), result.task_name, 'unreachable'),
            "message": result._result
        })
        self.result_buffer['_task_status'] = 'unreachable'
        print(result.task_name, result._result)

    def v2_runner_on_skipped(self, result):
        host = result._host.get_name()
        self.runner_on_skipped(host, self._get_item(getattr(result._result, 'results', {})))
        # self.result_buffer['message'].append({
        #     "color" : '#c5c8ce',
        #     "title": "%s %s: %s" % (str(host), result.task_name, 'skipped'),
        #     "message": result._result
        # })
        # self.result_buffer['_task_status'] = 'skip'
        print(result.task_name, result._result)

    def v2_playbook_on_stats(self, stats):
        self.result_buffer['_status'] = 'done'


def runansible(task, inventory, host_list, task_list, remote_user=None, become_user=None, check=False):
    options = {'verbosity': 0, 'ask_pass': False, 'private_key_file': None, 'remote_user': remote_user,
               'connection': 'smart', 'timeout': 30, 'ssh_common_args': '', 'sftp_extra_args': '',
               'scp_extra_args': '', 'ssh_extra_args': '', 'force_handlers': False, 'flush_cache': None,
               'become': False, 'become_method': 'sudo', 'become_user': become_user, 'become_ask_pass': False,
               'check': check, 'syntax': None, 'diff': False,
               'inventory': inventory}

    loader = DataLoader()
    passwords = dict()
    results_callback = ResultCallback(task)
    inventory = InventoryManager(loader=loader, sources=[options['inventory']])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play_source = dict(
            name="Python play Ansible",
            hosts=host_list,
            gather_facts='no',
            become_method='sudo',
            become_user=become_user,
            tasks=task_list
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    tqm = None
    try:
        tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                passwords=passwords,
                stdout_callback=results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
        )
        return tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()


def run_playbook(task, inventory='hosts_dev', play_book='fetch_config.yml'):
    try:
        cli = PlaybookCLI([" ", '-i', INVENTORY_PATH + inventory, play_book])

        super(PlaybookCLI, cli).run()

        loader, inventory, variable_manager = cli._play_prereqs()

        CLI.get_host_list(inventory, context.CLIARGS['subset'])

        pbex = PlaybookExecutor(playbooks=context.CLIARGS['args'], inventory=inventory,
                                variable_manager=variable_manager, loader=loader,
                                passwords=None)

        pbex._tqm._stdout_callback = ResultCallback(task)
        pbex.run()
        return True
    except Exception as e:
        logger.error(e)
        return False


def pb_get_inventory(host_file='hosts_dev', component=None):
    try:
        loader = DataLoader()
        inventory = InventoryManager(loader=loader, sources=[INVENTORY_PATH + host_file])
        groups = inventory.groups
        result = {}
        for key in groups.keys():
            if len(groups[key].hosts):
                group = []
                for h in groups[key].hosts:
                    group.append({
                        "name": h.name,
                        "ip": h.vars['ansible_host']
                        # "user": h.vars['ansible_user'],
                    })
                if component in key or component == 'all':
                    result[key] = group
            if len(groups[key].child_groups):
                group = []
                for cg in groups[key].child_groups:
                    for h in cg.hosts:
                        group.append({
                            "name": h.name,
                            "ip": h.vars['ansible_host']
                            # "user": h.vars['ansible_user'],
                        })
                    if component in key or component == 'all':
                        result[key] = group
        return result
    except Exception as e:
        logger.error(e)
        return None


def play_get_etc_config(task, inventory, host, type, config_path, file_name):
    tasks_list = [
        dict(action=dict(module='fetch',
                         args='src=%s dest=./tmp/%s-{{ inventory_hostname }}-%s flat=yes' % (
                         config_path, type, file_name))),
    ]
    return runansible(task, INVENTORY_PATH + inventory, [host], tasks_list)

def play_service(task, inventory, host, service, state, check=False):
    tasks_list = [
        dict(action=dict(module='service',
                         args='name=%s state=%s' % (
                         service, state))),
    ]
    return runansible(task, INVENTORY_PATH + inventory, [host], tasks_list, check=check)


def pb_upload_reset_config(task, inventory, host, component, config_path, file_name, content, update_only, use_template):
    file_path = './tmp/%s-%s-%s' % (component, host, file_name)
    with open(file_path, 'wb') as f:
        f.write(content)
    with open('./playbook_template/update_configuration.yml', 'r') as t:
        template = t.read()
    with open('./update_configuration.yml', 'w') as pb:
        pb_content = template % (host, file_path, config_path, component, update_only, use_template)
        pb.write(pb_content)
    return run_playbook(task, inventory, 'update_configuration.yml')


def pb_deploy_software(task, inventory, hosts, component, version):
    with open('./playbook_template/deploy.yml', 'r') as t:
        template = t.read()
    with open('./deploy.yml', 'w') as pb:
        pb_content = template % (hosts, component, version)
        pb.write(pb_content)
    return run_playbook(task, inventory, 'deploy.yml')

def pb_undeploy_software(task, inventory, hosts, component):
    with open('./playbook_template/undeploy.yml', 'r') as t:
        template = t.read()
    with open('./undeploy.yml', 'w') as pb:
        pb_content = template % (hosts, component)
        pb.write(pb_content)
    return run_playbook(task, inventory, 'undeploy.yml')

def pb_check_rpm(task, inventory, hosts, component):
    with open('./playbook_template/check_rpm.yml', 'r') as t:
        template = t.read()
    with open('./check_rpm.yml', 'w') as pb:
        pb_content = template % (hosts, component)
        pb.write(pb_content)
    return run_playbook(task, inventory, 'check_rpm.yml')


if __name__ == '__main__':
    # play_get_etc_config(create_task(), 'hosts.uat', 'kibana_all', 'kibana')
    task = create_task(123)
    # result = pb_deploy_software(task,'BD_LASS_UAT','Kafka_10.60.232.124','filebeat')
    # result = pb_check_rpm(task,'BD_LASS_UAT','Kafka_10.60.232.12','filebeat')
    # result = pb_deploy_software(task,'BD_LASS_UAT','Kafka_10.60.232.129','apm-server','abc')
    result = play_service(task, 'BD_LASS_UAT','Kafka_10.60.232.129', 'kafka', 'startted', check=True)
    print(result)