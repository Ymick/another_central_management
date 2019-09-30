/**
 * Created by lij021 on 2019/7/1.
 */

import httpRequest from '@/libs/httpRequest'
/* eslint-disable */
export const downloadConfig = (host, component, inventory,filename) => {
  return httpRequest.request({
    url: '/api/download_config',
    method: 'get',
    params: {
      host,
      component,
      inventory,
      filename
    }
  })
}

export const listConfig = (component) => {
  return httpRequest.request({
    url: '/api/list_config',
    method: 'get',
    params: {
      component
    }
  })
}

export const getConfig = (filename, component) => {
  return httpRequest.request({
    url: '/api/get_config',
    method: 'get',
    params: {
      filename,
      component
    }
  })
}

export const uploadConfig = (component, host, inventory, filename, content, updateOnly, template) => {
  return httpRequest.request({
    url: '/api/upload_config',
    method: 'post',
    params: {
      component,
      inventory,
      host,
      filename,
      updateOnly,
      template
    },
    data: content
  })
}

export const getTask = (id) => {
  return httpRequest.request({
    url: '/api/get_task',
    method: 'get',
    params: {id}
  })
}


export const listTemplate = (component) => {
  return httpRequest.request({
    url: '/api/config/list_template',
    method: 'get',
    params: {component}
  })
}

export const getTemplate = (component,filename) => {
  return httpRequest.request({
    url: '/api/config/get_template',
    method: 'get',
    params: {component,filename}
  })
}


