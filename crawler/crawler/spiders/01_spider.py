import csv
from playwright.sync_api import sync_playwright

URL = "https://www.therobotreport.com/category/markets-industries/biotechnology-medical-healthcare/"

with sync_playwright() as p:
    
    browser = p.chromium.launch(
        channel="chrome",   # 註：雖然你寫使用 Edge，但 "chrome" 渠道開出來會是 Google Chrome 喔！若要 Edge 請改 "msedge"
        headless=False,
        slow_mo=100,
        args=["--disable-blink-features=AutomationControlled"]
    )

    context = browser.new_context()
    page = context.new_page()

    # 開啟 CSV 檔案 (把標頭補上 'Date')
    with open('robot_report.csv', mode='w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Title', 'URL'])  # 🔥 這裡把 Date 補到第一個欄位了

        for page_num in range(1, 3):
            current_URL = URL + 'page/' + str(page_num) + '/'  # 補上斜線避免網站轉址
            page.goto(current_URL)

            if page_num == 1:
                input("完成驗證後按 Enter...")

            # 🔥 確保文章區塊真的載入了
            page.wait_for_selector("article", timeout=20000)
            page.wait_for_timeout(2000) # 給網頁一點緩衝時間

            # 🔥 關鍵：改用 .all() 獲取當前頁面所有的 article 元素列表
            article_list = page.locator('article').all()
            print(f"第 {page_num} 頁成功偵測到 {len(article_list)} 篇文章")

            for article in article_list:
                # 在這個文章區塊內找標題與連結
                link = article.locator('a.entry-title-link[rel="bookmark"]')
                # 在這個文章區塊內找日期標籤
                date_element = article.locator('time.entry-time')

                # 確保區塊內真的有連結存在再抓取
                if link.count() > 0:
                    title = link.inner_text().strip()
                    href = link.get_attribute("href")
                    
                    # 抓取日期文字
                    post_date = date_element.inner_text().strip() if date_element.count() > 0 else "No Date"

                    print(f"Date: {post_date} | Title: {title} | URL: {href}")
                    
                    # 寫入 CSV
                    writer.writerow([post_date, title, href])

    browser.close()