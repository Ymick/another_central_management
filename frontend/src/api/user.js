import httpRequest from '@/libs/httpRequest'

export const login = ({ userName, password }) => {
  const data = {
    username: userName,
    password: password
  }
  return httpRequest.request({
    url: '/login',
    data,
    method: 'post'
  })
}

export const getUserInfo = (token) => {
  return httpRequest.request({
    url: 'get_info',
    params: {
      token
    },
    method: 'get'
  })
}

export const logout = (token) => {
  return httpRequest.request({
    url: '/logout',
    method: 'post'
  })
}

export const getNotice = () => {
  return httpRequest.request({
    url: '/api/notice',
    method: 'get'
  })
}
