import csv
from playwright.sync_api import sync_playwright

URL = "https://www.therobotreport.com/category/markets-industries/biotechnology-medical-healthcare/"

with sync_playwright() as p:
    
    browser = p.chromium.launch(
        channel="chrome",   # 🔥 使用 Microsoft Edge
        headless=False,
        slow_mo=100,
        args=["--disable-blink-features=AutomationControlled"]
    )

    # 🔥 無痕模式 = new_context (不帶任何 storage)
    context = browser.new_context()

    page = context.new_page()

    # 開啟CSV檔案
    with open('robot_report.csv', mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'URL'])

        for page_num in range (1,50):
            current_URL = URL + '/page/' + str(page_num)

            page.goto(current_URL)

        # print(page.title())
            if page_num == 1:
                input("完成驗證後按 Enter...")

        # 🔥 等真正內容出現（關鍵）
            page.wait_for_selector("article", timeout=20000)

            # 🔥 再給 JS 一點時間 render
            page.wait_for_timeout(3000)


            links = page.locator('a.entry-title-link[rel="bookmark"]')

            for i in range(links.count()):

                link = links.nth(i)

                text = link.inner_text().strip()

                href = link.get_attribute("href")

                if text:

                    print(f"Text: {text} | URL: {href}")
                    #將每筆資料寫入csv
                    writer.writerow([text, href])

    # html = page.content()
    # print(html[:1000])

    browser.close()