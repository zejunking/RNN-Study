const puppeteer = require('puppeteer')
const sleep = require('promise.sleep')

const init = async () => {
  const width = 1024;
  const height = 1600;
  return puppeteer.launch({
    executablePath: 'chromium/Chromium.app/Contents/MacOS/Chromium',
    headless: false,
    'defaultViewport' : { 'width' : width, 'height' : height }
  })
}

const close = async (browser) => {
  await browser.close()
}

const downloadImg = async (page) => {

  const imgSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_bg.geetest_absolute'
  // const imgSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_slice.geetest_absolute'
  // 等待canvas加载完成
  await page.waitForSelector(imgSel)
  // 等待图片渲染完成
  await sleep(1000)

  // 执行dom操作，将canvas下载为PNG图片
  let links = await page.evaluate((imgSel) => {
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
  }, imgSel)
}

const Main = async () => {
  // 打开浏览器
  let browser = await init()

  // 打开页面
  const page = await browser.newPage()
  await page.goto('https://www.huxiu.com/')

  // 模拟点击登录按钮
  const loginBtn = await page.$('#top > div > ul.nav.navbar-nav.navbar-right.transition > li.login-link-box > a')
  await loginBtn.click()

  let imgCount = 0
  for (let index = 0; index < 300; index++) {
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
      const loginBtn = await page.$('#top > div > ul.nav.navbar-nav.navbar-right.transition > li.login-link-box > a')
      await loginBtn.click()

      for (let i = 0; i < 5; i++) {
        await downloadImg(page) // 下载图片
        await refreshIMG(page) // 刷新图片以备下次下载
        await sleep(1000) // 休眠1000，避免刷新过于频繁
        imgCount++
      }
      await sleep(3000)
      console.log('imgCount-->', imgCount)
      // 每5次刷新页面重试
      await page.reload()
    } catch (error) {
      console.log('error reload')
    }
  }
  // 关闭浏览器
  await browser.close()
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
