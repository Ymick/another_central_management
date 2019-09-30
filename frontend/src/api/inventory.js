import httpRequest from '@/libs/httpRequest'
/* eslint-disable */
export const listInventory = () => {
  return httpRequest.request({
    url: '/api/list_inventory',
    method: 'get'
  })
}

export const getInventory = (name,type) => {
  return httpRequest.request({
    url: '/api/get_inventory',
    method: 'get',
    params: {"name": name,"type":type}
  })
}
