#!/usr/bin/env python3
"""Regenerate every SVG asset the profile README uses.

Design contract (ui-ux-pro-max, "Developer Tool / IDE" palette):
    bg #0F172A   card #0E1223   border #1E293B   line #334155
    fg #F8FAFC   muted #94A3B8  accent #22C55E

Fonts are system stacks on purpose. GitHub serves README images through its
camo proxy and renders them as <img>, and an <img>-embedded SVG cannot fetch
external resources -- an @import of Google Fonts silently falls back to serif.
"""
import os
import textwrap

BG, CARD, BORDER = "#0F172A", "#0E1223", "#1E293B"
FG, MUTED, ACCENT = "#F8FAFC", "#94A3B8", "#22C55E"
LINE = "#334155"

MONO = "'JetBrains Mono','SFMono-Regular',Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',-apple-system,'Helvetica Neue',Arial,sans-serif"

NL = "\n"
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def write(path, body):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(body)
    print("  wrote {} ({:,} bytes)".format(path, len(body)))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


DEFS = """  <defs>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{border}"/>
    </pattern>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{accent}" stop-opacity=".16"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0"/>
    </radialGradient>
  </defs>""".format(border=BORDER, accent=ACCENT)


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1280, 400
    stats = [
        ("43", "public repos"),
        ("469", "contributions / yr"),
        ("417", "commits / yr"),
        ("8", "stars earned"),
    ]
    chips, x = [], 56
    for value, label in stats:
        w = 268
        chips.append(
            '  <g transform="translate({x},296)">{nl}'
            '    <rect width="{w}" height="64" rx="10" fill="{card}" stroke="{border}"/>{nl}'
            '    <text x="20" y="28" font-family="{mono}" font-size="22" font-weight="700" fill="{accent}">{value}</text>{nl}'
            '    <text x="20" y="48" font-family="{sans}" font-size="12.5" fill="{muted}" letter-spacing=".6">{label}</text>{nl}'
            "  </g>".format(x=x, w=w, nl=NL, card=CARD, border=BORDER, mono=MONO,
                            accent=ACCENT, sans=SANS, muted=MUTED,
                            value=value, label=label))
        x += w + 16

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        'aria-label="Mohamed Badr, full-stack developer in Cairo. 43 public repositories, 469 contributions per year, '
        '417 commits per year, 8 stars earned.">{nl}'
        "{defs}{nl}"
        '  <rect width="{W}" height="{H}" rx="16" fill="{bg}"/>{nl}'
        '  <rect width="{W}" height="{H}" rx="16" fill="url(#dots)"/>{nl}'
        '  <ellipse cx="1080" cy="70" rx="440" ry="260" fill="url(#glow)"/>{nl}'
        '  <rect x=".5" y=".5" width="{W1}" height="{H1}" rx="16" fill="none" stroke="{border}"/>{nl}{nl}'
        "  <!-- terminal chrome -->{nl}"
        '  <line x1="0" y1="52" x2="{W}" y2="52" stroke="{border}"/>{nl}'
        '  <circle cx="34" cy="26" r="6" fill="#EF4444"/>{nl}'
        '  <circle cx="56" cy="26" r="6" fill="#F59E0B"/>{nl}'
        '  <circle cx="78" cy="26" r="6" fill="{accent}"/>{nl}'
        '  <text x="112" y="31" font-family="{mono}" font-size="13" fill="{muted}">cBadr &#8212; ~/projects</text>{nl}{nl}'
        '  <text x="56" y="118" font-family="{mono}" font-size="15" fill="{muted}">'
        '<tspan fill="{accent}">$</tspan> whoami</text>{nl}{nl}'
        '  <text x="56" y="188" font-family="{sans}" font-size="52" font-weight="700" fill="{fg}" '
        'letter-spacing="-1">Mohamed Badr</text>{nl}{nl}'
        '  <text x="56" y="230" font-family="{sans}" font-size="19" fill="{muted}">'
        "Full-stack developer. I build SaaS products with Next.js, Laravel and Postgres.</text>{nl}"
        '  <text x="56" y="260" font-family="{sans}" font-size="19" fill="{muted}">Cairo, Egypt.</text>{nl}'
        '  <rect x="184" y="243" width="9" height="20" fill="{accent}">{nl}'
        '    <animate attributeName="opacity" values="1;1;0;0" dur="1.15s" repeatCount="indefinite"/>{nl}'
        "  </rect>{nl}{nl}"
        "{chips}{nl}"
        "</svg>{nl}"
    ).format(W=W, H=H, W1=W - 1, H1=H - 1, nl=NL, defs=DEFS, bg=BG, border=BORDER,
             accent=ACCENT, mono=MONO, sans=SANS, muted=MUTED, fg=FG,
             chips=NL.join(chips))


# ----------------------------------------------------------- languages
def langs():
    data = [
        ("TypeScript", 35.10, "#3178c6"),
        ("PHP", 25.88, "#4F5D95"),
        ("JavaScript", 17.27, "#f1e05a"),
        ("PL/pgSQL", 9.68, "#336790"),
        ("CSS", 8.79, "#663399"),
        ("Other", 3.28, "#64748B"),
    ]
    W, H = 440, 236
    bar_x, bar_w, bar_y = 24, W - 48, 76

    segs, x = [], float(bar_x)
    for _, pct, col in data:
        w = bar_w * pct / 100.0
        segs.append('    <rect x="{:.1f}" y="{}" width="{:.1f}" height="12" fill="{}"/>'.format(x, bar_y, w, col))
        x += w

    rows, y = [], 124
    for i, (name, pct, col) in enumerate(data):
        cx = 30 if i % 2 == 0 else 240
        rows.append(
            "  <g>{nl}"
            '    <circle cx="{cx}" cy="{cy}" r="5" fill="{col}"/>{nl}'
            '    <text x="{tx}" y="{y}" font-family="{sans}" font-size="13" fill="{fg}">{name}</text>{nl}'
            '    <text x="{px}" y="{y}" font-family="{mono}" font-size="12.5" fill="{muted}" text-anchor="end">{pct:.1f}%</text>{nl}'
            "  </g>".format(nl=NL, cx=cx, cy=y - 4, col=col, tx=cx + 14, y=y,
                            sans=SANS, fg=FG, name=esc(name), px=cx + 176,
                            mono=MONO, muted=MUTED, pct=pct))
        if i % 2 == 1:
            y += 30

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        'aria-label="Language distribution across 43 public repositories: TypeScript 35.1 percent, PHP 25.9, '
        'JavaScript 17.3, PL/pgSQL 9.7, CSS 8.8, other 3.3.">{nl}'
        '  <rect width="{W}" height="{H}" rx="12" fill="{card}"/>{nl}'
        '  <rect x=".5" y=".5" width="{W1}" height="{H1}" rx="12" fill="none" stroke="{border}"/>{nl}'
        '  <text x="24" y="36" font-family="{sans}" font-size="15" font-weight="600" fill="{fg}">Languages</text>{nl}'
        '  <text x="24" y="56" font-family="{sans}" font-size="12" fill="{muted}">by bytes, across 43 public repositories</text>{nl}'
        '  <clipPath id="barclip"><rect x="{bx}" y="{by}" width="{bw}" height="12" rx="6"/></clipPath>{nl}'
        '  <g clip-path="url(#barclip)">{nl}{segs}{nl}  </g>{nl}'
        "{rows}{nl}"
        "</svg>{nl}"
    ).format(W=W, H=H, W1=W - 1, H1=H - 1, nl=NL, card=CARD, border=BORDER,
             sans=SANS, fg=FG, muted=MUTED, bx=bar_x, by=bar_y, bw=bar_w,
             segs=NL.join(segs), rows=NL.join(rows))


# ---------------------------------------------------------- work cards
REPO_ICON = ("M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 "
             "0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 "
             "1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 "
             ".25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.25.25 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z")

STAR_ICON = ("M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 "
             "4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 "
             "6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z")

PROJECTS = [
    ("Tourism-Site",
     "Asset-free transport brokerage in Egypt. Customers get an instant quote, jobs broadcast to subcontractors, first to accept wins.",
     "TypeScript", "#3178c6", 0, None),
    ("php-redirector",
     "Routes visitors by country, device, browser and connection type, then pings Telegram on every hit. Zero dependencies.",
     "PHP", "#4F5D95", 0, None),
    ("Shortaty",
     "Multi-domain URL shortener. Rule-based targeting, bot-filtered analytics, and a Telegram bot per user.",
     "TypeScript", "#3178c6", 1, None),
    ("Issabel",
     "One-line installer that wires dongle_chain into Issabel so GSM modems work out of the box.",
     "Shell", "#89e051", 3, None),
    ("Al-Kayan",
     "Multi-tenant SaaS for football academies: training, attendance, matches, subscriptions and reports.",
     "TypeScript", "#3178c6", 1, "al-kayan.vercel.app"),
    ("Coding-Site",
     "Agency platform where clients browse services, order, pay and follow delivery. Arabic and English.",
     "TypeScript", "#3178c6", 1, "coding-site-coral.vercel.app"),
]


def card(name, desc, lang, col, stars, demo):
    W, H = 440, 186
    lines = textwrap.wrap(desc, width=54)[:3]
    body = NL.join(
        '  <text x="24" y="{y}" font-family="{sans}" font-size="13" fill="{muted}">{t}</text>'.format(
            y=88 + i * 20, sans=SANS, muted=MUTED, t=esc(line))
        for i, line in enumerate(lines))

    meta = ['  <circle cx="28" cy="{cy}" r="5.5" fill="{col}"/>{nl}'
            '  <text x="42" y="{ty}" font-family="{sans}" font-size="12.5" fill="{muted}">{lang}</text>'.format(
                cy=H - 26, col=col, nl=NL, ty=H - 21, sans=SANS, muted=MUTED, lang=esc(lang))]

    x = 42 + len(lang) * 7 + 22
    if stars:
        meta.append('  <path d="{d}" transform="translate({x},{y}) scale(.82)" fill="{muted}"/>{nl}'
                    '  <text x="{tx}" y="{ty}" font-family="{sans}" font-size="12.5" fill="{muted}">{s}</text>'.format(
                        d=STAR_ICON, x=x, y=H - 33, muted=MUTED, nl=NL,
                        tx=x + 18, ty=H - 21, sans=SANS, s=stars))
    if demo:
        meta.append('  <text x="{x}" y="{y}" font-family="{mono}" font-size="11.5" fill="{accent}" '
                    'text-anchor="end">{d}</text>'.format(
                        x=W - 24, y=H - 21, mono=MONO, accent=ACCENT, d=esc(demo)))

    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        'aria-label="{name}: {desc} Written in {lang}, {stars} stars.">{nl}'
        '  <rect width="{W}" height="{H}" rx="12" fill="{card}"/>{nl}'
        '  <rect x=".5" y=".5" width="{W1}" height="{H1}" rx="12" fill="none" stroke="{border}"/>{nl}'
        '  <rect x="0" y="0" width="{W}" height="3" rx="1.5" fill="{col}" opacity=".85"/>{nl}'
        '  <path d="{icon}" transform="translate(24,32) scale(1.05)" fill="{muted}"/>{nl}'
        '  <text x="48" y="45" font-family="{sans}" font-size="17" font-weight="600" fill="{fg}">{name}</text>{nl}'
        '  <line x1="24" y1="62" x2="{lx}" y2="62" stroke="{border}"/>{nl}'
        "{body}{nl}"
        "{meta}{nl}"
        "</svg>{nl}"
    ).format(W=W, H=H, W1=W - 1, H1=H - 1, nl=NL, name=esc(name), desc=esc(desc),
             lang=esc(lang), stars=stars, card=CARD, border=BORDER, col=col,
             icon=REPO_ICON, muted=MUTED, sans=SANS, fg=FG, lx=W - 24,
             body=body, meta=NL.join(meta))


if __name__ == "__main__":
    print("building assets...")
    write("assets/hero.svg", hero())
    write("assets/languages.svg", langs())
    for project in PROJECTS:
        write("assets/work/{}.svg".format(project[0]), card(*project))
    print("done.")
