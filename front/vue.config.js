module.exports = {
  devServer: {
    proxy: {
      '/.netlify': {
        target: 'http://[::1]:9000'
      }
    }
  }
}