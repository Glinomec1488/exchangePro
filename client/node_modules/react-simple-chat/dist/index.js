
'use strict'

if (process.env.NODE_ENV === 'production') {
  module.exports = require('./react-simple-chat.cjs.production.min.js')
} else {
  module.exports = require('./react-simple-chat.cjs.development.js')
}
