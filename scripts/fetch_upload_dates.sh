#!/bin/bash
# 查詢一批 YouTube 影片的發布日期與標題，輸出 CSV 供填入 index.html 卡片、或作為 slug 命名參考
# 用法：
#   scripts/fetch_upload_dates.sh <video_id> [video_id ...]
#   scripts/fetch_upload_dates.sh -f id_list.txt
#
# 輸出格式（stdout，逗號分隔）：
#   video_id,upload_date(YYYY-MM-DD),naive_slug,title
#
# naive_slug 只是把英文標題做機械式轉換（小寫、去符號、空白轉連字號），
# 用來當作 slug 命名的「起點」，不是最終答案——最終 slug 應該對照該篇
# deep-guide 導讀實際下的中文標題來取，這一步需要語意判斷，本腳本不做。
set -eo pipefail

usage() {
  echo "用法：$0 <video_id> [video_id ...]" >&2
  echo "     $0 -f id_list.txt" >&2
  exit 1
}

[ $# -eq 0 ] && usage

IDS=()
if [ "$1" == "-f" ]; then
  [ $# -eq 2 ] || usage
  while IFS= read -r line; do
    line="$(echo "$line" | xargs)"
    [ -z "$line" ] && continue
    IDS+=("$line")
  done < "$2"
else
  IDS=("$@")
fi

echo "video_id,upload_date,naive_slug,title"

for id in "${IDS[@]}"; do
  raw="$(yt-dlp --skip-download --print "%(upload_date)s|||%(title)s" "https://www.youtube.com/watch?v=$id" 2>/dev/null)"
  ymd_raw="${raw%%|||*}"
  title="${raw#*|||}"

  if [ -z "$ymd_raw" ] || [ "$ymd_raw" == "NA" ]; then
    echo "$id,ERROR,ERROR,\"無法取得資料\"" >&2
    continue
  fi

  date_fmt="${ymd_raw:0:4}-${ymd_raw:4:2}-${ymd_raw:6:2}"

  slug="$(echo "$title" | tr '[:upper:]' '[:lower:]' \
    | sed -E "s/[':\"!?()]//g" \
    | sed -E 's/[^a-z0-9]+/-/g' \
    | sed -E 's/^-+|-+$//g' \
    | cut -c1-60)"

  # CSV 欄位裡的雙引號跳脫
  title_escaped="$(echo "$title" | sed 's/"/""/g')"

  echo "$id,$date_fmt,$slug,\"$title_escaped\""
done
