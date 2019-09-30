<template>
    <div>
        <Tabs :value="inventoryName" @on-click="get_inventory">
            <TabPane :label="infor" v-for="(infor, i) in inventoryList" :key="`infor-${i}`" :name="infor">
                <Card :bordered="false" v-for="(hosts, group) in inventoryData" :key="group">
                    <p slot="title" style="height: 35px">
                        {{group}}
                        <Button shape="circle" icon="md-download" @click="download_config(group)">配置文件下载</Button>
                    </p>
                    <Button type="primary" @click="get_config(host.name)" shape="circle" icon="md-laptop"
                            v-for="(host,i) in hosts" :key="i">{{host.name}}
                    </Button>
                </Card>
                <Divider></Divider>
                <Card style="height: 600px">
                    <p slot="title">
                        模版配置
                    </p>
                    <p>
                        <Row >
                            <Col span="4" v-for="template in templateList" :key="template">
                            <Icon type="ios-document-outline" />
                            <a @click="get_template(template)">{{template}}</a>
                            </Col>
                        </Row>

                        <Divider></Divider>
                        <Split v-model="vsplit" style="height: 600px">
                            <div slot="left" class="configuration-split-pane">
                                <div style="height: 600px">
                                    <editor v-model="templateData" @init="editorInit" lang="yaml" theme="chrome"
                                            width="100%"
                                            height="70%"></editor>

                                </div>
                            </div>
                            <div slot="right" class="configuration-split-pane">
                                <br>
                                <Row>
                                    <CheckboxGroup v-model="templateGroup" >
                                        <Checkbox :label="group" v-for="(hosts, group) in inventoryData"
                                                  :key="group">
                                        </Checkbox>
                                    </CheckboxGroup>
                                </Row>
                                <br>
                                <Row>
                                    <Col Col span="12" offset="12">
                                    <Button style="margin-right: 8px" @click="upload_config(false,true)">上传</Button>
                                    <Button type="primary" @click="upload_config(true,true)">上传并重启</Button>
                                    </Col>
                                </Row>
                            </div>
                        </Split>
                    </p>
                </Card>
            </TabPane>
        </Tabs>
        <Drawer title="运行状态" :closable="false" v-model="showStatusDrawer" width="360">
            <div v-html="runningStatus">
                <Icon type="ios-loading"/>
            </div>
            <div v-html="runningResult"></div>
        </Drawer>
        <Drawer :title="selectedHost+' : '+componentType+'.yml'" :closable="false" placement="left" width="800"
                v-model="showContentDrawer">
            <editor v-model="configurationContent" @init="editorInit" lang="yaml" theme="chrome" width="100%"
                    height="70%"></editor>
            <div class="configurationdrawer-footer">
                <Button style="margin-right: 8px" @click="upload_config(false,false)">上传</Button>
                <Button type="primary" @click="upload_config(true,false)">上传并重启</Button>
            </div>
        </Drawer>

    </div>
</template>

<script>/* eslint-disable */
import {listInventory, getInventory} from '@/api/inventory'
import {
  downloadConfig,
  getConfig,
  uploadConfig,
  uploadResetConfig,
  getTask,
  listTemplate,
  getTemplate
} from '@/api/configuration'
import {checkHTTPStatus} from '@/libs/util'
export default {
  name: 'restart',

  data () {
    return {
      vsplit: 0.65,
      selectedHost: "",
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
    this.list_template()
  },
  methods: {
    editorInit: function () {
      require('brace/ext/language_tools') //language extension prerequsite...
      require('brace/mode/yaml')
      require('brace/theme/chrome')
    },
    list_inventory() {
      listInventory().then(data => {
        this.inventoryList = data.data
        this.inventoryName = this.inventoryList[0]
        this.get_inventory(this.inventoryList[0])
      })
    },
    list_template() {
      listTemplate(this.componentType).then(data => {
        this.templateList = data.data
        this.templateName = this.templateList[0]
        this.get_template(this.templateList[0])
      })
    },
    get_inventory(inventoryName) {
      this.inventoryName = inventoryName
      getInventory(inventoryName, this.componentType).then(data => {
        this.inventoryData = data.data
      })
    },
    get_template(templateName) {
      this.templateName = templateName
      getTemplate(this.componentType, templateName).then(data => {
        this.templateData = data.data
        console.log(this.templateData)
      })
    },
    download_config(group) {
      this.showStatusDrawer = true;
      this.runningStatus = "开始运行任务"
      this.runningResult = ""
      this.hostName = group
      this.$Spin.show()
      downloadConfig(this.hostName, this.componentType, this.inventoryName).then(data => {
        this.$Spin.hide()
        if (checkHTTPStatus(data, this.$Message)) {
          let result = data.data
          this.runningStatus = ""
          for (let k in result.message) {
            this.runningResult += result.message[k]
          }
        } else {
          this.showStatusDrawer = false
        }
      }).catch((e) => {
        console.log(e)
      })
    },
    get_config(hostName){
      this.showContentDrawer = true
      this.selectedHost = hostName
      getConfig(hostName, this.componentType).then(data => {
        this.configurationContent = data.data
      }).catch((e) => {
        console.log(e)
      })

    },
    upload_config(updateOnly, template){
      this.showStatusDrawer = true;
      this.$Spin.show()
      this.runningStatus = "开始运行任务"
      this.runningResult = ""
      uploadConfig(
        this.componentType,
        template ? this.templateGroup.join(',') : this.selectedHost,
        this.inventoryName,
        template ? this.templateData : this.this.configurationContent,
        updateOnly ? updateOnly : null,
        template ? template : null
      ).then(data => {
        this.$Spin.hide()
        if (checkHTTPStatus(data, this.$Message)) {
          let result = data.data
          this.runningStatus = ""
          for (let k in result.message) {
            this.runningResult += result.message[k]
          }
        } else {
          this.showStatusDrawer = false
        }
      }).catch(
        e => {
          this.$Spin.hide()
          this.$Message.error(e)
        })

    },
    clearTimer(){
    }

  }

}
</script>

<style>

</style>