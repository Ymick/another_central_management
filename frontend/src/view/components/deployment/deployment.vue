<template>
    <div>
        <Tabs :value="inventoryName" @on-click="get_inventory">
            <TabPane :label="infor" v-for="(infor, i) in inventoryList" :key="`infor-${i}`" :name="infor">
                <Row v-for="(hosts, group) in inventoryData" :key="group">
                    <Card :boardred="false">
                        <p slot="title" style="height: 35px">当前可用版本</p>
                        <Row>
                            <RadioGroup v-model="versionSelected">
                                <Radio :label="software" v-for="(software) in versionAvailable"
                                          :key="software">
                                </Radio>
                            </RadioGroup>
                        </Row>
                    </Card>
                    <br>
                    <Card :bordered="false">
                        <p slot="title" style="height: 35px">
                            {{group}}
                            <Button shape="circle" icon="md-checkbox-outline" @click="check_info(group)">检查
                            </Button>
                            <Button shape="circle" icon="md-hammer" @click="deploy_software(group)">安装
                            </Button>
                            <Button shape="circle" icon="md-hammer" @click="undeploy_software(group)">卸载
                            </Button>
                        </p>
                        <!--<Badge v-for="(host,i) in hosts" :key="host.name" text="6.4.3" :type="i>1?'primary':'success'">-->
                        <Badge v-for="(host,i) in hosts" :key="i" :ref="host.name">
                            <Dropdown style="margin-left: 20px">
                                <Button type="primary">
                                    {{host.name}}
                                    <Icon type="ios-arrow-down"></Icon>
                                </Button>
                                <DropdownMenu slot="list">
                                    <DropdownItem><a v-on:click="check_info(host.name)">检查</a></DropdownItem>
                                    <DropdownItem><a v-on:click="deploy_software(host.name)">安装</a></DropdownItem>
                                    <DropdownItem><a v-on:click="undeploy_software(host.name)">卸载</a></DropdownItem>
                                </DropdownMenu>
                            </Dropdown>
                        </Badge>
                    </Card>
                    <Divider></Divider>

                </Row>
            </TabPane>
        </Tabs>
        <Drawer title="运行状态" :closable="false" v-model="showStatusDrawer" width="800">
            <div v-html="runningStatus">
                <Icon type="ios-loading"/>
            </div>
            <div>
                <Collapse>
                    <Panel v-for="(status,i) in runningResult" :key="`ressult-${i}`" :name="status.title">
                        <b :style="`color: ${status.color}`">{{status.title}}</b>
                        <p slot="content">{{status.message}}</p>
                    </Panel>
                </Collapse>

            </div>
        </Drawer>
    </div>
</template>

<script>/* eslint-disable */
import {listInventory, getInventory} from '@/api/inventory'
import {getVersionAvailable, checkRPM, deploySoftware, undeploySoftware} from '@/api/operation'
import {checkHTTPStatus} from '@/libs/util'
export default {
  name: 'deployment',
  props: [
    'componentType'
  ],
  data () {
    return {
      selectedHost: "",
      showStatusDrawer: false,
      taskId: 0,
      runningStatus: "",
      runningResult: "",
      inventoryName: "",
      hostName: "",
      inventoryList: [],
      inventoryData: [],
      versionSelected: "",
      versionAvailable: []
    }
  },
  mounted () {
    this.get_versionAvailable()
    this.list_inventory()
  },
  methods: {
    list_inventory() {
      listInventory().then(data => {
        this.inventoryList = data.data
        this.inventoryName = this.inventoryList[0]
        this.get_inventory(this.inventoryList[0])
      }).catch(e => {
        this.$Message.error(e)
      })
    },
    get_inventory(inventoryName) {
      this.inventoryName = inventoryName
      getInventory(inventoryName, this.componentType).then(data => {
        this.inventoryData = data.data
      }).catch(e => {
        this.$Message.error(e)
      })
    },
    get_versionAvailable() {
      getVersionAvailable(this.componentType).then(data => {
        this.versionAvailable = data.data
        this.versionSelected = this.versionAvailable[0]

      }).catch(e => {
        this.$Message.error(e)
      })
    },
    check_info(host) {
      this.$Loading.start();
      this.$Spin.show();
      checkRPM(host, this.componentType, this.inventoryName).then(data => {
        this.$Loading.finish();
        this.$Spin.hide();
        let rpmInfoData = data.data
        for (let i in rpmInfoData) {
          console.log(this.$refs[rpmInfoData[i].host])
          for (let j in this.$refs[rpmInfoData[i].host]) {
            if (rpmInfoData[i].yumstate) {
              this.$refs[rpmInfoData[i].host][j].text = rpmInfoData[i].version
            } else {
              this.$refs[rpmInfoData[i].host][j].text = rpmInfoData[i].version
              this.$refs[rpmInfoData[i].host][j].type = "normal"
            }
          }
        }
      }).catch(e => {
        this.$Loading.error();
        this.$Spin.hide();
        this.$Message.error(e)
      })
    },


    undeploy_software(host){
      this.showStatusDrawer = true;
      this.$Spin.show()
      this.runningStatus = "开始运行任务"
      this.runningResult = ""
      undeploySoftware(host, this.componentType, this.inventoryName).then(data => {
        this.$Spin.hide()
        if (checkHTTPStatus(data, this.$Message)) {
          let result = data.data
          this.runningStatus = ""
          this.runningResult = result.message
          this.check_info(host)
        } else {
          this.showStatusDrawer = false
        }
      }).catch(e => {
        this.$Spin.hide()
        this.$Message.error(e)
      })
    },
    deploy_software(host, isDeploy){
      this.showStatusDrawer = true;
      this.$Spin.show()
      this.runningStatus = "开始运行任务"
      this.runningResult = ""
      deploySoftware(host, this.componentType, this.inventoryName, this.versionSelected).then(data => {
        this.$Spin.hide()
        if (checkHTTPStatus(data, this.$Message)) {
          let result = data.data
          this.runningStatus = ""
          this.runningResult = result.message
          this.check_info(host)
        } else {
          this.showStatusDrawer = false
        }
      }).catch(e => {
        this.$Spin.hide()
        this.$Message.error(e)
      })
    }
  }
}
</script>

<style>
</style>
