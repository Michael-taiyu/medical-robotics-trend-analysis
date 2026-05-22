import os
import time
from google.genai.errors import APIError  # 引入最新的通用錯誤類別
from google import genai
from google.genai import types
from openai import OpenAI

# 1. 初始化 Gemini 或 ChatGPT 用戶端 
# 或者手動帶入: client = genai.Client(api_key="你的KEY")
client = genai.Client(api_key = "YOUR_GEMINI_API_KEY_HERE")
# client = OpenAI(api_key= "YOUR_GEMINI_API_KEY_HERE")

# 2. 讀取資料夾內所有的 txt 檔案內容
txt_folder = 'article_txts'
all_articles_text = ""

print("正在讀取所有文字檔...")
for filename in sorted(os.listdir(txt_folder)):
    if filename.endswith('.txt'):
        with open(os.path.join(txt_folder, filename), 'r', encoding='utf-8') as f:
            all_articles_text += f"\n\n=== 新文章開始 ===\n{f.read()}\n=== 新文章結束 ===\n"

# 3. 設計高價值的產業趨勢分析 Prompt
PROMPT = """
你是一位資深的醫療機器人產業分析師與風險投資人。
以下是我為你準備的醫療機器人相關新聞與文章數據庫。請仔細閱讀所有文章，並撰寫一份結構嚴謹、具備高度商業與技術價值的「醫療機器人產業趨勢分析報告」。

請嚴格依照以下框架與「年份（從數據中觀察到的年份，如2024、2025、2026）」進行歸納分析：

1. 🎯 執行摘要 (Executive Summary)
   - 用 300 字核心總結目前全球醫療機器人的最重大變革。

2. 📈 歷年發展趨勢演進 (Year-by-Year Evolution Analysis)
   請針對數據中出現的年份（例如 2024 年、2025 年、2026 年）分開論述：
   - 【2024/2025年 回顧】：當時的市場核心焦點是什麼？哪些技術（如手術輔助、物流）開始商用？
   - 【2026年 當前技術爆發點】：今年最熱門的關鍵字是什麼？（例如：AI自主化、觸覺反饋、軟體機器人、特定專科手術）。

3. 🚀 核心應用領域佔比與突破
   請幫我評估並分析以下三大板塊的進展與文章提及熱度：
   - 手術機器人 (Surgical Robots)
   - 復健與外骨骼機器人 (Rehabilitation & Exoskeletons)
   - 醫院物流與護理輔助機器人 (Hospital Logistics & Care Assistant)

4. ⚠️ 產業當前挑戰與痛點
   - 根據文章內容，業界目前面臨哪些瓶頸？（例如：FDA法規監管、高昂成本、醫生學習曲線、資安隱私問題）。

5. 🔮 未來展望 (Future Outlook)
   - 預測未來 1-2 年內，哪一個細分市場最具備爆發潛力？

請使用「繁體中文」回答，觀點要辛辣、精準、多引用數據或具體公司案例（如直覺外科 Intuitive Surgical 等，若文章中有提到）。
"""

print("🚀 正在將資料送往 Gemini 進行深度分析（這可能需要一點時間）...")

max_retries = 5    # 最大重試次數
retry_delay = 10   # 每次失敗後等待 10 秒再試

for attempt in range(max_retries):
    try:
        # 使用最新、效能最好的官方標準模型名稱
        response = client.models.generate_content(
            model='gemini-2.5-flash',  # 如果真的很擠，也可以考慮換成 'gemini-1.5-pro'
            contents=[
                PROMPT,
                all_articles_text
            ]
        )

        # 4. 將 AI 分析結果存成最後的 Markdown 報告
        output_report = '醫療機器人趨勢分析報告_Gemini.md'
        with open(output_report, 'w', encoding='utf-8') as report_f:
            report_f.write(response.text)

        print(f"🎉 階段三完成！報告已生成為 '{output_report}'")
        print("\n--- Gemini 分析摘要預覽 ---")
        print(response.text[:500] + "...\n(後面已省略，請開啟檔案查看完整報告)")
        break # 成功了，直接跳出重試迴圈

    except APIError as e:
        # 新版 SDK 的錯誤都會繼承自 APIError，我們直接檢查狀態碼
        if e.code == 503 and attempt < max_retries - 1:
            print(f"⚠️ 伺服器目前太擠 (503)，等待 {retry_delay} 秒後進行第 {attempt + 2} 次重試...")
            time.sleep(retry_delay)
        else:
            print(f"❌ 呼叫 Gemini 發生錯誤 (狀態碼 {e.code}): {e.message}")
            break
    except Exception as e:
        print(f"❌ 呼叫 Gemini API 時發生其他未知錯誤: {e}")
        break

# for Gemini  
# 使用適合處理超長文本的 gemini-2.5-pro 或 flash
# response = client.models.generate_content(
#             model='gemini-1.5-pro-latest',  # 👈 改成這一個模型看看
#             contents=[
#                 PROMPT,
#                 all_articles_text
#             ]
#         )

# # 4. 將 AI 分析結果存成最後的 Markdown 報告
# with open('醫療機器人趨勢分析報告.md', 'w', encoding='utf-8') as report_f:
#     report_f.write(response.text)

# print("🎉 階段三完成！報告已生成為 '醫療機器人趨勢分析報告.md'")
# print("\n--- AI 分析摘要預覽 ---")
# print(response.text[:500] + "...\n(後面已省略，請開啟檔案查看完整報告)")



# for ChatGPT
# try:
#     # 使用 gpt-4o 模型進行分析
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "你是一位專業的產業分析師。"},
#             {"role": "user", "content": f"{PROMPT}\n\n以下為文章數據：\n{all_articles_text}"}
#         ],
#         temperature=0.3 # 降低隨機性，讓分析更嚴謹
#     )

#     # 4. 將 AI 分析結果存成最後的 Markdown 報告
#     output_report = '醫療機器人趨勢分析報告_ChatGPT.md'
#     with open(output_report, 'w', encoding='utf-8') as report_f:
#         report_f.write(response.choices[0].message.content)

#     print(f"🎉 階段三完成！報告已生成為 '{output_report}'")
#     print("\n--- ChatGPT 分析摘要預覽 ---")
#     print(response.choices[0].message.content[:500] + "...\n(後面已省略，請開啟檔案查看完整報告)")

# except Exception as e:
#     print(f"❌ 呼叫 ChatGPT API 時發生錯誤: {e}")
#     print("請檢查你的 OpenAI API Key 是否有效，或者帳戶內是否有足夠的額度。")


