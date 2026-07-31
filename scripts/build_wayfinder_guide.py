#!/usr/bin/env python3
"""Build the Wayfinder deep-guide HTML from its reviewed Markdown source."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "guides_md" / "wayfinder-project-planning.md"
OUTPUT = ROOT / "guides" / "wayfinder-project-planning.html"

TITLE = "不是把大專案切小就好：Wayfinder 真正管理的是「現在還不能決定的事」"
DESCRIPTION = "Wayfinder 如何用決策票、Frontier 與 Fog，管理跨多次 AI session 的大型專案規劃。"

FIGURES = {
    "一張地圖，不是一份提早寫完的待辦清單": """
<figure class="section-figure has-mobile">
  <picture>
    <source media="(max-width: 640px)" srcset="images/wayfinder-project-planning/section_1-mobile.png">
    <img src="images/wayfinder-project-planning/section_1.png" alt="Wayfinder 以 Frontier 與 Fog 管理大型專案中的已知與未知" loading="lazy">
  </picture>
  <figcaption>每完成一項決策，阻塞解除，能可靠處理的 Frontier 才向迷霧深處推進。</figcaption>
</figure>""",
    "四種決策票，代表四種不同的「不知道」": """
<figure class="section-figure has-mobile">
  <picture>
    <source media="(max-width: 640px)" srcset="images/wayfinder-project-planning/section_2-mobile.png">
    <img src="images/wayfinder-project-planning/section_2.png" alt="Wayfinder 的研究、原型、盤問與任務四種決策票" loading="lazy">
  </picture>
  <figcaption>先辨認缺的是事實、回饋、人的選擇或必要動作，再採用對應的處理方式。</figcaption>
</figure>""",
}


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)


def render_markdown(markdown: str) -> tuple[str, list[tuple[str, str]]]:
    body: list[str] = []
    toc: list[tuple[str, str]] = []
    in_list = False
    section_number = 0

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line.startswith("# "):
            continue
        if not line:
            if in_list:
                body.append("</ul>")
                in_list = False
            continue
        if line.startswith("## "):
            if in_list:
                body.append("</ul>")
                in_list = False
            section_number += 1
            heading = line[3:]
            anchor = f"s{section_number}"
            toc.append((anchor, heading))
            body.append(f'<h2 id="{anchor}">{inline_markup(heading)}</h2>')
            if heading in FIGURES:
                body.append(FIGURES[heading].strip())
            continue
        if line.startswith("- "):
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{inline_markup(line[2:])}</li>")
            continue
        if in_list:
            body.append("</ul>")
            in_list = False
        body.append(f"<p>{inline_markup(line)}</p>")

    if in_list:
        body.append("</ul>")
    return "\n".join(body), toc


article, toc_entries = render_markdown(SOURCE.read_text(encoding="utf-8"))
toc_links = "".join(
    f'<a href="#{anchor}">{html.escape(label)}</a>' for anchor, label in toc_entries
)

document = f"""<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(TITLE)}｜Matt Pocock AI 工作流深度導讀</title>
<meta name="description" content="{html.escape(DESCRIPTION)}">
<style>
:root{{color-scheme:light dark;}}
*{{box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
html,body{{margin:0;padding:0;}}
body{{
  background:#f7f5f1;color:#1b1d22;
  font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;
  font-size:16.5px;line-height:1.7;letter-spacing:0;
}}
@media (prefers-color-scheme:dark){{
  body{{background:#171819;color:#e9e7e2;}}
}}
.hero{{max-width:1120px;margin:0 auto;padding:58px 24px 34px;}}
.eyebrow{{
  max-width:760px;margin:0 auto 14px;color:#147d76;
  font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
}}
h1{{
  max-width:760px;margin:0 auto;color:#101b27;
  font-size:clamp(2.05rem,4vw,3.25rem);font-weight:850;
  line-height:1.24;text-wrap:balance;
}}
.dek{{
  max-width:760px;margin:20px auto 0;color:#59616b;
  font-size:17px;line-height:1.65;
}}
@media (prefers-color-scheme:dark){{
  .eyebrow{{color:#5ec6bc;}}
  h1{{color:#f5f1e9;}}
  .dek{{color:#b8bbb9;}}
}}
nav.toc{{
  position:sticky;top:0;z-index:50;
  background:rgba(247,245,241,.92);backdrop-filter:blur(8px);
  border-block:1px solid rgba(16,27,39,.09);
}}
nav.toc .toc-inner{{
  max-width:1120px;height:58px;margin:0 auto;padding:0 24px;
  display:flex;align-items:center;gap:6px;overflow-x:auto;
  scrollbar-width:thin;
}}
nav.toc a{{
  flex:0 0 auto;padding:8px 12px;border-radius:999px;
  color:#4f5a64;text-decoration:none;white-space:nowrap;font-size:13.5px;
}}
nav.toc a:hover{{background:rgba(20,125,118,.11);color:#147d76;}}
@media (prefers-color-scheme:dark){{
  nav.toc{{background:rgba(23,24,25,.92);border-color:rgba(255,255,255,.09);}}
  nav.toc a{{color:#b9bcb9;}}
  nav.toc a:hover{{background:rgba(94,198,188,.14);color:#72d5cb;}}
}}
article{{max-width:760px;margin:0 auto;padding:42px 24px 26px;}}
article p{{margin:0 0 22px;line-height:1.72;}}
article h2{{
  margin:54px 0 20px;color:#102737;
  font-size:clamp(1.42rem,2.6vw,1.95rem);line-height:1.36;
  font-weight:820;text-wrap:balance;scroll-margin-top:78px;
}}
article ul{{margin:0 0 26px;padding-left:1.35em;}}
article li{{margin:0 0 11px;padding-left:.2em;}}
article strong{{color:#0c645e;}}
@media (prefers-color-scheme:dark){{
  article h2{{color:#f0eee7;}}
  article strong{{color:#72d5cb;}}
}}
figure.section-figure{{width:min(860px,calc(100vw - 48px));margin:36px 50%;transform:translateX(-50%);}}
figure.section-figure img{{
  display:block;width:100%;aspect-ratio:16/9;object-fit:contain;
  border-radius:14px;box-shadow:0 8px 28px rgba(16,27,39,.12);
  background:#eee9df;cursor:zoom-in;
}}
figure.section-figure figcaption{{
  max-width:720px;margin:11px auto 0;color:#6c7379;
  font-size:13.5px;line-height:1.55;text-align:center;
}}
@media (prefers-color-scheme:dark){{
  figure.section-figure figcaption{{color:#aaaead;}}
}}
.source{{
  max-width:760px;margin:22px auto 0;padding:24px 24px 64px;
  border-top:1px solid rgba(16,27,39,.1);color:#777d80;font-size:13.5px;
}}
.source a{{color:#147d76;}}
@media (prefers-color-scheme:dark){{
  .source{{border-color:rgba(255,255,255,.1);color:#999e9d;}}
  .source a{{color:#72d5cb;}}
}}
.lightbox{{
  display:none;position:fixed;inset:0;z-index:200;
  align-items:center;justify-content:center;padding:24px;
  background:rgba(8,12,15,.9);cursor:zoom-out;
}}
.lightbox.is-open{{display:flex;}}
.lightbox img{{
  width:auto;height:auto;max-width:96vw;max-height:92vh;
  border-radius:8px;box-shadow:0 12px 48px rgba(0,0,0,.45);
}}
.lightbox-hint{{
  position:absolute;top:18px;right:24px;color:rgba(255,255,255,.78);
  font-size:14px;
}}
@media (max-width:640px){{
  .hero{{padding:40px 20px 25px;}}
  h1{{font-size:clamp(1.95rem,10vw,2.55rem);}}
  .dek{{font-size:16px;}}
  nav.toc .toc-inner{{height:56px;padding:0 14px;}}
  article{{padding:30px 20px 18px;}}
  article h2{{margin:43px 0 17px;scroll-margin-top:72px;}}
  figure.section-figure{{width:min(360px,calc(100vw - 32px));margin-block:30px;}}
  figure.section-figure.has-mobile img{{aspect-ratio:9/16;}}
  figure.section-figure figcaption{{padding:0 4px;text-align:left;}}
  .source{{padding:22px 20px 48px;}}
}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto;}}}}
</style>
</head>
<body>
<header class="hero">
  <div class="eyebrow">Matt Pocock AI 工作流深度導讀</div>
  <h1>{html.escape(TITLE)}</h1>
  <p class="dek">大型工作真正難的，不是任務太多，而是許多決定必須等研究、原型或人的選擇完成後，才有資格被做出。</p>
</header>
<nav class="toc" aria-label="文章段落"><div class="toc-inner">{toc_links}</div></nav>
<main>
<article>
{article}
</article>
<footer class="source">
  深度導讀・資料來源：
  <a href="https://www.youtube.com/watch?v=F3lL98Pj90o" target="_blank" rel="noopener">/wayfinder: Nothing is too big to plan anymore</a>
  ・<a href="../index.html">回到系列目錄</a>
</footer>
</main>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="放大資訊圖" aria-hidden="true">
  <span class="lightbox-hint">點擊或按 Esc 關閉</span>
  <img src="" alt="">
</div>
<script>
(function(){{
  var lightbox=document.getElementById("lightbox");
  var lightboxImg=lightbox.querySelector("img");
  function openLightbox(img){{
    lightboxImg.src=img.currentSrc||img.src;
    lightboxImg.alt=img.alt;
    lightbox.classList.add("is-open");
    lightbox.setAttribute("aria-hidden","false");
    document.body.style.overflow="hidden";
  }}
  function closeLightbox(){{
    lightbox.classList.remove("is-open");
    lightbox.setAttribute("aria-hidden","true");
    lightboxImg.src="";
    document.body.style.overflow="";
  }}
  document.querySelectorAll("figure.section-figure img").forEach(function(img){{
    img.addEventListener("click",function(){{openLightbox(img);}});
  }});
  lightbox.addEventListener("click",closeLightbox);
  document.addEventListener("keydown",function(event){{
    if(event.key==="Escape"&&lightbox.classList.contains("is-open"))closeLightbox();
  }});
}})();
</script>
</body>
</html>
"""

OUTPUT.write_text(document, encoding="utf-8")
print(OUTPUT)
