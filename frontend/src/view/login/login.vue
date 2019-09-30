<template>
    <div class="login" @keydown.enter="handleEnter">
        <div class="login-wrapper">
            <div class="login-header">
                <img :src="Logo" key="login-logo" alt="" class="logo">
                <div class="split"></div>
                <strong class="system-name">统一配置管理平台</strong>
            </div>
            <div class="login-content">
                <div class="login-form">
                    <div class="form-header">
                        <div class="form-header-item active">账号登录</div>
                        <span class="split"></span>
                    </div>
                    <div class="form-con">
                        <login-form ref="loginForm" @on-success-valid="handleSubmit"></login-form>
                    </div>
                </div>
            </div>
            <div class="login-footer">
                <p>安全小提示：内勤用户请使用办公电脑开机账号，密码登录；</p>
                <p>如您未获授权使用此私人电话系统，请立即离开。在未发通知或未获允许情况下，所有系统行为会受监控及记录。</p>
            </div>
        </div>
    </div>
</template>

<script>/* eslint-disable */
  import LoginForm from '_c/login-form'
  import { mapActions } from 'vuex'
  import Logo from '@/assets/images/logo-max-dark.png'

  export default {
    components: {
      LoginForm
    },
    data () {
      return {
        Logo
      }
    },
    methods: {
      ...mapActions([
        'handleLogin',
        'getUserInfo'
      ]),
      handleEnter () {
        this.$refs.loginForm.handleSubmit()
      },
      handleSubmit ({ userName, password }) {
        this.$Loading.start()
        this.handleLogin({ userName, password }).then(res => {
          this.$Loading.finish()
          this.$router.push({
            name: 'home'
          })
        }).catch(e => {
          this.$Loading.error()
          const { response } = e
          const content = response ? response.data.message : this.$t('login_incorrect')
          console.log(content)
          if (response.status === 401) {
            this.$Modal.error({
              title: this.$t('info'),
              content
            })
          } else {
            console.error(e)
          }
        })
      }
    }
  }
</script>

<style lang="less" scoped>
    @import './login.less';
</style>
