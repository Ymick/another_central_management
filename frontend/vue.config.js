/**
 * Global CLI Config File
 * see https://cli.vuejs.org/config/#global-cli-config
 */

const path = require('path')

const resolve = dir => {
  return path.join(__dirname, dir)
}

module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? './' // production base url.
    : '/',
  chainWebpack: config => {
    config.resolve.alias
      .set('@', resolve('src'))
      .set('_c', resolve('src/components'))
    config.module.rule('vue')
      .use('iview-loader')
      .loader('iview-loader')
      .options({
        prefix: true
      })
  },
  devServer: {
    port: 8081,
    open: true,
    proxy: 'http://localhost:8080'
  }
}
