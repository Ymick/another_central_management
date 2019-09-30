
import httpRequest from '@/libs/httpRequest'
/* eslint-disable */

export const getServiceStatus = (host, component, inventory) => {
  return httpRequest.request({
    url: '/api/service/status',
    method: 'get',
    params: {
      host,
      component,
      inventory,
    }
  })
}

export const setServiceState = (host, component, inventory, state) => {
  return httpRequest.request({
    url: '/api/service',
    method: 'put',
    params: {
      host,
      component,
      inventory,
      state
    }
  })
}

export const getVersionAvailable = (component) => {
  return httpRequest.request({
    url: '/api/get_version_available',
    method: 'get',
    params: {
      component
    }
  })
}



export const checkRPM = (host, component, inventory) => {
  return httpRequest.request({
    url: '/api/check_rpm',
    method: 'get',
    params: {
      host,
      component,
      inventory
    }
  })
}


export const deploySoftware = (host, component, inventory, version) => {
  return httpRequest.request({
    url: '/api/deploy_software',
    method: 'get',
    params: {
      host,
      component,
      inventory,
      version
    }
  })
}


export const undeploySoftware = (host, component, inventory) => {
  return httpRequest.request({
    url: '/api/undeploy_software',
    method: 'get',
    params: {
      host,
      component,
      inventory
    }
  })
}