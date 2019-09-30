import Vue from 'vue'
import Router from 'vue-router'
import routes from './routers'
import store from '@/store'
import iView from 'iview'
import { canAccessTo, clearUser, getUser } from '@/libs/util'

window.$bus = new Vue() // 全局消息总线，可以方便地发送/接收全局事件

Vue.use(Router)
const router = new Router({
  routes,
  mode: 'hash'
})
const LOGIN_PAGE_NAME = 'login'
window.$bus.$on('login_exp', () => { // 登录失效事件触发后，跳转到登录界面
  clearUser() // clear user in cookie
  store.commit('clearUser') // clear user in vuex store
  router.push({
    name: 'login'
  })
})
router.beforeEach((to, from, next) => {
  iView.LoadingBar.start()
  const user = getUser()
  if (!user || !user.token) {
    if (to.name !== LOGIN_PAGE_NAME) {
      next({
        name: LOGIN_PAGE_NAME
      })
    } else {
      next()
    }
  } else {
    if (to.name === LOGIN_PAGE_NAME) {
      next({
        name: 'home'
      })
    } else {
      const access = store.state.user.access
      if (canAccessTo(to.name, access, routes)) {
        next()
      } else {
        next({ replace: true, name: 'error_401' })
      }
    }
  }
})

router.afterEach(to => {
  iView.LoadingBar.finish()
  window.scrollTo(0, 0)
})

export default router
