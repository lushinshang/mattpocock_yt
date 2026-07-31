#!/bin/bash
# 把專案內以 YouTube video ID 命名的檔案/資料夾，統一改成語意化 slug 命名
# 用法：
#   scripts/rename_to_slug.sh <id:slug 對照表檔案>
#
# 對照表格式（每行一組，冒號分隔）：
#   n0VhIVtviC0:prototype-not-specs
#   3MP8D-mdheA:ai-deslop-codebase
#
# 會改名的資產：
#   guides_md/<id>.md              -> guides_md/<slug>.md
#   guides/images/<id>/            -> guides/images/<slug>/
#   subtitles/zh-TW/<id>.srt       -> subtitles/zh-TW/<slug>.srt
#   subtitles/en/<id>.srt          -> subtitles/en/<slug>.srt
#   subtitles/en/<id>.en.srt       -> subtitles/en/<slug>.en.srt      （舊資料相容，新資料通常沒有）
#   subtitles/en/<id>.en-orig.srt  -> subtitles/en/<slug>.en-orig.srt （舊資料相容，新資料通常沒有）
#
# 冪等：來源檔不存在、但目標檔已存在，視為「已經改過名」，跳過不報錯。
#
# 這支腳本【不會】改 guides/<slug>.html 內的圖片路徑、也不會改 index.html 的連結，
# 因為那兩份檔案改名當下可能還沒產生（html 是後面 md_to_html 階段才產出的），
# 跑完會列出「還需要人工/subagent 同步」的清單，由後續步驟處理。
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

usage() {
  echo "用法：$0 <id:slug 對照表檔案>" >&2
  exit 1
}

[ $# -eq 1 ] || usage
MAP_FILE="$1"
[ -f "$MAP_FILE" ] || { echo "找不到對照表：$MAP_FILE" >&2; exit 1; }

# 注意：這支腳本刻意不用 bash 陣列彙整「待同步清單」——macOS 內建的 bash 3.2
# 在 `set -u` + 陣列展開的某些組合下有已知的不穩定行為（同樣的程式碼多跑幾次
# 結果不一致）。改成邊跑迴圈邊即時印出，行為單純、可預期。
SYNC_NOTE_FILE="$(mktemp)"
trap 'rm -f "$SYNC_NOTE_FILE"' EXIT

move_if_needed() {
  local src="$1" dst="$2"
  if [ -e "$dst" ]; then
    if [ -e "$src" ]; then
      echo "  已存在目標，來源也還在，手動確認：$src vs $dst" >&2
    fi
    return
  fi
  if [ -e "$src" ]; then
    mv "$src" "$dst"
    echo "  改名：$src -> $dst"
  fi
}

while IFS=":" read -r id slug; do
  id="$(echo "$id" | xargs)"
  slug="$(echo "$slug" | xargs)"
  [ -z "$id" ] && continue
  echo "=== $id -> $slug ==="

  move_if_needed "guides_md/$id.md" "guides_md/$slug.md"
  move_if_needed "guides/images/$id" "guides/images/$slug"
  move_if_needed "subtitles/zh-TW/$id.srt" "subtitles/zh-TW/$slug.srt"
  move_if_needed "subtitles/en/$id.srt" "subtitles/en/$slug.srt"
  move_if_needed "subtitles/en/$id.en.srt" "subtitles/en/$slug.en.srt"
  move_if_needed "subtitles/en/$id.en-orig.srt" "subtitles/en/$slug.en-orig.srt"

  if [ -f "guides/$slug.html" ]; then
    echo "檢查圖片路徑：guides/$slug.html 內的 images/<id>/ 需要改成 images/<slug>/" >> "$SYNC_NOTE_FILE"
  fi
  if grep -q "$id" index.html 2>/dev/null; then
    echo "檢查連結：index.html 內含 $id -> $slug 這組對照，guides/ 與 subtitles/ 連結需要同步改成 slug" >> "$SYNC_NOTE_FILE"
  fi
done < "$MAP_FILE"

echo
echo "===== 還需要人工/subagent 同步的項目 ====="
if [ -s "$SYNC_NOTE_FILE" ]; then
  cat "$SYNC_NOTE_FILE"
else
  echo "無（可能 guides/*.html 與 index.html 尚未產生或尚未引用這些 id）"
fi
