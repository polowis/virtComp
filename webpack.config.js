const path = require('path')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const webpack = require('webpack')

module.exports = {
    mode: "development",
    entry: './app/resources/js/app.js',
    output: {
        path: path.resolve(__dirname, 'app/static/js'),
        filename: 'app.js'
    },
    devServer: {
        contentBase: path.resolve(__dirname, 'app/static')
    },
    module: {
        rules:[
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.(scss|css)$/,
                use: ["vue-style-loader", "css-loader", "sass-loader"]
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude: /node_modules/
            }
        ]
    },
    resolve: {
        alias:{
            vue$: "vue/dist/vue.esm.js"
        },
        extensions: ["*", ".js", ".vue", ".json"]
    },
    plugins: [ 
        new VueLoaderPlugin()
    ],
}