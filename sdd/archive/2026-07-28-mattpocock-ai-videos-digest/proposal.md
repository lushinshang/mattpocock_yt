# 提案：Matt Pocock AI 工作流影片字幕翻譯與深度導讀網站建立

- **類別**：新功能
- **日期**：2026-07-27

## 為什麼做
Matt Pocock 頻道在近兩個月內發布了 12 部關於 AI 輔助程式開發工作流（AI Coding Skills, Claude Code, Cursor, De-slop）的優質影片。為了方便繁體中文讀者快速吸收這些前沿 AI 工具與工作流經驗，需要將這些影片下載字幕、翻譯為台灣 IT/AI 慣用語的繁體中文 SRT，並透過 `deep-guide` 產出美觀獨立的導讀 HTML 頁面及總目錄。

## 要改什麼
1. 使用 `yt-dlp` 下載 12 部影片的英文 `.srt` 字幕檔。
2. 調用/派發多個 Subagent 並行將 12 部影片字幕翻譯為台灣 IT/AI 領域慣用語的繁體中文 `.srt`。
3. 套用 `deep-guide` 技能，將各影片的字幕與精華轉化為獨立的深度導讀 HTML 網頁。
4. 建立總目錄頁面 `index.html`，雙向連結各導讀 HTML 網頁與對應的中文 SRT 字幕。

## 影響範圍
- `subtitles/` (新增：12 部影片之英文與中文 srt 檔案)
- `guides/` (新增：12 部影片之深度導讀 HTML 檔案)
- `index.html` (新增：總目錄網頁)
- `sdd/mattpocock-ai-videos-digest/` (提案與任務文件)
