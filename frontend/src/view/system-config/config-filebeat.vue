<template>
    <div>
        <Configuration :componentType="componentType"></Configuration>
    </div>
</template>

<script>
/* eslint-disable */
    import {listInventory, getInventory} from '@/api/inventory'
    import Configuration from '@/view/components/configuration'
    export default {
      name: 'config-filebeat',
      components: {
        Configuration
      },
      data(){
        return {
          componentType: 'filebeat'
        }
      }

    }
</script>

<style lang="less">
    .count-style {
        font-size: 50px;
    }
</style>
