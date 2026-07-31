# 任務：digest-pipeline-automation

- [x] 任務 1：撰寫 `scripts/download_subtitles.sh`——輸入一批 video ID（檔案或參數），跑 `yt-dlp --skip-download --write-sub --write-auto-sub --sub-lang en --sub-format srt` 存到 `subtitles/en/<id>.srt`；已存在的檔案跳過並印出訊息，不覆蓋
- [x] 任務 2：撰寫 `scripts/fetch_upload_dates.sh`——輸入一批 video ID，跑 `yt-dlp --print upload_date` 轉成 `YYYY-MM-DD`，輸出 `id,slug建議,YYYY-MM-DD` 格式的 CSV 到 stdout
- [x] 任務 3：撰寫 `scripts/rename_to_slug.sh`——輸入 `id:slug` 對照表（沿用這次實際用過的格式），統一改名 `guides_md/`、`guides/images/`、`subtitles/en|zh-TW/`，跑完印出「還需要人工同步」的清單（`guides/<slug>.html` 內的圖片路徑、`index.html` 的連結）
- [x] 任務 4：畫 pipeline 全貌 mermaid flowchart（7 階段，每個節點標明「腳本」或「subagent」），先在對話裡貼給使用者確認可讀性，不要等進 README 才第一次被看到
- [x] 任務 5：撰寫 README.md 主文——專案總覽、任務 4 的 mermaid 圖、「新增一支影片」SOP（列出跑腳本的順序與對應的 subagent 派工說明）、已知限制與人工介入點
- [x] 任務 6：驗證三支腳本——用專案裡已經跑過的既有 12 支影片中任選 2 支（例如 `n0VhIVtviC0`、`3MP8D-mdheA`）重跑三支腳本，確認輸出（字幕內容、日期、改名結果）與現有檔案一致或行為符合預期（已存在檔案應跳過，不誤覆蓋）。過程中發現並修掉兩個 bash 3.2 相容性 bug（陣列在 `set -u` 下不穩定、多位元組標點緊貼變數替換時偶發截斷），已改用不依賴陣列的寫法

## 驗收條件

- 情境：當在乾淨環境下對一個新 video ID 執行 `download_subtitles.sh` → `fetch_upload_dates.sh`，就能拿到 `subtitles/en/<id>.srt` 與該影片的正確發布日期，不需要手動下 yt-dlp 指令
- 情境：當對現有 12 支影片任一支重跑 `rename_to_slug.sh`，就不會誤改已經是 slug 命名的檔案（冪等，重跑不出錯、不重複改名）
- 情境：當使用者或未來新 session 打開 `README.md`，就能看懂完整 pipeline 是什麼、新增一支影片要做哪些事、哪些步驟是腳本哪些是人工/subagent判斷，不需要回頭翻對話紀錄
- 情境：當任務 6 的驗證跑完，就能確認三支腳本在真實環境下可執行、不會破壞現有檔案
