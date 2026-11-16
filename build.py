"""Build the Japan Travel Starter Guide static site into ./docs (served by GitHub Pages).

Pages are defined in PAGES below. Run: python3 build.py
Paths are relative so the site works on GitHub Pages (user or project site) and on a custom domain.
"""
import hashlib
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs")

SITE_NAME = "Japan Travel Starter Guide"
with open(os.path.join(SRC, "assets", "style.css"), "rb") as _f:
    CSS_VER = hashlib.md5(_f.read()).hexdigest()[:8]
UPDATED = "November 2026"

# ---- Affiliate links (from the existing Wix site; keep IDs in one place) ----
AGODA_TOKYO = "https://www.agoda.com/partners/partnersearch.aspx?pcs=1&cid=1980443&hl=en-us&city=5085"
KLOOK_SKYLINER = "https://www.klook.com/activity/1410-skyliner-tokyo/?aid=143218"
AIRALO_NEW = "https://airalo.pxf.io/JAPANTIPS15"
AIRALO_ALL = "https://airalo.pxf.io/JAPANTIPS10"

AFF = 'target="_blank" rel="sponsored nofollow noopener"'
EXT = 'target="_blank" rel="noopener"'

DISCLOSURE = (
    '<p class="disclosure">This guide contains affiliate links. If you book through them, '
    'we may earn a small commission at no extra cost to you. '
    '<a href="{r}affiliate-disclosure/">How this works</a></p>'
)


def layout(title, description, body, depth, path):
    r = "../" * depth
    full_title = title if title == SITE_NAME else f"{title} | {SITE_NAME}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{r}assets/style.css?v={CSS_VER}">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r}"><img src="{LOGO}" alt="Japan Travel Starter Guide" width="160" height="73"></a>
    <nav class="site-nav"><a href="{r}start/">All guides</a></nav>
  </div>
</header>
<main>
{body.replace("{r}", r)}
</main>
<footer class="site-footer">
  <div class="wrap">
    <p class="footer-links"><a href="{r}about/">About</a><a href="{r}affiliate-disclosure/">Affiliate disclosure</a><a href="{r}privacy/">Privacy policy</a></p>
    <p>Prices and rules change. Check the official site before you travel. Last reviewed {UPDATED}.</p>
    <p>&copy; 2026 {SITE_NAME}</p>
  </div>
</footer>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Guides in journey order (one guide = one TikTok post).
# Each guide is a "station" on the route: kanji / kana / romaji like a Japanese station sign.
# ---------------------------------------------------------------------------
STAGES = [
    ("before", "Before you fly", "出発前"),
    ("landing", "Landing", "到着"),
    ("during", "During your trip", "滞在中"),
]

GUIDES = [
    {
        "slug": "where-to-stay-in-tokyo",
        "stage": "before",
        "ja": "宿", "kana": "やど",
        "short": "Where to stay",
        "title": "Where to stay in Tokyo on your first trip",
        "summary": "Shinjuku, Shibuya, Ueno/Asakusa or Tokyo Station: pick the area that fits your trip.",
    },
    {
        "slug": "japan-esim-pocket-wifi-sim",
        "stage": "before",
        "ja": "通信", "kana": "つうしん",
        "short": "Internet",
        "title": "eSIM vs pocket WiFi vs SIM card for Japan",
        "summary": "How to choose, and the phone-number detail most guides skip.",
    },
    {
        "slug": "ghibli-museum-tickets",
        "stage": "before",
        "ja": "三鷹", "kana": "みたか",
        "short": "Ghibli Museum",
        "title": "How to get Ghibli Museum tickets",
        "summary": "No tickets at the door. When sales open, what to prepare, and what to do if it sells out.",
    },
    {
        "slug": "narita-airport-to-tokyo",
        "stage": "landing",
        "ja": "成田空港", "kana": "なりたくうこう",
        "short": "Narita to Tokyo",
        "title": "Narita Airport to Tokyo: which train to take",
        "summary": "Skyliner, Access Express or N'EX. Choose by where your hotel is.",
    },
    {
        "slug": "japan-tax-free-shopping-2026",
        "stage": "during",
        "ja": "免税", "kana": "めんぜい",
        "short": "Tax-free shopping",
        "title": "Japan tax-free shopping changed on November 1, 2026",
        "summary": "You now pay full price and get the 10% back at the airport. What to do so you don't lose it.",
    },
    {
        "slug": "new-year-in-japan",
        "stage": "during",
        "ja": "正月", "kana": "しょうがつ",
        "short": "New Year",
        "title": "Visiting Japan over New Year? Read this first",
        "summary": "What closes from Dec 29 to Jan 3, when trains get packed, and how to plan around it.",
    },
]
for i, g in enumerate(GUIDES, start=1):
    g["code"] = f"{i:02d}"

# Most recently published guide (the one the latest TikTok points to).
NEWEST = "japan-tax-free-shopping-2026"


# ---- Images: the owner's own media, served from their Wix media library ----
WIX = "https://static.wixstatic.com/media/"
IMG_FUJI = "6e16e5_f6a1083d7154454d90c2bb85f5f706c2~mv2.jpg"
IMG_PHONE = "6e16e5_61c776631c7348d7b0f725e5d8653ac7~mv2.jpg"
IMG_TRAIN = "6e16e5_2bfe0a80b627441a843e3a5258298b27~mv2.jpg"
LOGO = WIX + "6e16e5_da7ef34dacdc48c297978fef254e2800~mv2.png/v1/fill/w_320,h_146,enc_auto/logo.png"


def img(media, w, h, focus="c"):
    """Wix image transform URL (crop to w x h). focus: c (center), t (top), b (bottom)."""
    return f"{WIX}{media}/v1/fill/w_{w},h_{h},al_{focus},q_75,enc_auto/photo.jpg"


GUIDE_IMG = {
    "where-to-stay-in-tokyo": (IMG_FUJI, "b"),
    "japan-esim-pocket-wifi-sim": (IMG_PHONE, "c"),
    "ghibli-museum-tickets": (IMG_FUJI, "t"),
    "narita-airport-to-tokyo": (IMG_TRAIN, "c"),
    "new-year-in-japan": (IMG_FUJI, "c"),
    "japan-tax-free-shopping-2026": (IMG_PHONE, "t"),
}


def guide_grid(r="{r}"):
    out = []
    for key, label, _ja in STAGES:
        items = [g for g in GUIDES if g["stage"] == key]
        out.append(f'<h2 class="stage">{label}</h2><div class="grid">')
        for g in items:
            media, focus = GUIDE_IMG[g["slug"]]
            new = '<span class="new">New</span>' if g["slug"] == NEWEST else ""
            out.append(
                f'<a class="tile" href="{r}guides/{g["slug"]}/">'
                f'<img src="{img(media, 720, 450, focus)}" alt="" loading="lazy" width="720" height="450">'
                f'<span class="tile-body">{new}<span class="tile-title">{g["title"]}</span>'
                f'<span class="tile-sum">{g["summary"]}</span>'
                f'<span class="tile-link">Read the guide</span></span></a>'
            )
        out.append("</div>")
    return "\n".join(out)


def article_hero(g, r="{r}"):
    media, focus = GUIDE_IMG[g["slug"]]
    return f"""
<header class="article-hero">
  <img src="{img(media, 1400, 620, focus)}" alt="" width="1400" height="620">
</header>
<div class="wrap"><h1 class="article-title">{g["title"]}</h1></div>"""


HOME = f"""
<section class="hero" style="--hero-img:url('{img(IMG_FUJI, 1800, 1000, "c")}')">
  <div class="hero-inner">
    <h1>Japan Travel Starter Guide</h1>
    <p>Simple tips for first-time visitors to Japan. Plan smarter, avoid common mistakes, and sort out your eSIM, hotel, trains and airport transfer before you arrive.</p>
    <a class="btn" href="#guides">See the guides</a>
  </div>
</section>
<section class="wrap-wide" id="guides">
{guide_grid()}
</section>
<section class="band">
  <div class="wrap">
    <h2>Need a hotel in Tokyo?</h2>
    <p>Compare prices for your dates on Agoda. Ueno and Asakusa are the easiest areas to reach from Narita Airport.</p>
    <a class="btn" href="{AGODA_TOKYO}" {AFF}>Search Tokyo hotels</a>
  </div>
</section>
"""

START = f"""
<section class="wrap-wide start">
  <h1>Guides from our TikTok</h1>
  <p class="lead">Find the guide from the video you just watched.</p>
{guide_grid()}
</section>
<section class="band">
  <div class="wrap">
    <h2>Booking links</h2>
    <a class="btn" href="{KLOOK_SKYLINER}" {AFF}>Book a Skyliner ticket (Narita to Ueno)</a>
    <a class="btn outline" href="{AIRALO_NEW}" {AFF}>Get an Airalo eSIM for Japan</a>
    <p class="codes">Airalo codes: <b>JAPANTIPS15</b> 15% off for new users, <b>JAPANTIPS10</b> 10% off for everyone</p>
    <a class="btn outline" href="{AGODA_TOKYO}" {AFF}>Search Tokyo hotels on Agoda</a>
    <p class="note">Some links are affiliate links. <a href="{{r}}affiliate-disclosure/">How this works</a></p>
  </div>
</section>
"""

ABOUT = """
<section class="article wrap">
  <h1>About</h1>
  <p>Japan Travel Starter Guide helps first-time visitors handle the practical side of a Japan trip: airport transfers, internet, tickets that sell out, where to stay, and seasonal surprises.</p>
  <p>The guides are written in Tokyo, Japan, by a team that reads Japanese sources and official pages directly, so you get the details that English summaries often miss.</p>
  <p>Every guide is checked against official sources when it is written. Prices and rules in Japan do change, so each page shows when it was last reviewed. If you spot something out of date, we want to hear about it.</p>
</section>
"""

DISCLOSURE_PAGE = """
<section class="article wrap">
  <h1>Affiliate disclosure</h1>
  <p>Some links on this site are affiliate links. If you click one and make a booking or purchase, we may earn a commission. The price you pay stays the same.</p>
  <p>Our partners currently include Agoda (hotels), Klook (tickets and transport) and Airalo (eSIM). We only link to services that are relevant to the guide you are reading.</p>
  <p>Affiliate income keeps the guides free. It does not change what we recommend: when a cheaper or simpler option exists without an affiliate link, we say so.</p>
</section>
"""

PRIVACY = """
<section class="article wrap">
  <h1>Privacy policy</h1>
  <p>This site does not ask you to create an account and does not collect your name or email address.</p>
  <h2>Analytics</h2>
  <p>We may use Google Analytics to understand which guides are read and how visitors arrive. It uses cookies and collects anonymous usage data such as pages viewed and device type. You can opt out with the <a href="https://tools.google.com/dlpage/gaoptout" target="_blank" rel="noopener">Google Analytics opt-out add-on</a>.</p>
  <h2>Affiliate links</h2>
  <p>When you click an affiliate link, the partner site (for example Agoda, Klook or Airalo) may set cookies to record that you came from this site. Their own privacy policies apply on their sites.</p>
  <h2>Changes</h2>
  <p>We may update this policy. The date at the bottom of each page shows when the site was last reviewed.</p>
</section>
"""


def article(title, lead_answer, body, sources):
    src = "".join(f'<li><a href="{u}" {EXT}>{t}</a></li>' for t, u in sources)
    src_block = f"<p><strong>Sources</strong></p><ul>{src}</ul>" if sources else ""
    return f"""
<article class="article">
  {{board}}
  <div class="wrap">
  <p class="meta">Updated {UPDATED}</p>
  {DISCLOSURE}
  <div class="answer"><p class="answer-label">Short answer</p><p>{lead_answer}</p></div>
  {body}
  <div class="note">{src_block}<p>Check the official pages before you travel. Prices and rules can change.</p></div>
  {{next}}
  </div>
</article>
"""


NARITA = article(
    "Narita Airport to Tokyo: which train should you take?",
    "Staying around Ueno or Asakusa? Take the <strong>Skyliner</strong>. Staying near Tokyo Station or Shinjuku? Take the <strong>N'EX</strong>. On a tight budget and not in a hurry? Take the <strong>Access Express</strong>.",
    f"""
<h2>The three options at a glance</h2>
<div class="table-scroll"><table>
<tr><th>Train</th><th>Best for</th><th>Time</th><th>Fare (adult)</th></tr>
<tr><td><strong>Skyliner</strong></td><td>Ueno, Asakusa, Nippori</td><td>About 36 min to Nippori, 41 min to Keisei-Ueno</td><td>¥2,580 at the station; ¥2,310 online for overseas visitors</td></tr>
<tr><td><strong>Access Express</strong></td><td>Budget, light luggage</td><td>Around 60 to 75 min to Ueno</td><td>Roughly ¥1,300, no reservation</td></tr>
<tr><td><strong>N'EX (Narita Express)</strong></td><td>Tokyo Station, Shinjuku, JR Pass holders</td><td>About 1 hour to Tokyo Station</td><td>About ¥3,000; covered by the JR Pass</td></tr>
</table></div>

<h2>Skyliner: the fastest way to Ueno</h2>
<p><strong>New from November 21, 2026:</strong> an earlier first Skyliner leaves Keisei-Ueno at 5:20 and Nippori at 5:25, reaching Narita Airport Terminal 2 at 6:01 and Terminal 1 at 6:03 (20 minutes earlier than before). It starts on November 21 for weekends and holidays and November 24 for weekdays. Useful if you have an early flight home.</p>
<p>The Skyliner runs non-stop from Narita to Nippori and Keisei-Ueno. Every seat is reserved and there is space for large suitcases. From Ueno you can reach Asakusa in a few minutes by subway.</p>
<p>The fare is made of a base fare plus a Skyliner ticket. Buying online in advance as an overseas visitor is cheaper than the station counter, and you skip the ticket queue after a long flight.</p>
<a class="btn" href="{KLOOK_SKYLINER}" {AFF}>Book a Skyliner ticket online</a>
<p>Note: a Suica or other IC card can pay the base fare, but you still need a Skyliner ticket for the reserved seat.</p>

<h2>Access Express: cheapest, but slower</h2>
<p>This Keisei train uses the same fast line for part of the way but stops more often and has no reserved seats. You can tap in with an IC card. It is a good choice if you arrive outside rush hour with light luggage.</p>

<h2>N'EX: best for Tokyo Station and Shinjuku</h2>
<p>JR's Narita Express runs directly to Tokyo Station and continues to Shinagawa, Shibuya and Shinjuku without changing trains. If you have a JR Pass, the N'EX is included, which usually makes it the obvious pick.</p>

<h2>Quick decision guide</h2>
<ul>
<li>Hotel in Ueno, Asakusa or nearby: <strong>Skyliner</strong></li>
<li>Hotel near Tokyo Station, Shinjuku or Shibuya: <strong>N'EX</strong></li>
<li>Holding a JR Pass: <strong>N'EX</strong></li>
<li>Saving money matters more than time: <strong>Access Express</strong></li>
</ul>
<p>Still choosing a hotel? Ueno and Asakusa are the easiest areas to reach from Narita. See <a href="{{r}}guides/where-to-stay-in-tokyo/">where to stay in Tokyo</a>.</p>
""",
    [
        ("Can you use Suica on the Skyliner? (Get Around Japan)", "https://www.getaroundjapan.jp/archives/2602"),
        ("Keisei Skyliner access guide (ANA)", "https://www.ana.co.jp/en/jp/guide/prepare/airport-guide/access/keisei/"),
        ("Keisei timetable change, Nov 21, 2026 (tabiris, Japanese)", "https://tabiris.com/archives/keisei-dia20261121/"),
    ],
)

ESIM = article(
    "eSIM vs pocket WiFi vs SIM card: which is best for Japan?",
    "For most solo travelers and couples with recent phones, an <strong>eSIM</strong> is the easiest: you set it up before you fly and have data the moment you land. Groups sharing one connection or travelers with older phones may prefer <strong>pocket WiFi</strong>.",
    f"""
<h2>Compare the three options</h2>
<div class="table-scroll"><table>
<tr><th>Option</th><th>Good for</th><th>Watch out for</th></tr>
<tr><td><strong>eSIM</strong></td><td>Recent phones, solo or couples, no pickup needed</td><td>Your phone must support eSIM and be carrier-unlocked</td></tr>
<tr><td><strong>Pocket WiFi</strong></td><td>Groups, several devices, older phones</td><td>Pick up and return, keep it charged, everyone stays close</td></tr>
<tr><td><strong>Physical SIM</strong></td><td>Phones without eSIM</td><td>Swapping cards, keeping your home SIM safe</td></tr>
</table></div>

<h2>Before you buy an eSIM</h2>
<ol>
<li>Check that your phone supports eSIM (most iPhones from XS onward and many recent Android phones do).</li>
<li>Check that your phone is unlocked. A phone locked to your home carrier will not accept another eSIM.</li>
<li>Install the eSIM at home over WiFi, then switch it on when you land.</li>
</ol>
<a class="btn" href="{AIRALO_NEW}" {AFF}>Get an Airalo Japan eSIM<small>Code JAPANTIPS15 for new users, JAPANTIPS10 for everyone</small></a>

<h2>The detail most guides skip: a Japanese phone number</h2>
<p>Most travel eSIMs are data-only. That is fine for maps and messaging, but a few bookings in Japan ask for a Japanese phone number. One example: buying Ghibli Museum tickets on a Lawson Loppi machine in a convenience store. If you expect to need one, choose a plan that includes a number, or book those tickets online before your trip.</p>
<p>Planning the Ghibli Museum? Read <a href="{{r}}guides/ghibli-museum-tickets/">how to get Ghibli Museum tickets</a>.</p>
""",
    [
        ("Ghibli Museum: how to get tickets (Japan Travel)", "https://en.japantravel.com/article/ghibli-museum-how-to-get-tickets-2026-guide/71834"),
    ],
)

GHIBLI = article(
    "How to get Ghibli Museum tickets (they sell out fast)",
    "You cannot buy tickets at the door. Tickets go on sale on <strong>Lawson Ticket at 10:00 Japan time on the 10th of each month</strong>, for visits in the following month. Visiting in January? Buy on December 10.",
    """
<h2>When tickets go on sale</h2>
<div class="table-scroll"><table>
<tr><th>If you visit in</th><th>Buy on (10:00 Japan time)</th></tr>
<tr><td>January 2027</td><td>December 10, 2026</td></tr>
<tr><td>February 2027</td><td>January 10, 2027</td></tr>
<tr><td>March 2027</td><td>February 10, 2027</td></tr>
</table></div>
<p>10:00 in Japan is 01:00 GMT the same day, and 20:00 New York time the evening before.</p>

<h2>What to do before sale day</h2>
<ol>
<li>Create a Lawson Ticket account a few days early. Do not leave it for the morning of the sale.</li>
<li>Decide your date and a backup date.</li>
<li>Pick your entry time in advance. You choose a time slot when you buy.</li>
</ol>

<h2>On sale day</h2>
<ol>
<li>Log in about 10 minutes before 10:00 Japan time.</li>
<li>Go straight to the Ghibli Museum page and choose your date and time without hesitating.</li>
<li>Complete payment and keep your confirmation.</li>
</ol>

<h2>If it sells out</h2>
<ul>
<li>Try other dates in the same month, especially weekdays.</li>
<li>Check again later: some tickets become available after the first rush.</li>
<li>Already in Japan? Tickets are also sold on Loppi machines in Lawson stores, which require a Japanese phone number. See <a href="{r}guides/japan-esim-pocket-wifi-sim/">eSIM vs pocket WiFi</a>.</li>
</ul>
""",
    [
        ("Ghibli Museum official ticket information", "https://ghibli-museum.jp/en/tickets"),
        ("Ghibli Museum: how to get tickets (Japan Travel)", "https://en.japantravel.com/article/ghibli-museum-how-to-get-tickets-2026-guide/71834"),
    ],
)

STAY = article(
    "Where to stay in Tokyo on your first trip",
    "First trip and want easy transport? <strong>Shinjuku</strong>. Want a traditional feel and an easy ride from Narita? <strong>Ueno or Asakusa</strong>. Planning day trips by bullet train? <strong>Tokyo Station</strong>. Here for shopping and nightlife? <strong>Shibuya</strong>.",
    f"""
<h2>The four areas compared</h2>
<div class="table-scroll"><table>
<tr><th>Area</th><th>Why stay here</th><th>Best for</th></tr>
<tr><td><strong>Shinjuku</strong></td><td>Huge transport hub, endless food, open late</td><td>First-timers who want everything nearby</td></tr>
<tr><td><strong>Shibuya</strong></td><td>Shopping, nightlife, young energy, city views</td><td>Shoppers and night owls</td></tr>
<tr><td><strong>Ueno / Asakusa</strong></td><td>Temples, old-town streets, direct Skyliner from Narita</td><td>Narita arrivals, traditional atmosphere</td></tr>
<tr><td><strong>Tokyo Station / Ginza</strong></td><td>Bullet trains, polished hotels, central location</td><td>Day trips to Kyoto, Nikko or Mt Fuji areas</td></tr>
</table></div>

<h2>How to choose in 30 seconds</h2>
<ul>
<li>Landing at Narita with big suitcases: Ueno or Asakusa (see <a href="{{r}}guides/narita-airport-to-tokyo/">Narita to Tokyo</a>).</li>
<li>Using a JR Pass for day trips: Tokyo Station.</li>
<li>Want food and transport options at any hour: Shinjuku.</li>
<li>Traveling for shopping and nightlife: Shibuya.</li>
</ul>

<h2>Tips before you book</h2>
<ul>
<li>Stay within a 5 to 10 minute walk of a station. It matters more than the exact area.</li>
<li>Tokyo hotel rooms are small. Check the room size if you travel with large luggage.</li>
<li>Book early for cherry blossom season and New Year, when prices rise.</li>
</ul>
<a class="btn" href="{AGODA_TOKYO}" {AFF}>Compare Tokyo hotels on Agoda</a>
""",
    [],
)

NEWYEAR = article(
    "Visiting Japan over New Year? Read this first",
    "Japan does not fully shut down, but from roughly <strong>December 29 to January 3</strong> many attractions, shops, restaurants, banks and ATMs close on one or more days, especially January 1. Trains and hotels are busiest around Dec 29 to 31 and Jan 2 to 4.",
    f"""
<h2>What usually closes</h2>
<ul>
<li>Many museums and some attractions, on part or all of the holiday</li>
<li>Small independent restaurants and shops</li>
<li>Banks, government offices and some ATMs</li>
</ul>
<p>Closure dates differ by place and by year. Check the 2026/27 opening days for every place that matters to your plan.</p>

<h2>What stays open</h2>
<ul>
<li>Convenience stores</li>
<li>Major shrines and temples, which are very crowded for hatsumode, the first shrine visit of the year</li>
<li>Many large chains and big department stores, often with shorter hours</li>
</ul>

<h2>When travel is busiest</h2>
<p>Japanese residents leave big cities around December 29 to 31 and return around January 2 to 4. Book trains and hotels for those days early.</p>

<h2>A simple plan</h2>
<ol>
<li>Book your hotel now. Prices rise and rooms go fast over New Year.</li>
<li>Keep January 1 light: a shrine visit and a walk instead of museums.</li>
<li>Carry some cash in case ATMs near you are closed.</li>
</ol>
<a class="btn" href="{AGODA_TOKYO}" {AFF}>Check Tokyo hotels for New Year</a>
""",
    [
        ("Japanese New Year travel and closures (japan-guide.com)", "https://www.japan-guide.com/e/e2276.html"),
    ],
)

TAXFREE = article(
    "Japan tax-free shopping changed on November 1, 2026",
    "From November 1, 2026 you pay the <strong>full price including 10% tax</strong> at the store, then get the tax back as a <strong>refund after customs checks your items when you leave Japan</strong>. Keep receipts and items together, and do not use tax-free snacks or cosmetics before you fly.",
    f"""
<h2>What changed</h2>
<div class="table-scroll"><table>
<tr><th></th><th>Until October 31, 2026</th><th>From November 1, 2026</th></tr>
<tr><td><strong>At the store</strong></td><td>Tax removed at the register</td><td>You pay the tax-inclusive price</td></tr>
<tr><td><strong>Getting the 10% back</strong></td><td>Not needed</td><td>Refund after customs confirms your items at departure</td></tr>
<tr><td><strong>Sealed tax-free bags</strong></td><td>Required for consumables</td><td>No longer needed</td></tr>
<tr><td><strong>Minimum spend</strong></td><td colspan="2">¥5,000 before tax, same store, same day</td></tr>
</table></div>

<h2>How to get your refund</h2>
<ol>
<li>Show your passport when you buy, at a shop that offers tax-free sales.</li>
<li>Keep the items and receipts together. Do not open or use consumables such as snacks, drinks or cosmetics.</li>
<li>When you leave Japan, go to customs <strong>before you check in</strong> for your flight and show your passport and the items.</li>
<li>After customs confirms the purchase, the shop sends the refund.</li>
</ol>

<h2>Tips that save you trouble</h2>
<ul>
<li>Using the automated gates when you arrive? Ask an officer for a passport entry stamp right afterwards.</li>
<li>Leave extra time at the airport. Queues are likely while everyone gets used to the new system.</li>
<li>Pack tax-free items where you can reach them, not deep in checked luggage.</li>
<li>Buying something big? Some shops can ship it overseas directly, which still works under the new rules.</li>
</ul>

<div class="cta-box">
  <p class="cta-title">Staying connected while you shop</p>
  <p>Maps, translation and receipts are easier with data from the moment you land.</p>
  <a class="btn" href="{AIRALO_NEW}" {AFF}>Get an Airalo Japan eSIM</a>
  <p class="codes">Code <b>JAPANTIPS15</b> for 15% off (new users) or <b>JAPANTIPS10</b> for 10% off.</p>
</div>
""",
    [
        ("Japan's tax-free shopping rules change from November 2026 (japan-guide.com)", "https://www.japan-guide.com/news/tax-free-shopping.html"),
        ("Changes are coming to Japan's tax-free shopping (JNTO)", "https://www.japan.travel/en/ca/news/changes-are-coming-to-japans-tax-free-shopping/"),
        ("Tax-free shopping reform from November 2026 (GOOD LUCK TRIP)", "https://www.gltjp.com/en/article/item/21542/"),
    ],
)

ARTICLES = {
    "narita-airport-to-tokyo": ("Narita Airport to Tokyo: which train to take", "Skyliner, Access Express or N'EX? How to choose the right train from Narita Airport to Tokyo by where your hotel is.", NARITA),
    "japan-esim-pocket-wifi-sim": ("eSIM vs pocket WiFi vs SIM card for Japan", "How to choose between an eSIM, pocket WiFi and a SIM card for your Japan trip.", ESIM),
    "ghibli-museum-tickets": ("How to get Ghibli Museum tickets", "Ghibli Museum tickets go on sale on the 10th of each month at 10:00 Japan time. How to prepare and what to do if they sell out.", GHIBLI),
    "where-to-stay-in-tokyo": ("Where to stay in Tokyo on your first trip", "Shinjuku, Shibuya, Ueno/Asakusa or Tokyo Station: how to choose where to stay in Tokyo on your first trip.", STAY),
    "japan-tax-free-shopping-2026": ("Japan tax-free shopping changed on November 1, 2026", "From November 1, 2026 tourists in Japan pay full price and claim the 10% tax back at customs when leaving. How the refund works and how not to lose it.", TAXFREE),
    "new-year-in-japan": ("Visiting Japan over New Year", "What closes in Japan from December 29 to January 3, when trains are busiest, and how to plan your New Year trip.", NEWYEAR),
}

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="6" fill="#fbf8f3"/><circle cx="16" cy="16" r="9" fill="#c8102e"/></svg>'


def write(rel_path, html):
    path = os.path.join(OUT, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(SRC, "assets"), os.path.join(OUT, "assets"))
    for extra in ("tools", "posts"):
        if os.path.isdir(os.path.join(SRC, extra)):
            shutil.copytree(os.path.join(SRC, extra), os.path.join(OUT, extra))
    with open(os.path.join(OUT, "assets", "favicon.svg"), "w") as f:
        f.write(FAVICON)

    write("index.html", layout(SITE_NAME, "Practical guides for first-time visitors to Japan: airport transfers, internet, tickets and where to stay.", HOME, 0, ""))
    write("start/index.html", layout("Start here", "Japan trip guides from our TikTok, newest first.", START, 1, "start/"))
    write("about/index.html", layout("About", "About Japan Travel Starter Guide.", ABOUT, 1, "about/"))
    write("affiliate-disclosure/index.html", layout("Affiliate disclosure", "How affiliate links work on this site.", DISCLOSURE_PAGE, 1, "affiliate-disclosure/"))
    write("privacy/index.html", layout("Privacy policy", "Privacy policy for Japan Travel Starter Guide.", PRIVACY, 1, "privacy/"))

    for slug, (title, desc, body) in ARTICLES.items():
        g = next(x for x in GUIDES if x["slug"] == slug)
        i = GUIDES.index(g)
        nxt = GUIDES[i + 1] if i < len(GUIDES) - 1 else None
        if nxt:
            media, focus = GUIDE_IMG[nxt["slug"]]
            next_html = (
                f'<a class="next-guide" href="{{r}}guides/{nxt["slug"]}/">'
                f'<img src="{img(media, 240, 240, focus)}" alt="" width="120" height="120" loading="lazy">'
                f'<span><span class="next-label">Next guide</span><span class="next-title">{nxt["title"]}</span></span></a>'
            )
        else:
            next_html = '<a class="btn outline" href="{r}start/">See all guides</a>'
        html_body = body.replace("{board}", article_hero(g)).replace("{next}", next_html)
        write(f"guides/{slug}/index.html", layout(title, desc, html_body, 2, f"guides/{slug}/"))

    write("404.html", layout("Page not found", "Page not found.", '<section class="article wrap"><h1>This stop does not exist</h1><p><a href="{r}">Go to the home page</a> or <a href="{r}start/">see all guides</a>.</p></section>', 0, "404.html"))
    print("Built", OUT)


if __name__ == "__main__":
    main()
