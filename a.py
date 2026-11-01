import math as m
import random as r
import turtle as t
import tkinter.font as tkf

# ------------------------------------------------------------------
#  100 WAYS TO SAY SORRY
#  A rotating wheel of 100 apologies. Colours travel from cool indigo
#  (the hurt) to warm gold (the making-up). The centre reads each one.
# ------------------------------------------------------------------

TICK = 16
INTERVAL = 9            # ticks between each apology appearing
R0 = 182                # where the spokes start
R_MAX = 342             # where the longest spoke may end
SERIF = "Georgia"
SANS = "Helvetica"

BG_TOP = (0.02, 0.02, 0.02)
BG_BOT = (0.15, 0.02, 0.03)
BGC = (0.01, 0.01, 0.01)
CREAM = (1.0, 1.0, 1.0)
GOLD = (1.0, 0.05, 0.08)
FLASH = (1.0, 1.0, 1.0)

STOPS = [
    (0.35, 0.0, 0.02),
    (0.75, 0.0, 0.04),
    (1.0, 0.05, 0.08),
    (1.0, 0.45, 0.45),
    (1.0, 1.0, 1.0),
]

PHRASES = [
    "I'm so sorry", "I was wrong", "Please forgive me",
    "I take full responsibility", "That was my mistake",
    "I should have listened", "I owe you an apology",
    "I didn't mean to hurt you", "I'm sorry I let you down", "I messed up",
    "I'm truly sorry", "I regret my words", "I was selfish",
    "I should have been there", "I'm sorry for yelling",
    "I'm sorry I wasn't honest", "I was not thinking of you",
    "I handled it badly", "I'm ashamed of how I acted", "You deserved better",
    "I'm sorry I broke my promise", "I'm sorry I forgot",
    "I put my pride first", "I'm sorry I didn't call", "I was unfair to you",
    "I judged too quickly", "I'm sorry I dismissed you",
    "I should have trusted you", "I'm sorry I interrupted", "I wasn't fair",
    "I made it about me", "I'm sorry I was distant",
    "I'm sorry I was late again", "I ignored what you needed",
    "I let my temper win", "I said things I didn't mean",
    "I'm sorry I made you worry", "I didn't see your side",
    "I should have asked first", "I'm sorry I stayed silent",
    "I took you for granted", "I'm sorry I was careless",
    "My words were unkind", "I'm sorry for the silence",
    "I was too proud to say it", "I'm sorry I wasn't listening",
    "I hurt someone I love", "I'm sorry I broke your trust",
    "I should have said it sooner", "I'm sorry it took so long",
    "I'm sorry I made excuses", "No excuses, just sorry",
    "I want to make it right", "Let me make it up to you",
    "I'm here to listen now", "I'll do better, I promise",
    "I'll be more patient", "I'm learning from this",
    "Tell me how to fix it", "I miss you, and I'm sorry",
    "You matter more than winning", "I can't lose you over this",
    "I'm sorry for the hurt", "I'm sorry for the tears",
    "I wish I could undo it", "I'd take it back if I could",
    "I'm sorry for my harsh words", "I was scared and lashed out",
    "I let stress speak for me", "I'm sorry I wasn't kind",
    "You didn't deserve that", "It was never your fault",
    "I'm sorry I blamed you", "I'm sorry I compared us",
    "I'm sorry I overreacted", "I misunderstood you",
    "I wasn't there for you", "I should have shown up",
    "I'm sorry I missed it", "I forgot what mattered",
    "I was busy, not present", "I took it out on you",
    "I'm sorry for the bad timing", "I made you feel small",
    "I'm sorry I wasn't gentle", "I'm sorry I held a grudge",
    "I let it go on too long", "I should have spoken first",
    "I'm sorry I lied", "I'm sorry I hid the truth",
    "You can trust me again", "Give me another chance", "I'm ready to talk",
    "I'm sorry, and I mean it", "I'm sorry from my heart",
    "Forgive me when you can", "I'm grateful for you",
    "I love you, and I'm sorry", "Can we start over?", "I'm sorry. Always.",
]
N = len(PHRASES)
assert N == 100, N

s = t.Screen()
s.setup(800, 800)


def hx(c):
    return "#%02x%02x%02x" % tuple(int(max(0, min(1, v)) * 255) for v in c)


def mix(a, b, k):
    return tuple(p + (q - p) * k for p, q in zip(a, b))


def clamp(v):
    return max(0.0, min(1.0, v))


def palette(k):
    k = clamp(k) * (len(STOPS) - 1)
    i = min(int(k), len(STOPS) - 2)
    return mix(STOPS[i], STOPS[i + 1], k - i)


s.bgcolor(hx(BG_TOP))
s.title("100 Ways to Say Sorry")
s.tracer(0)
cv = s.getcanvas()
rng = r.Random(7)

# ---------------- background: dusk gradient, stars, rings ----------------
BANDS = 80
for i in range(BANDS):
    y0 = -420 + 840 * i / BANDS
    c = mix(BG_TOP, BG_BOT, (i / (BANDS - 1)) ** 1.4)
    cv.create_rectangle(-430, y0, 430, y0 + 840 / BANDS + 1,
                        fill=hx(c), outline="")

stars = []
for _ in range(90):
    x, y = rng.uniform(-400, 400), rng.uniform(-400, 400)
    if m.hypot(x, y) < 372:
        continue
    b = rng.uniform(0.15, 0.5)
    sz = rng.choice((0.8, 1, 1, 1.4))
    stars.append((cv.create_oval(x - sz, y - sz, x + sz, y + sz,
                                 fill=hx(mix(BGC, CREAM, b)), outline=""), b))

for rad, k in ((R0 - 14, 0.35), (R0 - 19, 0.12)):
    cv.create_oval(-rad, -rad, rad, rad, outline=hx(mix(BG_TOP, GOLD, k)),
                   width=1)
RING = 366
cv.create_oval(-RING, -RING, RING, RING,
               outline=hx(mix(BG_TOP, GOLD, 0.18)), width=1)

# ---------------- spokes ----------------
fs = 9
while fs > 6:
    f = tkf.Font(root=cv, family=SANS, size=fs)
    if max(f.measure(p) for p in PHRASES) <= R_MAX - R0:
        break
    fs -= 1

spokes = []
for i, text in enumerate(PHRASES):
    th = m.pi / 2 - 2 * m.pi * i / N          # start at 12 o'clock, go clockwise
    sid = cv.create_text(0, 0, text=text, font=(SANS, fs),
                         fill=hx(BGC), anchor="w")
    spokes.append(dict(id=sid, th=th, color=palette(i / (N - 1)),
                       born=None))

# ---------------- centre ----------------
title = cv.create_text(0, -72, text="1 0 0   W A Y S   T O   S A Y",
                       font=(SANS, 8, "bold"), fill=hx(BGC))
title2 = cv.create_text(0, -56, text="S O R R Y",
                        font=(SANS, 8, "bold"), fill=hx(BGC))
phrase = cv.create_text(0, -2, text="", font=(SERIF, 19, "italic"),
                        fill=hx(BGC), width=250, justify="center")
rule = cv.create_line(-26, 52, 26, 52, fill=hx(BGC), width=1)
counter = cv.create_text(0, 72, text="", font=(SANS, 9, "bold"),
                         fill=hx(BGC))

arc = cv.create_arc(-RING, -RING, RING, RING, start=90, extent=-0.01,
                    style="arc", outline=hx(GOLD), width=2)

# ---------------- state ----------------
tick = 0
rot = 0.0
shown = 0
cur = None            # index of phrase in the centre
cur_t = 0             # tick it appeared
done_t = None


def show_center(i):
    global cur, cur_t
    cur, cur_t = i, tick
    cv.itemconfig(phrase, text=PHRASES[i])
    cv.itemconfig(counter, text="N° %03d" % (i + 1))


def place(p, slide):
    a = (p["th"] + rot) % (2 * m.pi)
    rr = R0 + slide
    x, y = rr * m.cos(a), -rr * m.sin(a)
    if m.pi / 2 < a < 3 * m.pi / 2:
        ang, anc = m.degrees(a) + 180, "e"
    else:
        ang, anc = m.degrees(a), "w"
    cv.coords(p["id"], x, y)
    cv.itemconfig(p["id"], angle=ang % 360, anchor=anc)


def step():
    global tick, rot, shown, done_t
    tick += 1
    rot -= 0.0006 + (0.0006 if shown >= N else 0)

    # reveal the next apology
    if shown < N and tick % INTERVAL == 0:
        spokes[shown]["born"] = tick
        show_center(shown)
        shown += 1
        cv.itemconfig(arc, extent=-max(0.01, min(359.9, 360 * shown / N)))
        if shown == N:
            done_t = tick

    # when finished, keep the centre alive
    if done_t and (tick - done_t) > 150 and (tick - cur_t) > 170:
        show_center(rng.choice([k for k in range(N) if k != cur]))

    # spokes: fade in, slide out, sweeping highlight when complete
    sweep = (tick * 0.22) % N
    for i, p in enumerate(spokes):
        if p["born"] is None:
            continue
        u = clamp((tick - p["born"]) / 40)
        e = 1 - (1 - u) ** 3
        place(p, (1 - e) * 18)
        glow = 0.0
        if done_t:
            d = abs(i - sweep)
            d = min(d, N - d)
            glow = m.exp(-(d / 3.0) ** 2) * 0.65
        pop = 0.9 * m.sin(m.pi * clamp((u - 0.1) / 0.5)) if u < 0.6 else 0
        col = mix(mix(BGC, p["color"], 0.82 * e), FLASH, max(glow, pop))
        cv.itemconfig(p["id"], fill=hx(col))

    # centre text
    k = clamp((tick - 8) / 40)
    cv.itemconfig(title, fill=hx(mix(BGC, GOLD, 0.85 * k)))
    cv.itemconfig(title2, fill=hx(mix(BGC, GOLD, 0.85 * k)))
    cv.itemconfig(rule, fill=hx(mix(BGC, GOLD, 0.5 * k)))
    if cur is not None:
        fe = clamp((tick - cur_t) / 14)
        c = mix(BGC, mix(CREAM, spokes[cur]["color"], 0.18), fe)
        cv.itemconfig(phrase, fill=hx(c))
        cv.itemconfig(counter, fill=hx(mix(BGC, GOLD, 0.75 * fe)))

    # twinkle
    for _ in range(2):
        sid, b = rng.choice(stars)
        cv.itemconfig(sid, fill=hx(mix(BGC, CREAM, b * rng.uniform(0.4, 1.3))))

    cv.after(TICK, step)


try:
    cv.after(300, step)
    t.done()
except (t.Terminator, Exception):
    pass