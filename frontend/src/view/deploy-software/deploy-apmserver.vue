<template>
    <div>
        <Deployment :componentType="componentType"></Deployment>
    </div>
</template>

<script>/* eslint-disable */
    import {listInventory, getInventory} from '@/api/inventory'
    import Deployment from '@/view/components/deployment'
    export default {
      name: 'deploy-apmserver',
      components: {
        Deployment
      },
      data(){
        return {
          componentType: 'apm-server'
        }
      }

    }
</script>

<style lang="less">
    .count-style {
        font-size: 50px;
    }
</style>
