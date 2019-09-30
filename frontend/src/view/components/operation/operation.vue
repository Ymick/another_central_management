<template>
    <div>
        <Tabs :value="inventoryName" @on-click="get_inventory">
            <TabPane :label="infor" v-for="(infor, i) in inventoryList" :key="`infor-${i}`" :name="infor">
                <Row v-for="(hosts, group) in inventoryData" :key="group">
                    <Card :bordered="false">
                        <p slot="title" style="height: 35px">
                            {{group}}
                            <Button shape="circle" icon="md-checkbox-outline" @click="check_status(group)">检查
                            </Button>
                            <Button shape="circle" icon="md-hammer" @click="set_state(group, 'started')">安装
                            </Button>
                            <Button shape="circle" icon="md-hammer" @click="set_state(group, 'stopped')">卸载
                            </Button>
                        </p>
                        <Badge v-for="(host,i) in hosts" :key="i" :ref="host.name">
                            <Dropdown style="margin-left: 20px">
                                <Button type="primary">
                                    {{host.name}}
                                    <Icon type="ios-arrow-down"></Icon>
                                </Button>
                                <DropdownMenu slot="list">
                                    <DropdownItem><a v-on:click="check_status(host.name)">查询</a></DropdownItem>
                                    <DropdownItem><a v-on:click="set_state(host.name, 'started')">启动</a></DropdownItem>
                                    <DropdownItem><a v-on:click="set_state(host.name,'stopped')">关闭</a></DropdownItem>
                                </DropdownMenu>
                            </Dropdown>
                        </Badge>
                    </Card>

                </Row>

            </TabPane>
        </Tabs>
        <Drawer title="运行状态" :closable="false" v-model="showStatusDrawer" width="360">
            <div v-html="runningStatus">
                <Icon type="ios-loading"/>
            </div>
            <div v-html="runningResult"></div>
        </Drawer>
    </div>
</template>

<script>/* eslint-disable */
import {listInventory, getInventory} from '@/api/inventory'
import {
  getServiceStatus,
  setServiceState
} from '@/api/operation'
import {checkHTTPStatus} from '@/libs/util'
export default {
  name: 'operation',
  props: [
    'componentType'
  ],
  data () {
    return {
      vsplit: 0.65,
      selectedHosts: [],
      showStatusDrawer: false,
      showContentDrawer: false,
      templateGroup: [],
      templateUpdateTime: "2019-08-10",
      templateUpdateUser: "admin",
      templateData: "",
      taskId: 0,
      runningStatus: "",
      runningResult: "",
      inventoryName: "",
      templateName: "",
      configurationContent: "",
      hostName: "",
      inventoryList: [],
      templateList: [],
      inventoryData: []
    }
  },
  mounted () {
    this.list_inventory()
  },
  methods: {
    list_inventory() {
      listInventory().then(data => {
        this.inventoryList = data.data
        this.inventoryName = this.inventoryList[0]
        this.get_inventory(this.inventoryList[0])
      })
    },
    get_inventory(inventoryName) {
      this.inventoryName = inventoryName
      getInventory(inventoryName, this.componentType).then(data => {
        this.inventoryData = data.data
      })
    },
    check_status(host) {
      this.$Loading.start();
      this.$Spin.show();
      getServiceStatus(host, this.componentType, this.inventoryName).then(data => {
        this.$Loading.finish();
        this.$Spin.hide();
        let serviceInfoData = data.data
        for (let i in serviceInfoData) {
          console.log(this.$refs[serviceInfoData[i].host])
          for (let j in this.$refs[serviceInfoData[i].host]) {
            console.log(serviceInfoData[i])
            if (serviceInfoData[i].state === "active") {
              this.$refs[serviceInfoData[i].host][j].type = "success"
              this.$refs[serviceInfoData[i].host][j].text = serviceInfoData[i].state
            } else {
              this.$refs[serviceInfoData[i].host][j].type = "normal"
              this.$refs[serviceInfoData[i].host][j].text = serviceInfoData[i].state
            }
          }
        }
      }).catch(e => {
        this.$Loading.error();
        this.$Spin.hide()
        this.$Message.error(e)
      })
    },
    set_state(host, state) {
      this.showStatusDrawer = true;
      this.$Loading.start();
      this.$Spin.show();
      //reloaded, restarted, started, stopped
      setServiceState(host, this.componentType, this.inventoryName, state).then(data => {
        this.$Loading.finish();
        this.$Spin.hide();
        this.check_status(host)
        if (checkHTTPStatus(data, this.$Message)) {
          let result = data.data
          this.runningStatus = ""
          this.runningResult = result.message
        } else {
          this.showStatusDrawer = false
        }
      }).catch(e => {
        this.$Loading.error();
        this.$Spin.hide()
        this.$Message.error(e)
      })
    },
  }

}
</script>

<style>

</style>