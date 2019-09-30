<template>
    <div>
        <Tabs :value="inventoryName" @on-click="get_inventory">
            <TabPane :label="infor" v-for="(infor, i) in inventoryList" :key="`infor-${i}`" :name="infor">
                <Tabs  type="card" :value="configFileName" v-model="configFileName">
                    <TabPane :label="cType" v-for="(cType, i) in configType" :key="`cType-${i}`" :name="cType">
                        <Card :bordered="false" v-for="(hosts, group) in inventoryData" :key="group">
                            <p slot="title" style="height: 35px">
                                {{group}}
                                <Button shape="circle" icon="md-download" @click="download_config(group)">配置文件下载
                                </Button>
                            </p>
                            <Button type="primary" @click="get_config(host.name)" shape="circle" icon="md-laptop"
                                    v-for="(host,i) in hosts" :key="i">{{host.name}}
                            </Button>
                        </Card>
                    </TabPane>
                </Tabs>
                <Divider></Divider>
                <Card style="height: 600px">
                    <p slot="title">
                        模版配置
                    </p>
                    <p>
                        <Row>
                            <Col span="4" v-for="template in templateList" :key="template">
                            <Icon type="ios-document-outline"/>
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
                                    <CheckboxGroup v-model="templateGroup">
                                        <Checkbox :label="group" v-for="(hosts, group) in inventoryData"
                                                  :key="group">
                                        </Checkbox>
                                    </CheckboxGroup>
                                </Row>
                                <br>
                                <Row>
                                    <Col Col span="12" offset="12">
                                    <Button style="margin-right: 8px" @click="upload_config(true,true)">上传</Button>
                                    <Button type="primary" @click="upload_config(false,true)">上传并重启</Button>
                                    </Col>
                                </Row>
                            </div>
                        </Split>
                    </p>
                </Card>
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
        <Drawer :title="selectedHost+' : '+configFileName" :closable="false" placement="left" width="600"
                v-model="showContentDrawer">
            <editor v-model="configurationContent" @init="editorInit" lang="yaml" theme="chrome" width="100%"
                    height="70%"></editor>
            <div class="configurationdrawer-footer">
                <Button style="margin-right: 8px" @click="upload_config(true,false)">上传</Button>
                <Button type="primary" @click="upload_config(false,false)">上传并重启</Button>
            </div>
        </Drawer>

    </div>
</template>

<script>/* eslint-disable */
import {listInventory, getInventory} from '@/api/inventory'
import {
  listConfig,
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
  name: 'configuration',
  components: {
    editor: require('vue2-ace-editor')
  },
  props: [
    'componentType'
  ],
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
      configFileName: "",
      configType: [],
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
    this.list_config()
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
      }).catch(e => {
        this.$Message.error(e)
      })
    },
    list_config() {
      listConfig(this.componentType).then(data => {
        this.configType = data.data
        this.configFileName = this.configType[0]
      }).catch(e => {
        this.$Message.error(e)
      })
    },
    list_template() {
      listTemplate(this.componentType).then(data => {
        this.templateList = data.data
        this.templateName = this.templateList[0]
        this.get_template(this.templateList[0])
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
    get_template(templateName) {
      this.templateName = templateName
      getTemplate(this.componentType, templateName).then(data => {
        this.templateData = data.data
      }).catch(e => {
        this.$Message.error(e)
      })
    },
    download_config(group) {
      this.showStatusDrawer = true;
      this.runningStatus = "开始运行任务"
      this.runningResult = ""
      this.hostName = group
      this.$Spin.show()
      downloadConfig(this.hostName, this.componentType, this.inventoryName, this.configFileName).then(data => {
        this.$Spin.hide()
        if (checkHTTPStatus(data, this.$Message)) {
          let result = data.data
          this.runningStatus = ""
          this.runningResult = result.message
        } else {
          this.showStatusDrawer = false
        }
      }).catch((e) => {
        this.$Message.error(e)
      })
    },
    get_config(hostName){
      this.showContentDrawer = true
      this.selectedHost = hostName
      let filename = hostName + '-' + this.configFileName
      getConfig(filename, this.componentType).then(data => {
        this.configurationContent = data.data
      }).catch((e) => {
        this.$Message.error(e)
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
        this.configFileName,
        template ? this.templateData : this.configurationContent,
        updateOnly,
        template
      ).then(data => {
        this.$Spin.hide()
        if (checkHTTPStatus(data, this.$Message)) {
          let result = data.data
          this.runningStatus = ""
          this.runningResult = result.message
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
    .configurationdrawer-footer {
        width: 100%;
        position: absolute;
        bottom: 0;
        left: 0;
        border-top: 1px solid #e8e8e8;
        padding: 10px 16px;
        text-align: right;
        background: #fff;
    }

    .configuration-split {
        height: 800px;
        border: 1px solid #dcdee2;
    }

    .configuration-split-pane {
        padding: 10px;
    }
</style>