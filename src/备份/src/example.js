const puppeteer = require('puppeteer')
const sleep = require('promise.sleep')

const init = async () => {
  const browser = await puppeteer.launch({
    executablePath: 'chromium/Chromium.app/Contents/MacOS/Chromium',
    headless: false
  })
  const page = await browser.newPage()
  await page.goto('https://passport.bilibili.com/login')

  const username = await page.$('#login-username')
  await username.focus() // 定位到搜索框
  await page.keyboard.type('145215')
  const password = await page.$('#login-passwd')
  await password.focus() // 定位到搜索框
  await page.keyboard.type('145215')
  const loginBtn = await page.$('#geetest-wrap > ul > li.btn-box > a.btn.btn-login')
  await loginBtn.click()

  // page.on('load', (args) => {
  //   console.log(args)
  // })

  const imgSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_bg.geetest_absolute'
  // const imgSel = 'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute > div > canvas.geetest_canvas_slice.geetest_absolute'
  let canvas = await page.waitForSelector(imgSel)
  await sleep(1000)
  let links = await page.evaluate(imgSel => {
    console.log('1212121')
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
    return Promise.resolve(imgURL)
  }, imgSel)
  console.log('links-=-->', links)
  // if (canvas) {
  //   console.log(canvas,'1212121',canvas.innerHtml)
  //   let img = canvas.toDataURL('image/png')
  //   console.log(img)
  // }
  // let canvas = await page.$('.geetest_panel > .geetest_panel_next')
  // console.log(canvas.innerHtml)

  // await browser.close()
}

init()
