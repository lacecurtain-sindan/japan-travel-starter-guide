# Daily TikTok → site playbook (Japan Travel Starter Guide)

Goal: affiliate income (Airalo eSIM codes, Klook, Agoda). First booking/sale by 2026-11-30.
Owner: cloud株式会社. Account: TikTok @japantraveltipshp. Site: https://lacecurtain-sindan.github.io/japan-travel-starter-guide/

## Fixed facts
- Affiliate IDs on the SITE: Agoda cid=1980443, Klook aid=143218. Airalo: https://airalo.pxf.io/JAPANTIPS15 and /JAPANTIPS10.
- Airalo codes attribute sales even without a link click: JAPANTIPS15 (15% off, new users), JAPANTIPS10 (10% off, everyone). Put the code on the CTA slide and in the caption whenever the topic allows.
- TikTok bio link (set in the phone app only) still points to the old Wix site, which also has working affiliate links.
- Posting times (JST): 10:00 (US evening) and 20:00 (Asia/Australia evening). Use TikTok Studio's schedule option.
- Content format: photo carousel (TikTok Studio → 写真 tab), 1080x1440 slides drawn by src/tools/slides.js. 5–7 slides: cover, numbered tips, CTA.
- No face, no filming. English only. No copyrighted characters or film stills.

## Daily routine (one run per day)
1. **Review yesterday** (TikTok Studio → コンテンツ, and each post's analytics if available): views, likes, comments, saves, shares per post. Note which hooks/topics did best.
2. **Check affiliate dashboards** (signed in, built-in browser): partners.agoda.com/dashboard, affiliate.klook.com/ja/dashboard (過去7日間), app.impact.com (Airalo). Record clicks / sales.
3. **Trend check**: WebSearch for news that affects visitors to Japan right now (rule changes, closures, seasonal events, weather, prices), and what Japan-travel topics are being discussed. Prefer topics with a booking angle (eSIM, airport transfer, hotels, tickets that sell out, passes, tours).
4. **Plan 2 posts**: one high-reach (timely/surprising), one high-intent (directly tied to an affiliate product). Apply lessons from step 1. Avoid repeating a topic posted in the last 7 days unless it performed in the top 2.
5. **Fact-check** every number/date on official or reputable pages. If unsure, leave it out.
6. **Site**: if a post needs a guide that does not exist, add it to build.py (GUIDES + ARTICLES + GUIDE_IMG), set NEWEST, run `python3 build.py && touch docs/.nojekyll`, commit and push.
7. **Write the posts** into content/posts/YYYY-MM-DD.json (same schema as 2026-11-13.json).
8. **Upload** each post (see "Upload procedure"), schedule 10:00 and 20:00 JST.
9. **Log** results and decisions in content/log.md, commit, push.

## Upload procedure (TikTok Studio, built-in browser)
1. Navigate to https://www.tiktok.com/tiktokstudio/upload?from=webapp&tab=photo . Use resize_window 1280x900 on the tab for a full layout; reset to desktop at the end.
2. Inject the renderer: the page blocks fetching other sites (CSP), so paste the contents of src/tools/slides.js (comments stripped) into javascript_tool, then in the same call:
   `const files = await JTSG.render(post); JTSG.attach(files);` then wait ~6s and confirm the text "N枚の写真がアップロードされました".
3. Title: focus `input[placeholder^="キャッチー"]` via JS, then computer type (≤90 chars).
4. Description: focus `.public-DraftEditor-content`, put the caret at the end with a Range, computer type the text; add hashtags one by one as "#tag " (with trailing space), then press Escape.
5. Music: click the button "楽曲を追加", pick an upbeat track from おすすめ by clicking its "Use" button (e.g. "Japan Trip Finale", "Little Holiday"). Avoid gloomy titles.
6. Location: click the "Tokyo" chip under 場所 (or a more specific place if relevant).
7. Click "さらに表示". Turn on the switch next to "投稿コンテンツを開示" (input.Switch__input) and tick "ブランドコンテンツ" (affiliate promotion). Leave "AI生成コンテンツ" off (slides are drawn graphics).
8. Schedule: click `input.Radio__input[value=schedule]`. Time input is `input.TUXTextInputCore-input` with value HH:MM. Click it, then in `.tiktok-timepicker-option-list` (24 items = hours, 12 items = minutes) click the innermost leaf element whose text is the hour; reopen and click the minute leaf. Verify the input value. Date input next to it (YYYY-MM-DD) defaults to today.
9. Click the last visible button "投稿予約する". The page goes to /tiktokstudio/content; confirm the row shows the scheduled time.
10. To abandon a draft: "破棄" then confirm "編集を破棄".

## Slide writing rules
- Cover: kicker (who it is for) + 3–6 word title that creates curiosity + one-line promise.
- One idea per tip slide; title ≤ 6 words; body ≤ 2 short sentences; highlight the key phrase with [[ ]].
- Last slide: save/follow prompt + code (when relevant) + "Link in bio".
- Captions: 1–2 sentence summary, the code (if relevant), "(Contains an affiliate code.)" or "(Affiliate code: we may earn a commission at no extra cost to you.)", 5–6 hashtags (#japantravel #japantips + topic tags).
