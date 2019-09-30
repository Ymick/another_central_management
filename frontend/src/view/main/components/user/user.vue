<template>
  <div class="user-avator-dropdown">
    <Dropdown @on-click="handleClick">
      <Avatar :src="userAvator"/>
      <Icon :size="12" type="arrow-down-b"></Icon>
      <DropdownMenu slot="list">
        <DropdownItem name="logout">{{$t('login_out')}}</DropdownItem>
      </DropdownMenu>
    </Dropdown>
    <a href="javascript:void(0)" @click="loginOut">{{$t('login_out')}}</a>
  </div>
</template>

<script>
import './user.less'
import { mapActions } from 'vuex'
export default {
  name: 'User',
  props: {
    userAvator: {
      type: String,
      default: ''
    }
  },
  methods: {
    ...mapActions([
      'handleLogOut'
    ]),
    handleClick (name) {
      switch (name) {
        case 'logout':
          this.loginOut()
          break
      }
    },
    loginOut () {
      this.handleLogOut().then(() => {
        this.$router.push({
          name: 'login'
        })
      })
    }
  }
}
</script>
