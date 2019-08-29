const puppeteer = require('puppeteer')
const sleep = require('promise.sleep')
const rp = require('request-promise')

const init = async () => {
  const width = 1024;
  const height = 1600;
  return puppeteer.launch({
    // executablePath: 'static/chromium/Chromium.app/Contents/MacOS/Chromium',
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false,
    'defaultViewport' : { 'width' : width, 'height' : height }
  })
}

const close = async (browser) => {
  await browser.close()
}

const downloadImg = async (page, imgCount) => {

  const imgSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_bg.geetest_absolute'
  const imgKSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_slice.geetest_absolute'
  // const imgSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_slice.geetest_absolute'
  // 等待canvas加载完成
  await page.waitForSelector(imgSel)
  await page.waitForSelector(imgKSel)
  // 等待图片渲染完成
  await sleep(2*1000)

  // 执行dom操作，将canvas下载为PNG图片
  await page.evaluate((imgSel, imgKSel) => {
    console.log('开始下载图片')
    let canvas = document.querySelector(imgSel)
    console.log(canvas)
    var MIME_TYPE = "image/png";
    var imgURL = canvas.toDataURL(MIME_TYPE);
    console.log(imgURL)
    var dlLink = document.createElement('a');
    dlLink.download = 'test';
    dlLink.href = imgURL;
    dlLink.dataset.downloadurl = [MIME_TYPE, dlLink.download, dlLink.href].join(':');

    document.body.appendChild(dlLink);
    dlLink.click();
    document.body.removeChild(dlLink);
    return Promise.resolve()
  }, imgSel, imgKSel)

  await sleep(1000)

  await page.evaluate((imgSel, imgKSel) => {
    console.log('开始下载图片')
    var MIME_TYPE = "image/png";
    let canvas1 = document.querySelector(imgKSel)
    console.log(canvas1)
    var imgURL1 = canvas1.toDataURL(MIME_TYPE);
    console.log(imgURL1)
    var dlLink1 = document.createElement('a');
    dlLink1.download = 'testBg';
    dlLink1.href = imgURL1;
    dlLink1.dataset.downloadurl = [MIME_TYPE, dlLink1.download, dlLink1.href].join(':');

    document.body.appendChild(dlLink1);
    dlLink1.click();
    document.body.removeChild(dlLink1);
    return Promise.resolve()
  }, imgSel, imgKSel)
}

const Main = async () => {
  // 打开浏览器
  let browser = await init()

  // 打开页面
  const page = await browser.newPage()
  await page.goto('https://passport.bilibili.com/login')

  for (let index = 1; index <= 5; index++) {
    try {
      // 定位到用户名输入框
      const username = await page.$('#login-username')
      await username.focus()
      await page.keyboard.type('145215')
      // 定位到密码输入框
      const password = await page.$('#login-passwd')
      await password.focus()
      await page.keyboard.type('145215')
      // 模拟点击登录按钮
      const loginBtn = await page.$('#geetest-wrap > ul > li.btn-box > a.btn.btn-login')
      await loginBtn.click()

      await downloadImg(page) // 下载图片
      await sleep(2000)
      var formData = {
        test: '/Users/zejun/Downloads/test.png',
        testBg: '/Users/zejun/Downloads/testBg.png'
      }
      console.log(formData)
      const body = await rp.post({ url: 'http://localhost:5000/predict', formData: formData, json: true })
      console.log('body-->', body, body.predict)

      const distance = body.predict


      let sideSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_slider.geetest_ready > div.geetest_slider_button'
      // let btn = await getBtnPosition(sideSel, page)
      await page.waitForSelector(sideSel)
      // 等待图片渲染完成
      await sleep(1000)
      let btn = await page.$(sideSel)
      console.log(btn.clientHeight, btn.clientWidth, btn.width, btn.innerWidth)
      let k = await page.$eval(sideSel, ele=>[ele.clientHeight, ele.clientWidth, ele.offsetTop, ele.offsetLeft])
      console.log(k)
      let btn_position = {
        btn_left: 630 + k[0],
        btn_top: 410 + k[1]
      }

      let dis = [0, 5, -5, 10, -10]
      let isTrue = false
      for (let item of dis) {
        isTrue = await DragSilder(page, parseInt(distance) + item, btn_position)
        if (isTrue) {
          break
        }
        console.log('调整偏移量，重试！')
      }

      if (isTrue) {
        break
      }

      console.log('登录失败，刷新页面重试')

      await page.reload()
    } catch (error) {
      await page.reload()
      console.log('error reload')
    } finally {
      await sleep(3000)
      const resDe = await rp.get({ url: 'http://localhost:5000/delete', json: true })
      console.log('resDe-->', resDe)
    }
  }
  // 关闭浏览器
  // await close(browser)
}

const DragSilder = async (page, distance, btn_position) => {
  const distance1 = distance - 10
  const distance2 = 10

  page.mouse.click(btn_position.btn_left,btn_position.btn_top,{delay:2000})
  page.mouse.down(btn_position.btn_left,btn_position.btn_top)
  page.mouse.move(btn_position.btn_left+distance1,btn_position.btn_top,{steps:30})
  await sleep(800)
  page.mouse.move(btn_position.btn_left+distance1+distance2,btn_position.btn_top,{steps:20})
  await sleep(800)
  page.mouse.up()
  await sleep(4000)

  let resultSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next'

  let result = await page.$eval(resultSel, ele => ele.style.display)
  console.log(distance, ' : ', result, result !== 'block')

  return result === 'none'

  // try {
  //   let resultSel1 = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo > div.geetest_panel_success.geetest_success_animate'
  //   let result1 = await page.$eval(resultSel1, ele => ele.style.display)
  //   console.log(distance, ' : ', result1, result1 === 'block')
  //   return result1 === 'block'
  // } catch (error) {
  //   console.log(distance, ' : 失败')
  //   return false
  // }
}

 /**
  * 计算滑块位置
 */
async function getBtnPosition(side, page) {
  const btn_position = await page.evaluate((side) => {
    const dom = document.querySelector(side)
    console.log(dom)
    let clientWidth = dom.clientWidth
    let clientHeight = dom.clientHeight
    return {btn_left:clientWidth/2-104,btn_top:clientHeight/2+59}
  })
  return btn_position;
 }

const chongIMG = async (page) => {
  const chongBtnSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo > div.geetest_panel_error > div.geetest_panel_error_content'
  let chongBtn = await page.$(chongBtnSel).catch(async () => {
    console.log('2222222222')
    await page.reload()
  })
  if (chongBtn) {
    chongBtn.click()
  }
}

const refreshIMG = async (page) => {
  const refreshBtnSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_panel > div > a.geetest_refresh_1'
  let refreshBtn = await page.$(refreshBtnSel).catch(async () => {
    console.log('1111111111')
    await page.reload()
  })
  if (!refreshBtn) {
    await chongIMG(page)
    await sleep(1000)
    await page.waitForSelector(refreshBtnSel)
    await sleep(1000)
    refreshBtn = await page.$(refreshBtnSel)
  }
  refreshBtn.click()
}

const closeIMG = async (page) => {
  const closeBtnSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_panel > div > a.geetest_close'
  let closeBtn = await page.$(closeBtnSel).catch(async () => {
    console.log('xsjhdcbshdbcjshd')
    await page.reload()
  })
  if (!closeBtn) {
    await chongIMG(page)
    await sleep(1000)
    await page.waitForSelector(closeBtnSel)
    await sleep(1000)
    closeBtn = await page.$(closeBtnSel)
  }
  closeBtn.click()
}

Main()
