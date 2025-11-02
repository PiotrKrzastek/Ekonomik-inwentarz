const path = require('path');

module.exports = {
  entry: path.resolve(__dirname, 'app/static/src/index.js'),
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'app/static/dist'),
    publicPath: '/dist/', // dla devServer
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: { loader: 'babel-loader', options: { presets: ['@babel/preset-env'] } }
      }
    ]
  },
  mode: 'development',
  devServer: {
    static: path.resolve(__dirname, 'app/static/dist'),
    port: 8080,
    hot: true,
    allowedHosts: 'all',           // zezwala na wszystkie hosty
    headers: {                      // dodaje nagłówki CORS
      'Access-Control-Allow-Origin': '*',
    },

  }
};
