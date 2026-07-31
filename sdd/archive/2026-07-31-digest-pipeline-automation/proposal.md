# 提案：把重建過程規劃成可重複的 pipeline，並以 README.md 記錄

- **類別**：重構（把手動觸發的流程規劃成文件化、部分工程化的 pipeline）
- **日期**：2026-07-31

## 為什麼做

這個專案目前 12 篇導讀，從「抓字幕」到「產出 html」，是分散在多輪對話裡手動觸發完成的：yt-dlp 指令是在對話中臨時打的、12 個並行 subagent 是逐一手動派工、檔名改成 slug 是臨時寫的 shell script、發布日期是事後補查的。整個過程沒有留下任何一份「下次要重跑（例如新增一支影片）該怎麼做」的說明，連上一輪對話都才發現：專案建立後頻道又新發布了一支相關影片（`/wayfinder`，2026-07-30），目前沒有機制知道要怎麼把它排進既有 pipeline。

使用者要求把整個重建過程回顧、規劃成一套 pipeline，並明確標出哪些步驟該用工程化腳本執行（確定性高、不需要語言/內容判斷，例如下載字幕、查發布日期、改檔名）、哪些步驟該保留 subagent（需要語言與內容判斷，例如深度導讀寫作、總編輯審查、html 排版與資訊圖規劃），最終產出一份 `README.md`，內含 mermaid 流程圖，作為未來新增影片或重跑流程時的依循文件。

## 要改什麼

1. 把目前手動下的三個工程化步驟，抽成可重複執行的 shell script，放在 `scripts/`：
   - `scripts/download_subtitles.sh`：給一批 YouTube video ID，用 yt-dlp 抓英文字幕（`--write-sub --write-auto-sub --sub-lang en --sub-format srt`），存到 `subtitles/en/<id>.srt`
   - `scripts/fetch_upload_dates.sh`：給一批 video ID，用 yt-dlp 查 `upload_date`，輸出 `id,YYYY-MM-DD` 對照表（供人工填入 index.html 卡片）
   - `scripts/rename_to_slug.sh`：給一份 `id:slug` 對照表，統一改名 `guides_md/`、`guides/images/`、`subtitles/en|zh-TW/` 底下的檔案與資料夾，並列出需要人工同步修改連結的檔案清單（目前是 `guides/*.html` 內的圖片路徑、`index.html` 的連結）
2. 新增 `README.md`（放在專案根目錄），內容包含：
   - 專案總覽（這是什麼、給誰看）
   - 完整 pipeline 流程圖（mermaid flowchart），涵蓋 7 個階段：抓字幕 → 訂 slug → deep-guide 分段導讀 → 總編輯審查 → md_to_html 轉換（含資訊圖）→ 檔名/資料夾統一改名 → index.html 卡片整併
   - 每個階段標明「工程化腳本」或「AI subagent」，並說明為什麼不能/不該automation化（例如 deep-guide 寫作需要語意判斷，無法用腳本規則化）
   - 「新增一支影片」SOP：給定一個新 video ID，依序要跑哪些腳本、要派哪些 subagent、要手動確認哪些事（例如主題是否符合系列調性——上一輪發現的 `lNOQaakmyDU` 定價影片就是被人工判斷排除的案例）
   - 已知限制與人工介入點（例如：影片主題篩選目前是人工判斷、codex 資訊圖生成需要 codex CLI 先登入、index.html 卡片摘要目前是人工撰寫而非自動抓取）
3. 不改動任何現有 `guides/`、`guides_md/`、`subtitles/`、`index.html` 的既有內容，純新增文件與 script

## 影響範圍

- 新增：`README.md`（專案根目錄）
- 新增：`scripts/download_subtitles.sh`、`scripts/fetch_upload_dates.sh`、`scripts/rename_to_slug.sh`
- `sdd/digest-pipeline-automation/`（提案與任務文件）
