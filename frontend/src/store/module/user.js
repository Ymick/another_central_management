import { login, logout } from '@/api/user'
import { setUser, getUser, clearUser } from '@/libs/util'
// import face from '../../assets/images/iview-face.png'
/* eslint-disable */

const cookieUser = getUser()
export default {
  state: {
    userName: cookieUser.userName,
    userId: cookieUser.userId,
    avatorImgPath: cookieUser.avatorImgPath,
    token: cookieUser.token,
    access: cookieUser.access
  },
  mutations: {
    setAvator (state, avatorPath) {
      state.avatorImgPath = avatorPath
    },
    setUserId (state, id) {
      state.userId = id
    },
    setUserName (state, name) {
      state.userName = name
    },
    setAccess (state, access) {
      state.access = access.map(a => {
        return a.toLowerCase()
      })
    },
    setToken (state, token) {
      state.token = token
    },
    setUser (state, data) {
      const user = {
        userName: data.userName,
        token: data.token,
        userId: data.userName,
        access: data.roles.map(role => role.toLowerCase()),
        avatorImgPath: ''
      }
      state.userId = user.userId
      state.userName = user.userName
      state.avatorImgPath = user.avatorImgPath
      state.token = user.token
      state.access = user.access
      setUser(user)
    },
    clearUser (state) {
      clearUser()
      state.userId = ''
      state.userName = ''
      state.avatorImgPath = ''
      state.token = null
      state.access = []
    }
  },
  actions: {
    // 登录
    handleLogin ({ commit }, { userName, password }) {
      userName = userName.trim()
      return new Promise((resolve, reject) => {
        login({
          userName,
          password
        }).then(res => {
          console.log(res.data)
          const data = res.data
          data.userName = userName
          commit('setUser', data)
          resolve()
        }).catch(err => {
          if (err.status === 401) {
            reject('401')
          } else {
            reject(err)
          }
        })
      })
    },
    // 退出登录
    handleLogOut ({ state, commit }) {
      return new Promise((resolve, reject) => {
        if (state.token) {
          logout(state.token).then(() => {
            commit('setToken', '')
            commit('setAccess', [])
            clearUser()
            resolve()
          }).catch(err => {
            // 忽略退出登录失败的异常
            console.warn('logout error.', err)
            commit('setToken', '')
            commit('setAccess', [])
            clearUser()
            resolve()
          })
        } else {
          commit('setToken', '')
          commit('setAccess', [])
          clearUser()
          resolve()
        }
        // 如果你的退出登录无需请求接口，则可以直接使用下面三行代码而无需使用logout调用接口
        /**
         commit('setToken', null)
         commit('setAccess', [])
         clearUser()
         resolve()
         **/
      })
    },
    // 获取用户相关信息
    getUserInfo ({ state, commit }) {
      return new Promise((resolve, reject) => {
        resolve()
        getUserInfo(state.token).then(res => {
         const data = res.data
         commit('setAvator', data.avator)
         commit('setUserName', data.user_name)
         commit('setUserId', data.user_id)
         commit('setAccess', data.access)
         resolve(data)
         }).catch(err => {
         reject(err)
         })
      })
    }
  }
}
