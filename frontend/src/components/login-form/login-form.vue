<template>
    <Form ref="loginForm" :model="form" :rules="rules">
        <FormItem class="form-item" prop="userName" :class="{focus: focus === 'userName'}">
            <Input
                    class="form-input"
                    v-model="form.userName"
                    placeholder="请输入用户名"
                    @on-focus="focus='userName'"
                    @on-blur="focus=''"
            >
            <span class="form-input-prepend" slot="prepend">
          <Icon class="form-input-prepend-icon" :size="16" type="person"></Icon>用户名
        </span>
            </Input>
        </FormItem>
        <FormItem class="form-item" prop="password" :class="{focus: focus === 'password'}">
            <Input
                    type="password"
                    v-model="form.password"
                    placeholder="请输入密码"
                    @on-focus="focus='password'"
                    @on-blur="focus=''"
            >
            <span class="form-input-prepend" slot="prepend">
          <Icon class="form-input-prepend-icon" :size="14" type="locked"></Icon>密&nbsp;&nbsp;&nbsp;&nbsp;码
        </span>
            </Input>
        </FormItem>
        <FormItem>
            <div class="form-item-flex">
                <Checkbox style="font-size: 14px;" label="remember password" v-model="remember">记住密码</Checkbox>
                <a href="javascript:void(0)">修改密码</a>
            </div>
        </FormItem>
        <FormItem class="form-item-submit">
            <Button class="submit-btn" html-type="submit" @click.prevent="handleSubmit" type="primary" long>登&nbsp;&nbsp;&nbsp;&nbsp;录</Button>
        </FormItem>
    </Form>
</template>
<script>/* eslint-disable */
  import {setRemPass, getRemPass, clearRemPass} from './../../libs/util'
  export default {
    name: 'LoginForm',
    props: {
      userNameRules: {
        type: Array,
        default: () => {
          return [
            {required: true, message: '账号不能为空', trigger: 'blur'}
          ]
        }
      },
      passwordRules: {
        type: Array,
        default: () => {
          return [
            {required: true, message: '密码不能为空', trigger: 'blur'}
          ]
        }
      }
    },
    data () {
      return {
        focus: 'userName',
        form: {
          userName: '',
          password: ''
        },
        remember: false
      }
    },
    computed: {
      rules () {
        return {
          userName: this.userNameRules,
          password: this.passwordRules
        }
      }
    },
    methods: {
      handleSubmit () {
        this.$refs.loginForm.validate((valid) => {
          if (valid) {
            if (this.remember) {
              setRemPass(this.form)
            } else {
              clearRemPass()
            }
            this.$emit('on-success-valid', {
              userName: this.form.userName,
              password: this.form.password
            })
          }
        })
      }
    },
    mounted () {
      const data = getRemPass()
      if (data) {
        this.remember = true
        this.form = data
      }
    }
  }
</script>

<style lang="less" scoped>
    .flex-center {
        display: flex;
        align-items: center;
    }
    .form {
        &-item {
             padding: 13px 33px;
             border-left: 6px solid transparent;
        &-flex {
             line-height: 1.3;
             padding: 0 33px;
             display: flex;
             justify-content: space-between;
             font-size: 14px;
            a {
                border-bottom: 1px solid;
            }
        }
        &.focus {
             background-color: #f2f6f9;
             border-left-color: #4197f0;
         }
        &-submit {
             padding: 0 33px;
         }
    }
    &-input {
         font-size: 14px;
    &-prepend {
     .flex-center;
         border: none;
         color: #928c91;
         font-weight: 500;
    &-icon {
         color: #d2e0ea;
         margin-right: 6px;
     }
    }
    }
    }
    .submit-btn {
        background-color: #4297ed;
        font-size: 18px;
        font-weight: bold;
        padding: 16px 9;
    }
</style>

