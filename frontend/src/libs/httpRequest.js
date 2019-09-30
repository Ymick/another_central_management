import Axios from 'axios'
import { Message } from 'iview'
import i18n from './../locale'
import qs from 'qs'
import { getUser } from '@/libs/util'
/* eslint-disable */
const conf = {
  headers: {
    'Content-Type': 'application/json; charset=utf-8'
  },
  timeout: 300000,
  baseURL: process.env.NODE_ENV === 'production'
    ? '/' // production base url
    : 'http://localhost:3389' // development base url
}

Axios.defaults.withCredentials=true;
const instance = Axios.create(conf)
instance.interceptors.request.use(config => {
  if (!config.url.includes('/login')) {
    const user = getUser()
    if (user && user.token) {
      config.headers.Authorization = 'Bearer ' + user.token
    }
  }
  return config
})
instance.interceptors.response.use(res => {
  return res
}, error => {
  // Handling Errors
  if (error.response) {
    if (error.response.status === 401 || error.response.status === 403) {
      if (!error.response.config.url.includes('/login')) {
        return Promise.reject(error)
      } else {
        Message.error(i18n.t('login_timeout'))
        window.$bus.$emit('login_exp')
        return Promise.reject('login expired.')
      }
    } else {
      if (error.response.data.message) {
        Message.error(error.response.data.message)
      } else {
        Message.error(i18n.t('ajax_error'))
      }
      return Promise.reject('ajax error:server response status ' + error.response.status)
    }
  } else if (error.request) {
    Message.error(i18n.t('ajax_error'))
    return Promise.reject('ajax error:The request was made but no response was received')
  } else {
    // Something happened in setting up the request that triggered an Error
    Message.error(i18n.t('ajax_error'))
    return Promise.reject('ajax error:' + error.message)
  }
})

export default {
  request (options) {
    return instance(options)
  },
  // 以form表单方式提交数据
  formRequest (options) {
    if (!options.data) {
      return instance({
        url: options.url,
        method: 'get'
      })
    }
    return instance({
      url: options.url,
      method: 'post',
      data: qs.stringify(options.data),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  }
}
