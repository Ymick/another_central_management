<template>
    <div>
        <Operation :componentType="componentType"></Operation>
    </div>
</template>

<script>/* eslint-disable */
    import {listInventory, getInventory} from '@/api/inventory'
    import Operation from '@/view/components/operation'
    export default {
      name: 'config-kafka',
      components: {
        Operation
      },
      data(){
        return {
          componentType: 'kafka'
        }
      }

    }
</script>

<style lang="less">
    .count-style {
        font-size: 50px;
    }
</style>
