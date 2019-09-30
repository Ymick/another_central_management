<template>
    <div>
        <Tabs :value="inventoryName" @on-click="get_inventory">
            <TabPane :label="infor" v-for="(infor, i) in inventoryList" :key="`infor-${i}`" :name="infor">
                <Card :bordered="false" v-for="(hosts, group) in inventoryData" :key="group">
                    <p slot="title">{{group}}</p>

                    <Button type="primary" shape="circle" icon="md-laptop" v-for="host in hosts" :key="host">{{host.name}}</Button>
                    <!--<p v-for="host in hosts" :key="host">{{host.name}}</p>-->
                </Card>
            </TabPane>
        </Tabs>

    </div>
</template>

<script>
/* eslint-disable */
    import {listInventory, getInventory} from '@/api/inventory'
    import InforCard from '_c/info-card'
    export default {
      name: 'home',
      components: {
        InforCard
      },
      data () {
        return {
          inventoryName: "",
          inventoryList: [],
          inventoryData: []
        }
      },
      mounted () {
        this.list_inventory()
      },
      methods: {
        list_inventory() {
          listInventory().then(data => {
            console.log(data)
            this.inventoryList = data.data
            this.inventoryName = this.inventoryList[0]
            this.get_inventory(this.inventoryList[0])
          })
        },
        get_inventory(hostname) {
          console.log(hostname)
          getInventory(hostname).then(data => {
            console.log(data)
            this.inventoryData = data.data
          })

        }
      }

    }
</script>

<style lang="less">
    .count-style {
        font-size: 50px;
    }
</style>
