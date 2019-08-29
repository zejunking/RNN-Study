const puppeteer = require('puppeteer')
const sleep = require('promise.sleep')
const rp = require('request-promise')
const fs = require('fs')

function image2Base64 (img) {
  var canvas = document.createElement('canvas')
  canvas.width = img.width
  canvas.height = img.height
  var ctx = canvas.getContext('2d')
  ctx.drawImage(img, 0, 0, img.width, img.height)
  var dataURL = canvas.toDataURL('image/png')
  return dataURL
}

async function main () {
  var img = '/Users/zejun/Downloads/test.png'

  // const fs = require('fs')
  // const path = require('path')
  // const mineType = require('mime-types') // 文件类型

  // let filePath = path.resolve('/Users/zejun/Downloads/test.png') // 如果是本地文件
  // let data = fs.readFileSync(filePath)
  // let bufferData = new Buffer(data, 'base64')
  // let base64 = 'data:' + mineType.lookup(filePath) + ';base64,' + data
  // // fs.writeFileSync(path.resolve('/Users/zejun/Downloads/test.png'), base64, err => {})
  // // fs.writeFile('your/save/file/path', base64, err => {...});

  // const buffer = Buffer.from(base64.replace('data:image/jpg;base64,', ''), 'base64')
  // fs.writeFileSync('temp.jpg',buffer)
  var formData = {
    test: '/Users/zejun/Downloads/test.png',
    testBg: '/Users/zejun/Downloads/testBg.png'
  }
  console.log(formData)
  const body = await rp.post({ url: 'http://localhost:5000/predict', formData: formData, json: true })
  console.log('body-->', body)
}

main()
