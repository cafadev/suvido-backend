const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const WebpackShellPluginNext = require('webpack-shell-plugin-next');


module.exports = (env, argv) => {

  const plugins = [
    new MiniCssExtractPlugin({
      filename: '../css/main.css',
    }),
  ]

  const shellCommands = {
    // onBeforeBuild: {
    //   scripts: ['rm -R assets/suvido/*'],
    //   blocking: true,
    // }
  }

  if (argv.mode === 'development') {
    shellCommands.onAfterDone = {
      scripts: ['python manage.py collectstatic --no-input --clear'],
      blocking: true,
      parallel: false,
    }
  }

  plugins.push(new WebpackShellPluginNext(shellCommands))

  return {
    entry: './src/index.js',

    output: {
      filename: 'main.js',
      path: __dirname + '/assets/suvido/js'
    },
    module: {
      rules: [
        {
          test: /\.js?$/,
          loader: "babel-loader",
          exclude: /node_modules/,
        },
        {
          test: /\.js$/i,
          include: path.resolve(__dirname, 'src'),
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env'],
            },
          },
        },
        {
          test: /\.css$/,
          use: [
            MiniCssExtractPlugin.loader,
            'css-loader',
            'postcss-loader'
          ],
        },
      ],
    },
    plugins
  }
}