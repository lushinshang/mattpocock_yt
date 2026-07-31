#!/bin/bash
# 下載一批 YouTube 影片的英文字幕（含自動語音辨識字幕），存到 subtitles/en/<id>.srt
# 用法：
#   scripts/download_subtitles.sh <video_id> [video_id ...]
#   scripts/download_subtitles.sh -f id_list.txt   # 每行一個 video id
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT_DIR="$PROJECT_ROOT/subtitles/en"

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

mkdir -p "$OUT_DIR"

for id in "${IDS[@]}"; do
  target="$OUT_DIR/$id.srt"
  if [ -f "$target" ]; then
    echo "跳過（已存在）：$target"
    continue
  fi

  echo "下載中：$id"
  yt-dlp --skip-download \
    --write-sub --write-auto-sub \
    --sub-lang en --sub-format srt \
    -o "$OUT_DIR/$id.%(ext)s" \
    "https://www.youtube.com/watch?v=$id"

  # yt-dlp 會把字幕存成 <id>.en.srt（語言碼夾在副檔名前），正規化成 <id>.srt
  if [ -f "$OUT_DIR/$id.en.srt" ]; then
    mv "$OUT_DIR/$id.en.srt" "$target"
    echo "完成：$target"
  else
    echo "警告：$id 沒有抓到任何英文字幕（可能連自動字幕都沒有）" >&2
  fi
done
