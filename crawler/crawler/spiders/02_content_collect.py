import csv
import os
import time
import re
from playwright.sync_api import sync_playwright

# 建立用來放文字檔的資料夾
os.makedirs('article_txts', exist_ok=True)

def clean_filename(text):
    """移除非法字元，避免檔名報錯"""
    return re.sub(r'[\\/*?:"<>|]', "", text)[:50]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # 抓內文用無痕背景跑就好，速度快
    page = browser.new_page()

    # 1. 讀取階段一的 CSV
    with open('robot_report.csv', mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for idx, row in enumerate(reader):
            print(f"正在下載第 {idx+1} 篇: {row['Title']}")
            
            try:
                page.goto(row['URL'], timeout=15000)
                # 根據 TheRobotReport 的結構，內文通常在 .entry-content
                page.wait_for_selector('.entry-content', timeout=5000)
                content = page.locator('.entry-content').inner_text().strip()
                
                # 2. 組合成要給 AI 讀的格式化文本
                txt_content = (
                    # f"來源網站: {row['Source']}\n"
                    f"發布日期: {row['Date']}\n"
                    f"文章標題: {row['Title']}\n"
                    # f"文章作者: {row['Author']}\n"
                    f"文章連結: {row['URL']}\n"
                    f"----------------------------------------\n"
                    f"內文:\n{content}"
                )
                
                # 3. 存成個別的 txt 檔案
                filename = f"article_txts/{idx+1:03d}_{clean_filename(row['Title'])}.txt"
                with open(filename, 'w', encoding='utf-8') as txt_f:
                    txt_f.write(txt_content)
                    
            except Exception as e:
                print(f"❌ 該連結抓取失敗 {row['URL']}: {e}")
            
            time.sleep(1) # 溫柔爬蟲，停頓 1 秒

    browser.close()
print("🎉 階段二：所有文章已成功轉換為獨立 TXT 檔！")