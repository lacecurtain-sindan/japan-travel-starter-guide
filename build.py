"""Build the Japan Travel Starter Guide static site into ./docs (served by GitHub Pages).

Pages are defined in PAGES below. Run: python3 build.py
Paths are relative so the site works on GitHub Pages (user or project site) and on a custom domain.
"""
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs")

SITE_NAME = "Japan Travel Starter Guide"
UPDATED = "November 2026"

# ---- Affiliate links (from the existing Wix site; keep IDs in one place) ----
AGODA_TOKYO = "https://www.agoda.com/partners/partnersearch.aspx?pcs=1&cid=1967609&hl=en-us&city=5085"
KLOOK_SKYLINER = "https://www.klook.com/activity/1410-skyliner-tokyo/?aid=125057&aff_adid=1313025"
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=Zen+Kaku+Gothic+New:wght@500;700;900&display=swap">
<link rel="stylesheet" href="{r}assets/style.css">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{r}"><span class="brand-ja" lang="ja" aria-hidden="true">日本</span><span class="brand-en">Japan Travel Starter Guide</span></a>
    <nav class="site-nav"><a href="{r}start/">All guides</a></nav>
  </div>
</header>
<main>
{body.replace("{r}", r)}
</main>
<footer class="site-footer">
  <div class="tenji" aria-hidden="true"></div>
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
NEWEST = "new-year-in-japan"


def route_map(r="{r}"):
    """Vertical line diagram: stages are sections of the line, guides are stations."""
    out = ['<ol class="route" aria-label="Guides in trip order">']
    for key, label, ja in STAGES:
        out.append(
            f'<li class="route-stage"><span class="stage-ja" lang="ja">{ja}</span>'
            f'<span class="stage-en">{label}</span></li>'
        )
        for g in [g for g in GUIDES if g["stage"] == key]:
            new = '<span class="new">New</span>' if g["slug"] == NEWEST else ""
            out.append(
                f'<li class="route-stop"><a href="{r}guides/{g["slug"]}/">'
                f'<span class="num" aria-label="Stop {g["code"]}"><b>JT</b>{g["code"]}</span>'
                f'<span class="stop-body"><span class="stop-ja" lang="ja">{g["ja"]}</span>'
                f'<span class="stop-title">{g["title"]}{new}</span>'
                f'<span class="stop-sum">{g["summary"]}</span></span></a></li>'
            )
    out.append("</ol>")
    return "\n".join(out)


def station_board(g, r="{r}"):
    """Station-sign header for a guide: prev/next stops are real links."""
    i = GUIDES.index(g)
    prev_g = GUIDES[i - 1] if i > 0 else None
    next_g = GUIDES[i + 1] if i < len(GUIDES) - 1 else None
    prev_html = (
        f'<a class="adj prev" href="{r}guides/{prev_g["slug"]}/"><span lang="ja">{prev_g["ja"]}</span>{prev_g["short"]}</a>'
        if prev_g else f'<a class="adj prev" href="{r}"><span lang="ja">日本</span>All stops</a>'
    )
    next_html = (
        f'<a class="adj next" href="{r}guides/{next_g["slug"]}/"><span lang="ja">{next_g["ja"]}</span>{next_g["short"]}</a>'
        if next_g else f'<a class="adj next" href="{r}start/"><span lang="ja">終点</span>All guides</a>'
    )
    return f"""
<header class="board">
  <span class="board-num"><b>JT</b>{g["code"]}</span>
  <p class="board-kana" lang="ja">{g["kana"]}</p>
  <p class="board-ja" lang="ja">{g["ja"]}</p>
  <h1 class="board-en">{g["title"]}</h1>
  <nav class="board-band" aria-label="Previous and next guide">{prev_html}{next_html}</nav>
</header>"""


HOME = f"""
<section class="hero wrap">
  <div class="board board-hero">
    <p class="board-kana" lang="ja">はじめての にほん</p>
    <p class="board-ja" lang="ja">日本</p>
    <h1 class="board-en">Your first trip to Japan</h1>
    <div class="board-band"><span class="adj prev"><span lang="ja">出発前</span>Before you fly</span><span class="adj next"><span lang="ja">滞在中</span>During your trip</span></div>
  </div>
  <p class="lead">Practical guides to the parts of a first Japan trip that catch people out, in the order you will need them.</p>
</section>
<section class="wrap">
{route_map()}
<div class="cta-box">
  <p class="cta-title">Need a hotel in Tokyo?</p>
  <p>Compare prices for your dates on Agoda.</p>
  <a class="btn" href="{AGODA_TOKYO}" {AFF}>Search Tokyo hotels</a>
</div>
</section>
"""

START = f"""
<section class="wrap start">
  <h1 class="start-title">Guides from our TikTok</h1>
  <p class="lead">Find the guide from the video you just watched. They are listed in trip order.</p>
{route_map()}
  <h2>Booking links from the guides</h2>
  <a class="btn" href="{KLOOK_SKYLINER}" {AFF}>Book a Skyliner ticket (Narita to Ueno)<small>Online price for overseas visitors</small></a>
  <a class="btn ghost" href="{AIRALO_NEW}" {AFF}>Get an Airalo eSIM for Japan<small>Code JAPANTIPS15 for new users, JAPANTIPS10 for everyone</small></a>
  <a class="btn ghost" href="{AGODA_TOKYO}" {AFF}>Search Tokyo hotels on Agoda</a>
  <p class="note">Some links are affiliate links. <a href="{{r}}affiliate-disclosure/">How this works</a></p>
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
  <div class="wrap-wide">{{board}}</div>
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

ARTICLES = {
    "narita-airport-to-tokyo": ("Narita Airport to Tokyo: which train to take", "Skyliner, Access Express or N'EX? How to choose the right train from Narita Airport to Tokyo by where your hotel is.", NARITA),
    "japan-esim-pocket-wifi-sim": ("eSIM vs pocket WiFi vs SIM card for Japan", "How to choose between an eSIM, pocket WiFi and a SIM card for your Japan trip.", ESIM),
    "ghibli-museum-tickets": ("How to get Ghibli Museum tickets", "Ghibli Museum tickets go on sale on the 10th of each month at 10:00 Japan time. How to prepare and what to do if they sell out.", GHIBLI),
    "where-to-stay-in-tokyo": ("Where to stay in Tokyo on your first trip", "Shinjuku, Shibuya, Ueno/Asakusa or Tokyo Station: how to choose where to stay in Tokyo on your first trip.", STAY),
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
        next_html = (
            f'<a class="next-stop" href="{{r}}guides/{nxt["slug"]}/"><span class="next-label">Next stop</span>'
            f'<span class="next-ja" lang="ja">{nxt["ja"]}</span><span class="next-title">{nxt["title"]}</span></a>'
            if nxt else
            '<a class="next-stop" href="{r}start/"><span class="next-label">End of the line</span>'
            '<span class="next-ja" lang="ja">終点</span><span class="next-title">See all guides</span></a>'
        )
        html_body = body.replace("{board}", station_board(g)).replace("{next}", next_html)
        write(f"guides/{slug}/index.html", layout(title, desc, html_body, 2, f"guides/{slug}/"))

    write("404.html", layout("Page not found", "Page not found.", '<section class="article wrap"><h1>This stop does not exist</h1><p><a href="{r}">Go to the home page</a> or <a href="{r}start/">see all guides</a>.</p></section>', 0, "404.html"))
    print("Built", OUT)


if __name__ == "__main__":
    main()
