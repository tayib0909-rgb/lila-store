#!/usr/bin/env python3
"""Builds the interior HTML for DOGS ARE WEIRD. WE LOVE THEM.

Usage:  python3 build/build.py        (from books/dogs-are-weird)
Output: build/interior.html  (rendered to PDF by build/render.js)

Illustrations: drop finished art into images/ named by ID (e.g. images/IMG-001.jpg,
images/CAT-drama.png, images/XMAS-X01.webp). Any page whose image exists will use it;
otherwise a clearly labeled placeholder frame is printed.
"""
import html, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from content import breeds_1, breeds_2, breeds_3, breeds_4, extras as X  # noqa: E402

IMG_DIR = ROOT / "images"
CAT_DATA = {c[0]: c for c in X.CATEGORIES}
GROUPS = [
    ("drama", breeds_1.DRAMA), ("tiny", breeds_1.TINY), ("fluffy", breeds_2.FLUFFY), ("couch", breeds_2.COUCH),
    ("athletic", breeds_3.ATHLETIC), ("giants", breeds_3.GIANTS), ("weird", breeds_4.WEIRD), ("owners", breeds_4.OWNERS),
]
n = 0
for key, lst in GROUPS:
    for b in lst:
        n += 1
        b.category = key
        b.img_id = f"IMG-{n:03d}"
ALL = [b for _, l in GROUPS for b in l]
BY_NAME = {b.name: b for b in ALL}

e = html.escape
PAW = ('<svg viewBox="0 0 24 24"><path fill="{f}" d="M12 13.5c-3 0-6 2.6-6 5.2 0 1.6 1.3 2.3 2.8 2.3 1.2 0 2-.6 3.2-.6s2 .6 3.2.6c1.5 0 2.8-.7 2.8-2.3 0-2.6-3-5.2-6-5.2zM5.2 12.6c1.3-.3 1.9-1.9 1.5-3.4S5 6.7 3.7 7s-1.9 1.9-1.5 3.4 1.7 2.5 3 2.2zm4-3.4c1.5 0 2.5-1.6 2.5-3.5S10.7 2 9.2 2 6.8 3.6 6.8 5.6s1 3.6 2.4 3.6zm5.6 0c1.4 0 2.4-1.6 2.4-3.6S16.2 2 14.8 2s-2.5 1.7-2.5 3.6 1 3.6 2.5 3.6zm5.5-2.2c-1.3-.3-2.7.8-3 2.3s.2 3 1.5 3.3 2.7-.8 3-2.3-.2-3-1.5-3.3z"/></svg>')
PAW_BIG = PAW.format(f="currentColor").replace('fill="currentColor"', 'fill="#000"')


def find_img(img_id):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        p = IMG_DIR / f"{img_id}{ext}"
        if p.exists():
            return f"../images/{img_id}{ext}"
    return None


def portrait(img_id, direction, tag="Portrait"):
    src = find_img(img_id)
    if src:
        return f'<div class="portrait has-img" style="background-image:url(\'{src}\')"></div>'
    return (f'<div class="portrait"><div class="ph">{PAW_BIG}<div class="tag">{e(tag)} · Illustration pending</div>'
            f'<div class="id">{img_id}</div><div class="dir">{e(direction)}</div></div></div>')


def paws(v):
    return '<div class="paws">' + "".join(PAW.format(f="var(--c)" if i < v else "#E4DACB") for i in range(5)) + "</div>"


class Book:
    def __init__(self):
        self.pages = []  # (html_inner, classes, style, folio_label)

    def add(self, inner, cls="", style="", folio=True, cat=None):
        if cat:
            c = CAT_DATA[cat]
            style = f"--c:{c[4]};--c2:{c[5]};" + style
        self.pages.append((inner, cls, style, folio))
        return len(self.pages)  # 1-based page number

    def render(self):
        out = []
        for i, (inner, cls, style, folio) in enumerate(self.pages, 1):
            side = "recto" if i % 2 == 1 else "verso"
            fol = f'<div class="folio">{i}</div>' if folio else ""
            out.append(f'<section class="page {side} {cls}" style="{style}" data-p="{i}">{inner}{fol}</section>')
        return "\n".join(out)


book = Book()
toc = []        # (group, title, page)
index_pages = {}

# ---------------- Front matter ----------------
book.add('<div class="safe center title-page">'
         '<div class="kicker" style="--c:var(--red)">Christmas Gift Edition 2027</div><div class="rule"></div>'
         '<h1 class="display">Dogs Are Weird.<span>We Love Them.</span></h1>'
         '<p class="sub">100+ Hilarious Dog Breeds, Crazy Personalities, Adorable Portraits &amp; Facts That Will Make You Laugh</p>'
         '<div class="rule"></div><div class="ed">A Gift Book for Dog Lovers</div></div>', folio=False)

book.add('<div class="safe copyright" style="display:flex;flex-direction:column;justify-content:flex-end">'
         '<p><b>DOGS ARE WEIRD. WE LOVE THEM.</b><br>100+ Hilarious Dog Breeds, Crazy Personalities, Adorable Portraits &amp; Facts That Will Make You Laugh<br>Christmas Gift Edition 2027</p>'
         '<p>Copyright © 2027 Tayeb Msalem. All rights reserved.</p>'
         '<p>No part of this publication may be reproduced, distributed or transmitted in any form or by any means without the prior written permission of the publisher, except for brief quotations in reviews.</p>'
         f'<p>{e(X.DISCLAIMER)}</p>'
         '<p>All illustrations are original works created for this edition. Breed names are used descriptively; this book is not affiliated with or endorsed by any kennel club.</p>'
         '<p>ISBN: [KDP-ASSIGNED OR OWN ISBN]<br>Independently published · Printed in the United States of America</p>'
         '<p>First Edition, 2027</p></div>', folio=False)

book.add('<div class="snow"></div><div class="safe center">'
         '<div class="ornament"></div><div class="kicker gold" style="color:#E8C766;font-size:10pt">Christmas 2027</div>'
         '<h2 class="display" style="margin:.2in 0">Merry Christmas<br><span class="gold">from the Weirdest,<br>Sweetest Dogs on Earth</span></h2>'
         '<p style="max-width:5.4in">This season, may your stockings be full, your cookies be safe from the Beagle and your home be filled with wagging tails, muddy paws and the kind of love only a dog can give.</p>'
         '<div class="rule" style="background:#E8C766"></div><p style="font-size:11pt;opacity:.85">Pour the cocoa. Grab a blanket. Let the weirdness begin.</p></div>',
         cls="xmas", folio=False)

book.add('<div class="safe center"><div class="kicker" style="--c:var(--red)">Dedication</div><div class="rule"></div>'
         + "".join(f'<p style="font:italic 400 17pt/1.55 Fraunces;max-width:5.4in;margin-bottom:.2in">{e(p)}</p>' for p in X.DEDICATION.split("\n\n"))
         + '<div class="rule"></div></div>', folio=False)

book.add('<div class="safe center"><div style="width:100%;max-width:6.2in"><div class="giftbox">'
         '<div class="kicker" style="--c:var(--red);text-align:center;font-size:10pt">A Special Gift</div>'
         '<h2 class="display" style="text-align:center;font-size:30pt;margin:.12in 0 .1in">For Someone Who Loves Dogs<br>(and Is Just as Weird)</h2>'
         '<label>To</label><div class="line"></div><label>From</label><div class="line"></div>'
         '<label>A Message for You</label><div class="line"></div><div class="line"></div><div class="line"></div><div class="line"></div>'
         '<label>Christmas 2027</label><div class="line" style="width:50%"></div>'
         '</div><p style="text-align:center;margin-top:.2in;font:700 18pt Caveat;color:var(--red)">Woof! (That means Merry Christmas.)</p></div></div>', folio=False)

TOC_PAGE = book.add("__TOC__", folio=False)
welcome = book.add('<div class="safe chapter"><div class="ch-head"><div class="kicker" style="--c:var(--red)">Welcome</div>'
                   '<h2 class="display">Hello, Fellow <em style="color:var(--red)">Dog Person.</em></h2></div><div class="ch-body">'
                   + "".join(f'<p style="font:400 12pt/1.62 InterB;margin-bottom:.16in">{e(p)}</p>' for p in X.WELCOME)
                   + '<p style="font:700 22pt Caveat;color:var(--red);margin-top:.2in">Woof, and happy reading!</p></div></div>', style="--c:var(--red)")
toc.append(("Start Here", "Welcome", welcome))
how = book.add('<div class="safe chapter"><div class="ch-head"><div class="kicker" style="--c:var(--red)">How to Read This Book</div>'
               '<h2 class="display">Every Profile, <em style="color:var(--red)">Decoded.</em></h2>'
               '<p>Each breed gets its own page packed with real facts and ridiculous truths. Here\'s what you\'ll find.</p></div><div class="ch-body"><div class="grid2">'
               + "".join(f'<div class="tile" style="--c:var(--red)"><h4>{e(a)}</h4><p style="color:var(--ink)">{e(b)}</p></div>' for a, b in X.HOW_TO_READ)
               + '<div class="tile" style="--c:var(--red)"><h4>Paw Meters</h4><div style="display:flex;gap:.15in;align-items:center;margin-top:.05in">'
               + paws(1).replace("var(--c)", "var(--red)") + '<span style="font-size:8.5pt">Low</span>' + paws(5).replace("var(--c)", "var(--red)") + '<span style="font-size:8.5pt">Off the charts</span></div></div>'
               + '</div><p style="margin-top:.25in;font:italic 400 10.5pt/1.5 Fraunces;color:var(--ink-soft)">The eight categories are for laughs, not science. Plenty of Couch Potatoes love a hike, and every Drama Queen has a quiet side. Each dog is an individual, just like their humans.</p></div></div>',
               style="--c:var(--red)")
toc.append(("Start Here", "How to Read This Book", how))


# ---------------- Breed & chapter helpers ----------------
def opener(key):
    c = CAT_DATA[key]
    lst = dict(GROUPS)[key]
    names = "".join(f"<div>{e(b.name)}</div>" for b in lst)
    p = book.add(f'<div class="bgpaws"></div><div class="safe"><div class="kicker">Chapter · {len(lst)} Breeds</div>'
                 f'<h2 class="display">{e(c[1])}</h2><div class="tagline">{e(c[2])}</div>'
                 f'<div class="art">{portrait("CAT-" + key, "Group portrait of breeds from this chapter posing together like a movie poster, editorial studio set in the chapter color", "Chapter art")}</div>'
                 f'<p class="intro">{e(c[3])}</p><div class="list">{names}</div></div>', cls="opener", cat=key)
    toc.append((c[1], "Meet " + c[1].replace("The ", "the ", 1), p))


def breed_page(b, num):
    c = CAT_DATA[b.category]
    inner = f'''<div class="safe">
  <div class="b-head"><div><div class="kicker">{e(c[1])}</div><h1>{e(b.name)}</h1>
    <div class="meta">Origin: <b>{e(b.origin)}</b></div></div><div class="num">No.{num:03d}</div></div>
  <div class="hero">{portrait(b.img_id, b.portrait)}
    <div class="card stats"><h4>Quick Stats</h4>
      <div class="stat"><span>Height</span><strong>{e(b.height)}</strong></div>
      <div class="stat"><span>Weight</span><strong>{e(b.weight)}</strong></div>
      <div class="stat"><span>Lifespan</span><strong>{e(b.lifespan)}</strong></div>
      <div class="meter"><span>Grooming</span>{paws(b.grooming)}</div>
      <div class="meter"><span>Exercise</span>{paws(b.exercise)}</div>
      <div class="meter"><span>Trainability</span>{paws(b.trainability)}</div>
      <div class="perfect"><b>Perfect For</b>{e(b.perfect)}</div>
    </div></div>
  <div class="fitbox">
    <div class="truth"><div class="lbl">The Hilarious Truth</div><p>{e(b.funny)}</p></div>
    <div class="cols">
      <div style="display:flex;flex-direction:column;gap:.1in"><div class="sec"><h5>Origin &amp; History</h5><p>{e(b.history)}</p></div>
        <div class="sec"><h5>Personality &amp; Temperament</h5><p>{e(b.temperament)}</p></div></div>
      <div class="sec fact"><h5>★ Surprising Fact</h5><p>{e(b.fact)}</p></div>
    </div>
    <div class="trio">
      <div class="card"><h6>If This Dog Were a Person…</h6><p>{e(b.person)}</p></div>
      <div class="card"><h6>Secret Superpower</h6><p>{e(b.superpower)}</p></div>
      <div class="card bubble"><h6>If It Could Talk</h6><p>“{e(b.says)}”</p></div>
    </div>
  </div>
</div>'''
    p = book.add(inner, cls="breed", cat=b.category)
    index_pages[b.name] = p


def chapter(key, kicker, title_html, intro, body, toc_title, style=""):
    p = book.add(f'<div class="safe chapter"><div class="ch-head"><div class="kicker">{e(kicker)}</div>'
                 f'<h2 class="display">{title_html}</h2>{"<p>" + e(intro) + "</p>" if intro else ""}</div>'
                 f'<div class="ch-body">{body}</div></div>', cls="chapter-page", cat=key, style=style)
    toc.append(("Just for Laughs", toc_title, p))
    return p


def rank_list(items, numbered=True):
    return "".join(f'<div class="rank"><div class="n">{i if numbered else "★"}</div><div><h4>{e(a)}</h4><p>{e(b)}</p></div></div>'
                   for i, (a, b) in enumerate(items, 1))


# ---------------- Humor chapter bodies ----------------
def ch_drama():
    chapter("drama", "Countdown", "The World's Biggest <em>Drama Queens</em>",
            "Ranked by our panel of experts (three people and a very judgmental cat).",
            rank_list(X.DRAMA_TOP10), "The World's Biggest Drama Queens")


def ch_texts():
    def ph(name, msgs):
        return (f'<div class="phone"><div class="who"><b>{e(name)}</b>iMessage · now</div>'
                + "".join(f'<div class="msg {w}">{e(t)}</div>' for w, t in msgs) + "</div>")
    a, b = X.TEXTS[:3], X.TEXTS[3:]
    p1 = chapter("drama", "Unread Messages", "If Dogs Could Send <em>Text Messages</em>",
                 "Be grateful they don't have thumbs. Here's what your phone would look like if they did.",
                 '<div class="grid2">' + "".join(ph(n, m) for n, m in a[:2]) + '</div><div style="height:.15in"></div><div class="grid2">' + ph(*a[2]) + ph(*b[0]) + "</div>",
                 "If Dogs Could Send Text Messages")
    book.add('<div class="safe chapter"><div class="ch-head"><div class="kicker">Unread Messages, Continued</div>'
             '<h2 class="display" style="font-size:28pt">More Texts You Never <em>Wanted</em></h2></div><div class="ch-body"><div class="grid2">'
             + "".join(ph(n, m) for n, m in b[1:]) +
             '</div><div class="tile" style="margin-top:.25in"><h4>Bonus: Auto-Reply Messages</h4>'
             '<p style="color:var(--ink)"><b>Bulldog:</b> "I am currently asleep. I will respond when I feel like it (never)."<br>'
             '<b>Border Collie:</b> "Received. Processed. Herded. Anything else?"<br>'
             '<b>Cat (wrong number):</b> "No."</p></div></div></div>', cls="chapter-page", cat="drama")
    return p1


def ch_boss():
    tiles = "".join(f'<div class="tile {"ceo" if i == 0 else ""}"><h4>{e(r)}</h4><div class="big">{e(d)}</div><p>{e(t)}</p></div>'
                    for i, (r, d, t) in enumerate(X.SECRET_BOSS))
    chapter("tiny", "Org Chart", "Dogs Who Are Secretly <em>the Boss</em>",
            "You think you run the household. Here's the real chain of command.",
            f'<div class="org">{tiles}</div><p style="margin-top:.2in;font:italic 400 1em Fraunces;color:var(--ink-soft);text-align:center">Your position: Snack Dispenser, Junior Level. Performance review: pending.</p>',
            "Dogs Who Are Secretly the Boss")


def ch_mortgage():
    chapter("tiny", "Household Finances", "Dogs Who Think They <em>Pay the Mortgage</em>",
            "They've never seen a bill. They've never held a pen. Yet they walk around the house like they signed the deed.",
            rank_list(X.MORTGAGE, numbered=False) + '<div class="tile" style="margin-top:.18in"><h4>Official Statement From the Dogs</h4>'
            '<p style="color:var(--ink);font:italic 500 1.1em/1.4 Fraunces">"We contribute emotional support, home security and floor-cleaning services. We believe this is more than fair."</p></div>',
            "Dogs Who Think They Pay the Mortgage")


def ch_owners():
    chapter("fluffy", "Relatable Content", "Things Only <em>Dog Owners</em> Understand",
            "Check off every one that's true. If you get all of them, congratulations: you're officially one of us.",
            '<ul class="checklist" style="columns:2;column-gap:.3in">' + "".join(f"<li>{e(t)}</li>" for t in X.OWNERS_UNDERSTAND) + "</ul>",
            "Things Only Dog Owners Understand")


def ch_adorable():
    chapter("fluffy", "Pure Joy", "The Most Ridiculously <em>Adorable</em> Dog Personalities",
            "Every dog has a personality type. Which one lives at your house?",
            '<div class="grid2">' + "".join(f'<div class="tile"><h4>{e(a)}</h4><p style="color:var(--ink)">{e(b)}</p></div>' for a, b in X.ADORABLE) + "</div>",
            "The Most Ridiculously Adorable Dog Personalities")


def ch_couch():
    top = X.COUCH_CHAMPIONSHIP
    pod = (f'<div class="podium">'
           f'<div class="pod"><div class="nm">{e(top[1][1])}</div><div class="sc">{top[1][2]} pts</div><div class="blk" style="background:#9AA4B1;height:1.1in">2</div></div>'
           f'<div class="pod"><div class="nm">{e(top[0][1])}</div><div class="sc">{top[0][2]} pts</div><div class="blk" style="background:var(--gold);height:1.5in">1</div></div>'
           f'<div class="pod"><div class="nm">{e(top[2][1])}</div><div class="sc">{top[2][2]} pts</div><div class="blk" style="background:#B07A4A;height:.8in">3</div></div></div>')
    chapter("couch", "Official Results", "The Ultimate <em>Couch Potato</em> Championship",
            "Judged on stillness, snoring volume, cushion coverage and refusal to move for snacks (nobody scored in that last category).",
            pod + rank_list([(f"{m} · {b} ({s} pts)", t) for m, b, s, t in top], numbered=True),
            "The Ultimate Couch Potato Championship")


def ch_habits():
    chapter("couch", "A Day in the Life", "Dogs and Their <em>Ridiculous</em> Daily Habits",
            "A typical day, minute by ridiculous minute.",
            '<ul class="schedule">' + "".join(f'<li><span class="t">{e(t)}</span><span class="d">{e(d)}</span></li>' for t, d in X.DAILY_HABITS) + "</ul>",
            "Dogs and Their Ridiculous Daily Habits")
    book.add('<div class="safe chapter"><div class="ch-head"><div class="kicker">The Science (Sort Of)</div>'
             '<h2 class="display" style="font-size:30pt">Why Do Dogs <em>Do That?</em></h2>'
             '<p>Some of the weirdest habits actually have real explanations.</p></div><div class="ch-body"><div class="grid2">'
             + "".join(f'<div class="tile"><h4>{e(a)}</h4><p style="color:var(--ink)">{e(b)}</p></div>' for a, b in X.HABITS_EXPLAINED) +
             '</div><div style="margin-top:.3in;height:3.8in;border-radius:18px;overflow:hidden;position:relative">'
             + portrait("ART-habits", "A Labrador spinning in circles on a dog bed, motion blur, cozy living room, photographic humor", "Feature art") +
             '</div></div></div>', cls="chapter-page", cat="couch")


def ch_jobs():
    chapter("athletic", "Career Day", "If Dog Breeds <em>Had Jobs</em>",
            "Résumés reviewed. References checked. Treats negotiated.",
            '<div class="grid2">' + "".join(f'<div class="tile" style="padding:.08in .14in"><h4>{e(a)}</h4><div class="big" style="font-size:1.1em">{e(b)}</div></div>' for a, b in X.JOBS) + "</div>",
            "If Dog Breeds Had Jobs")


def ch_zombie():
    z = X.ZOMBIES

    def tier(cls, title, rows):
        return f'<div class="tier {cls}"><h3>{title}</h3>' + "".join(f'<div class="row"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in rows) + "</div>"
    chapter("athletic", "Survival Guide", "Which Dog Would Survive a <em>Zombie Apocalypse?</em>",
            "Our experts ran the simulations. The results are… concerning.",
            tier("s", "Will Definitely Survive", z["survive"]) + tier("m", "Fifty-Fifty", z["maybe"]) + tier("f", "First to Go (Bless Them)", z["first"]),
            "Which Dog Would Survive a Zombie Apocalypse?")


def ch_dating():
    def prof(d):
        name, br, age, look, likes, bio = d
        return (f'<div class="profile"><div class="top"><b>{e(name)}, {age}</b><span>{e(br)} · 0.4 miles away</span></div>'
                f'<div class="bd"><p><em>About me</em>{e(bio)}</p><p><em>Likes</em>{e(likes)}</p><p><em>Looking for</em>{e(look.replace("Looking for: ", ""))}</p></div>'
                f'<div class="btns"><span>✕</span><span>♥</span></div></div>')
    chapter("giants", "Swipe Right", "If Your Dog Had a <em>Dating Profile</em>",
            "Love is in the air. So is fur.",
            '<div class="grid3">' + "".join(prof(d) for d in X.DATING[:3]) + "</div>"
            + '<div style="margin-top:.25in;height:3.6in;border-radius:18px;overflow:hidden;position:relative">'
            + portrait("ART-dating", "A Great Dane and a tiny Chihuahua on a candlelit dinner date at a bistro table, sharing one spaghetti noodle, romantic warm bokeh", "Feature art")
            + "</div>", "If Your Dog Had a Dating Profile")
    book.add('<div class="safe chapter"><div class="ch-head"><div class="kicker">More Matches Near You</div>'
             '<h2 class="display" style="font-size:28pt">It\'s a <em>Match!</em></h2></div><div class="ch-body"><div class="grid3">'
             + "".join(prof(d) for d in X.DATING[3:]) +
             '</div><div class="tile" style="margin-top:.25in"><h4>First-Date Tips From the Dogs</h4>'
             '<p style="color:var(--ink)">1. Sniff first, ask questions later. 2. Always share your fries. 3. If it\'s going badly, roll over and show your belly. Works every time.</p></div></div></div>',
             cls="chapter-page", cat="giants")


def ch_manip():
    chapter("weird", "Warning Signs", "10 Signs Your Dog Is <em>Manipulating You</em>",
            "You're not being paranoid. You're being played. Lovingly.",
            rank_list(X.MANIPULATION) + '<p style="margin-top:.14in;font:italic 400 1em Fraunces;color:var(--ink-soft)">Score 8 or more? Your dog isn\'t manipulating you. Your dog is running a full-scale operation.</p>',
            "10 Signs Your Dog Is Manipulating You")


def ch_awards():
    chapter("weird", "Red Carpet", "The Great Dog Breed <em>Awards</em>",
            "The envelopes, please. (Don't let the Lab eat them.)",
            '<div class="grid2">' + "".join(f'<div class="award"><div class="medal">★</div><div><h4>{e(a)}</h4><div class="who">{e(b)}</div><p>{e(c)}</p></div></div>' for a, b, c in X.AWARDS) + "</div>",
            "The Great Dog Breed Awards")


def quiz_pages(key, q, toc_title, xmas=False):
    qs = "".join(f'<div class="quiz-q"><h4><span>{i}.</span>{e(t)}</h4><ol>' + "".join(f"<li><b>{'ABCD'[j]}</b>{e(o)}</li>" for j, o in enumerate(opts)) + "</ol></div>"
                 for i, (t, opts) in enumerate(q["questions"], 1))
    style = "--c:#B3261E;--c2:#F9DEDC" if xmas else ""
    p = book.add(f'<div class="safe chapter"><div class="ch-head"><div class="kicker">{"Christmas Quiz" if xmas else "Quiz Time"}</div>'
                 f'<h2 class="display">{e(q["title"])}</h2><p>{e(q["intro"])}</p></div><div class="ch-body">{qs}'
                 f'<p style="text-align:center;font:700 18pt Caveat;color:var(--c);margin-top:.1in">Count your letters, then turn the page!</p></div></div>',
                 cls="chapter-page", cat=None if xmas else key, style=style)
    toc.append(("Christmas Gift Edition" if xmas else "Just for Laughs", q["title"], p))
    res = "".join(f'<div class="result"><div class="l">{e(a)}</div><div><h4>{e(b)}</h4><p>{e(c)}</p></div></div>' for a, b, c in q["results"])
    book.add(f'<div class="safe chapter"><div class="ch-head"><div class="kicker">Your Results</div><h2 class="display">And You Are…</h2></div>'
             f'<div class="ch-body">{res}<p style="text-align:center;font:italic 400 1em Fraunces;color:var(--ink-soft);margin-top:.15in">A perfect tie? Congratulations, you\'re a mixed breed: the best of everything.</p></div></div>',
             cls="chapter-page", cat=None if xmas else key, style=style)


# ---------------- Assemble body ----------------
after = {
    "drama": [ch_drama, ch_texts], "tiny": [ch_boss, ch_mortgage], "fluffy": [ch_owners, ch_adorable],
    "couch": [ch_couch, ch_habits], "athletic": [ch_jobs, ch_zombie], "giants": [ch_dating],
    "weird": [ch_manip, ch_awards], "owners": [lambda: quiz_pages("owners", X.QUIZ, "The Ultimate Dog Personality Quiz")],
}
num = 0
for key, lst in GROUPS:
    opener(key)
    for b in lst:
        num += 1
        breed_page(b, num)
    for fn in after[key]:
        fn()

# ---------------- Christmas section ----------------
XS = "--c:#B3261E;--c2:#F9DEDC"
p = book.add('<div class="snow"></div><div class="safe center"><div class="ornament"></div>'
             '<div class="kicker" style="color:#E8C766;font-size:10pt">The Christmas Chapter</div>'
             '<h2 class="display" style="margin:.2in 0">Dogs at <span class="gold">Christmas</span></h2>'
             '<p style="max-width:5.4in">Twinkling lights. Shiny ornaments. Cookies left out for Santa. To a dog, the holidays look like the world\'s greatest, most tempting obstacle course.</p>'
             '<div style="width:100%;height:4.3in;margin-top:.35in;border-radius:22px;overflow:hidden;position:relative" class="art">'
             + portrait("XMAS-hero", "A cozy living room on Christmas Eve: a Golden Retriever, Corgi, Frenchie and Husky in Santa hats around a glowing tree, falling snow outside the window, warm golden light", "Christmas art")
             + '</div></div>', cls="xmas opener", folio=True)
toc.append(("Christmas Gift Edition", "Dogs at Christmas", p))

for half in (X.CHRISTMAS_PORTRAITS[:4], X.CHRISTMAS_PORTRAITS[4:]):
    cells = "".join(f'<div class="gal">{portrait("XMAS-" + i, d, "Christmas portrait")}<div class="cap"><b>{e(n)}</b><span>{e(c)}</span></div></div>' for i, n, d, c in half)
    p = book.add('<div class="snow"></div><div class="safe chapter"><div class="ch-head"><div class="kicker" style="color:#E8C766">Holiday Portrait Gallery</div>'
                 '<h2 class="display" style="color:#FFF7E6;font-size:30pt">Funny Christmas <span class="gold">Dog Portraits</span></h2></div>'
                 f'<div class="gallery">{cells}</div></div>', cls="xmas", style=XS)
    if half is X.CHRISTMAS_PORTRAITS[:4] or True:
        if not any(t[1] == "Funny Christmas Dog Portraits" for t in toc):
            toc.append(("Christmas Gift Edition", "Funny Christmas Dog Portraits", p))

p = book.add('<div class="safe chapter"><div class="ch-head"><div class="kicker">Holiday Hazard Report</div>'
             '<h2 class="display">Dogs at Christmas: Who Would <em>Destroy the Tree First?</em></h2>'
             '<p>Official odds of total tree destruction, calculated by our elves.</p></div><div class="ch-body">'
             + "".join(f'<div class="rank"><div class="n">{r}</div><div><h4>{e(b)} <span style="float:right;color:var(--c);font-family:Lilita;font-weight:400;font-size:1.3em">{o}</span></h4><p>{e(t)}</p></div></div>' for r, b, o, t in X.TREE_DESTROYERS)
             + '<div class="tile" style="margin-top:.15in;background:#FFF6E0"><h4 style="color:#8A6A0A">Safety Note From the Elves</h4><p style="color:var(--ink)">Keep chocolate, xylitol, grapes, raisins, tinsel, ribbon, and electrical cords out of paws\' reach. Secure the tree to the wall, and choose shatterproof ornaments for the low branches.</p></div></div></div>',
             cls="chapter-page", style=XS)
toc.append(("Christmas Gift Edition", "Who Would Destroy the Tree First?", p))

quiz_pages(None, X.CHRISTMAS_QUIZ, "Which Christmas Dog Are You?", xmas=True)

p = book.add('<div class="safe chapter"><div class="ch-head"><div class="kicker">Festive Honors</div>'
             '<h2 class="display">The Festive <em>Dog Awards</em></h2><p>Celebrating outstanding achievement in holiday mischief.</p></div><div class="ch-body"><div class="grid2">'
             + "".join(f'<div class="award"><div class="medal" style="background:radial-gradient(circle at 35% 30%,#FF8A80,#B3261E 60%,#6E0F0A)">✦</div><div><h4>{e(a)}</h4><div class="who">{e(b)}</div></div></div>' for a, b in X.FESTIVE_AWARDS)
             + '</div><div style="margin-top:.3in;height:3.9in;border-radius:18px;overflow:hidden;position:relative">'
             + portrait("XMAS-awards", "A Corgi in a reindeer costume accepting a tiny golden trophy on a stage with red curtains and twinkling lights", "Christmas art")
             + '</div></div></div>', cls="chapter-page", style=XS)
toc.append(("Christmas Gift Edition", "The Festive Dog Awards", p))

p = book.add('<div class="snow"></div><div class="safe center"><div class="kicker" style="color:#E8C766;font-size:10pt">Words to Warm the Heart</div>'
             '<h2 class="display" style="margin:.15in 0 .3in;font-size:36pt">Heartwarming <span class="gold">Dog Quotes</span></h2>'
             + "".join(f'<div class="quote">“{e(q)}”</div>' for q in X.QUOTES) + "</div>", cls="xmas")
toc.append(("Christmas Gift Edition", "Heartwarming Dog Quotes", p))

p = book.add('<div class="safe chapter keepsake"><div class="ch-head"><div class="kicker">Keepsake Page</div>'
             '<h2 class="display">My Own <em>Weird</em> Dog</h2><p>Every dog deserves a page in this book. Here\'s yours.</p></div><div class="ch-body">'
             '<div class="photo">Paste or draw your dog here!</div>'
             + "".join(f'<div class="fl"><span>{e(l)}</span><div></div></div>' for l in ["Name", "Breed (or Beautiful Mix)", "Category", "Weirdest Habit", "Secret Superpower", "If My Dog Could Talk, It Would Say…", "Christmas Wish"])
             + "</div></div>", cls="chapter-page", style=XS)
toc.append(("Christmas Gift Edition", "My Own Weird Dog (Keepsake Page)", p))

idx_items = sorted(index_pages.items())
half = (len(idx_items) + 1) // 2


def idx_html(items):
    out, last = [], ""
    for name, pg in items:
        if name[0] != last:
            last = name[0]
            out.append(f'<div class="L">{last}</div>')
        out.append(f'<div><span>{e(name)}</span><span class="dots"></span><span>{pg}</span></div>')
    return "".join(out)


p = book.add(f'<div class="safe chapter"><div class="ch-head"><div class="kicker">A to Z</div><h2 class="display">Breed Index</h2></div>'
             f'<div class="ch-body"><div class="index">{idx_html(idx_items[:half])}</div></div></div>', cls="chapter-page", style=XS)
toc.append(("The End", "Breed Index A–Z", p))
book.add(f'<div class="safe chapter"><div class="ch-body"><div class="index">{idx_html(idx_items[half:])}</div></div></div>', cls="chapter-page", style=XS)

p = book.add('<div class="snow"></div><div class="safe center"><div class="ornament"></div><div class="kicker" style="color:#E8C766;font-size:10pt">Until Next Time</div>'
             '<h2 class="display" style="margin:.2in 0 .3in">Dogs Are Weird.<br><span class="gold">We Love Them.</span></h2>'
             + "".join(f'<p style="max-width:5.6in;margin-bottom:.16in;font-size:13pt">{e(t)}</p>' for t in X.CLOSING)
             + '<p style="font:700 26pt Caveat;color:#E8C766;margin-top:.2in">Merry Christmas! Woof!</p></div>', cls="xmas")
toc.append(("The End", "A Merry Little Goodbye", p))

if len(book.pages) % 2:
    book.add('<div class="safe center"><p style="font:700 22pt Caveat;color:var(--ink-soft)">This page intentionally left blank<br>(the dog ate the content).</p></div>', folio=False)

# ---------------- TOC ----------------
groups = []
for g, t, pg in toc:
    if not groups or groups[-1][0] != g:
        groups.append((g, []))
    groups[-1][1].append((t, pg))
cat_color = {c[1]: c[4] for c in X.CATEGORIES}
toc_html = ('<div class="safe chapter"><div class="ch-head"><div class="kicker" style="--c:var(--red)">Contents</div>'
            '<h2 class="display">What\'s Inside <em style="color:var(--red)">(Besides Fur)</em></h2></div><div class="ch-body"><div class="toc">')
for g, items in groups:
    col = cat_color.get(g, "#B3261E")
    toc_html += f'<div class="grp"><h4 style="color:{col}">{e(g)}</h4>' + "".join(
        f'<div class="it"><span>{"<b>" + e(t) + "</b>" if t.startswith("Meet") else e(t)}</span><span class="dots"></span><span>{pg}</span></div>' for t, pg in items) + "</div>"
toc_html += "</div></div></div>"
inner, cls, style, folio = book.pages[TOC_PAGE - 1]
book.pages[TOC_PAGE - 1] = (toc_html, cls, "--c:#B3261E", folio)

doc = f'''<!doctype html><html lang="en-US"><head><meta charset="utf-8"><title>Dogs Are Weird. We Love Them. (Interior)</title>
<link rel="stylesheet" href="style.css"></head><body>{book.render()}
<script>
// Auto-fit: shrink text inside any overflowing fit container until it fits.
window.__fitReport = [];
document.fonts.ready.then(() => {{
const fits = el => el.scrollHeight <= el.clientHeight + 1;
document.querySelectorAll('.fitbox, .ch-body, .toc').forEach(el => {{
  if (el.querySelector('.gallery')) return;
  const set = v => {{ el.style.fontSize = v + 'px'; }};
  const start = parseFloat(getComputedStyle(el).fontSize);
  const cap = start * (el.classList.contains('ch-body') ? 1.45 : 1.12);
  let fs = start;
  while (fits(el) && fs < cap) {{ fs += 0.25; set(fs); }}
  while (!fits(el) && fs > 9.6) {{ fs -= 0.25; set(fs); }}
  const page = el.closest('.page').dataset.p;
  if (!fits(el)) window.__fitReport.push({{page, status: 'OVERFLOW'}});
  else if (fs < start) window.__fitReport.push({{page, status: 'shrunk', from: (start*72/96).toFixed(1), to: (fs*72/96).toFixed(1)}});
}});
window.__fitDone = true;
}});
</script></body></html>'''
(ROOT / "build" / "interior.html").write_text(doc)

manifest = {
    "pages": len(book.pages),
    "breeds": [{"no": i + 1, "name": b.name, "category": CAT_DATA[b.category][1], "img_id": b.img_id, "page": index_pages[b.name],
                "has_image": bool(find_img(b.img_id))} for i, b in enumerate(ALL)],
}
(ROOT / "build" / "manifest.json").write_text(json.dumps(manifest, indent=1))
print(f"pages={len(book.pages)} breeds={len(ALL)}")
