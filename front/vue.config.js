module.exports = {
  lintOnSave: false,
  devServer: {
    compress: true, //一切服务都启用 gzip 压缩, response header中添加Content-Encoding: gzip
    open: true, // 默认打开浏览器
    // openPage: "indexPd.html", //默认打开浏览器时的导航页面
    proxy: {
      "/api": {
        target: "http://127.0.0.1:5000",
        changeOrigin: true,
        logLevel: "debug",
        pathRewrite: { "^/api": "" }
      },
    }
  }
};
