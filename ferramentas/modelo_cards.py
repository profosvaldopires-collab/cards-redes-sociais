from PIL import Image, ImageDraw, ImageFont, ImageOps

W = H = 1080
BG = (247, 244, 236)
BLUE = (6, 52, 165)
GOLD = (204, 152, 28)
RED = (196, 40, 40)
FD = "/usr/share/fonts/truetype/google-fonts/"
F = lambda w, s: ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
FOOTER = "Prof. Osvaldo Pires  |  Licitações e Contratos"
MAXW = W - 2 * 90


SYM = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
def _symf(font):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font.size)
def tl(d, text, font):
    return sum(d.textlength(ch, font=_symf(font) if ch in "→✕" else font) for ch in text)
def tx(d, xy, text, font, fill):
    x, y = xy
    for ch in text:
        f = _symf(font) if ch in "→✕" else font
        d.text((x, y + (font.size*0.12 if ch in "→✕" else 0)), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f)

def base():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([34, 34, W - 34, H - 34], outline=BLUE, width=3)
    return im, d


def tracked(d, xy, text, font, fill, track=4, anchor_center=False):
    widths = [d.textlength(ch, font=font) + track for ch in text]
    total = sum(widths) - track
    x, y = xy
    if anchor_center:
        x = (W - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w
    return total


def seg_width(d, segs, font):
    return sum(tl(d, t, font) for t, _ in segs)


def rich_lines(d, lines, weight, size, y, center=False, gap=1.12, x0=90, maxw=MAXW):
    # shrink until all lines fit
    while True:
        font = F(weight, size)
        if all(seg_width(d, l, font) <= maxw for l in lines):
            break
        size -= 2
    for l in lines:
        w = seg_width(d, l, font)
        x = (W - w) / 2 if center else x0
        for t, c in l:
            tx(d, (x, y), t, font, c)
            x += tl(d, t, font)
        y += int(size * gap)
    return y


def hline(d, y, x1, x2, color=GOLD, w=3):
    d.line([x1, y, x2, y], fill=color, width=w)


def footer(d):
    hline(d, 955, 90, W - 90, w=2)
    f = F("Regular", 24)
    w = d.textlength(FOOTER, font=f)
    d.text(((W - w) / 2, 975), FOOTER, font=f, fill=BLUE)


def button(d, text, y, fill=GOLD, color=BLUE, size=34):
    f = F("Bold", size)
    w = tl(d, text, f)
    pw, ph = 56, 26
    x = (W - w) / 2
    d.rounded_rectangle([x - pw, y, x + w + pw, y + size + 2 * ph], radius=(size + 2 * ph) // 2, fill=fill)
    tx(d, (x, y + ph - 4), text, f, color)


B = lambda t: (t, BLUE)
G = lambda t: (t, GOLD)


def card_std(tag, head, body, out, body_size=40, extra=None):
    im, d = base()
    tracked(d, (90, 95), tag, F("SemiBold", 28) if False else F("Medium", 28), BLUE, track=5)
    y = rich_lines(d, head, "Bold", 84, 230)
    hline(d, y + 35, 90, 560)
    y += 110
    y = rich_lines(d, body, "Medium", body_size, y, gap=1.6)
    if extra:
        extra(im, d, y)
    footer(d)
    im.save(out)


# 1 capa
im, d = base()
tracked(d, (0, 120), "ACÓRDÃO EM 60s  •  TCU 2921/2026 – PLENÁRIO", F("Medium", 28), BLUE, track=4, anchor_center=True)
y = rich_lines(d, [[B("COMO SE CONTA O")], [G("PRAZO"), B(" DA")], [B("LICITAÇÃO?")]], "Bold", 104, 245, center=True, gap=1.08)
hline(d, y + 30, 240, 840)
y = rich_lines(d, [[B("O TCU aplicou os arts. 55 e 183")], [B("da Lei 14.133/2021")]], "Regular", 40, y + 70, center=True, gap=1.35)
button(d, "ARRASTE  →", y + 55)
footer(d)
im.save("01.png")

# 2 regra
card_std("A REGRA",
         [[B("EXCLUI O "), G("DIA DO COMEÇO.")], [B("INCLUI O DO VENCIMENTO.")]],
         [[G("Art. 55: "), B("prazo mínimo (pregão: 8 dias úteis)")],
          [G("Art. 183: "), B("exclui o começo, inclui o fim")],
          [G("Art. 183, § 1º, I: "), B("o prazo começa no")],
          [B("1º dia útil após a divulgação no PNCP")]],
         "02.png", body_size=38)

# 3 erro
card_std("O ERRO MAIS COMUM",
         [[B("CONTAR O "), G("DIA SEGUINTE")], [B("À DIVULGAÇÃO COMO")], [B("O 1º DIA DO PRAZO")]],
         [[B("O pregoeiro contou 18/9 (sex)")],
          [B("como o 1º dia útil.")],
          [B("Para o TCU, 18/9 é o "), G("dia do começo")],
          [B("e sai da conta.")]],
         "03.png", body_size=40)

# 4 linha do tempo
im, d = base()
tracked(d, (90, 95), "NA PRÁTICA", F("Medium", 28), BLUE, track=5)
y = rich_lines(d, [[B("A "), G("CONTA"), B(" DO")], [B("CASO CONCRETO")]], "Bold", 74, 200)
hline(d, y + 30, 90, 560)
items = [("17/9 (qui)", "divulgação no PNCP", BLUE, GOLD),
         ("18/9 (sex)", "dia do começo: excluído", BLUE, GOLD),
         ("21/9 (seg)", "1º dia computado", BLUE, GOLD),
         ("29/9 (ter), 9h", "propostas encerradas  ✕", RED, RED),
         ("30/9 (qua)", "8º dia útil: fim do prazo", BLUE, BLUE)]
f1, f2 = F("Bold", 33), F("Medium", 33)
yy = y + 80
step = 92
d.line([118, yy + 22, 118, yy + 22 + step * (len(items) - 1)], fill=GOLD, width=3)
for date, txt, col, dot in items:
    d.ellipse([106, yy + 10, 130, yy + 34], fill=dot)
    d.text((160, yy), date, font=f1, fill=col)
    x = 160 + d.textlength(date, font=f1)
    tx(d, (x, yy), "  —  " + txt, f2, col)
    yy += step
footer(d)
im.save("04.png")


# 5 detalhe
def quote_box(im, d, y):
    q = ["“Encerrar seu recebimento às 9h desse dia",
         "não lhes assegurou a integralidade desse prazo.”"]
    f = F("Medium", 31)
    top = y + 20
    d.rectangle([110, top, W - 110, top + 190], outline=GOLD, width=3)
    yy = top + 28
    for l in q:
        w = d.textlength(l, font=f)
        d.text(((W - w) / 2, yy), l, font=f, fill=BLUE)
        yy += 46
    s = "TCU, Acórdão 2921/2026 – Plenário, voto, § 11"
    fs = F("Regular", 22)
    d.text(((W - d.textlength(s, font=fs)) / 2, yy + 14), s, font=fs, fill=GOLD)


card_std("O DETALHE QUE PASSA BATIDO",
         [[B("O ÚLTIMO DIA")], [B("VALE "), G("INTEIRO")]],
         [[G("Art. 183: "), B("inclui-se o dia do vencimento.")],
          [B("Mesmo se 29/9 fosse o 8º dia,")],
          [B("encerrar às 9h não bastaria.")]],
         "05.png", body_size=36, extra=quote_box)

# 6 consequencia
card_std("A CONSEQUÊNCIA",
         [[B("RECONHECEU A FALHA.")], [G("NÃO ANULOU.")]],
         [[B("Disputa efetiva: proposta vencedora")],
          [B("cerca de 37% abaixo do estimado")],
          [B("Sem anulação, sem republicação, sem cautelar")],
          [B("Resultado: "), G("ciência ao órgão e arquivamento")]],
         "06.png", body_size=36)


# 7 para guardar
def cta(im, d, y):
    button(d, "SALVE E COMPARTILHE", y + 30)


card_std("PARA GUARDAR",
         [[B("AGENTE DE CONTRATAÇÃO:")], [B("CONTE DO "), G("PNCP + 1")], [G("DIA ÚTIL")]],
         [[B("Encerre as propostas só depois")],
          [B("do último dia inteiro.")],
          [G("Licitante: "), B("confira a contagem antes")],
          [B("de impugnar (art. 164).")]],
         "07.png", body_size=36, extra=cta)

# 8 foto
im, d = base()
photo = Image.open("ferramentas/assets/foto-oficial.jpg").convert("RGB")
pw, ph = 430, 760
photo = ImageOps.fit(photo, (pw, ph), centering=(0.5, 0.15))
mask = Image.new("L", (pw, ph), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw, ph], radius=28, fill=255)
px, py = W - 90 - pw, 140
im.paste(photo, (px, py), mask)
d.rounded_rectangle([px, py, px + pw, py + ph], radius=28, outline=GOLD, width=4)
tracked(d, (90, 150), "ACÓRDÃO EM 60s", F("Medium", 28), BLUE, track=5)
y = rich_lines(d, [[B("Prof.")], [B("Osvaldo")], [B("Pires")]], "Bold", 76, 230, maxw=px - 120, gap=1.05)
hline(d, y + 20, 90, 330)
y = rich_lines(d, [[G("Licitações e Contratos")]], "SemiBold" if False else "Medium", 32, y + 50, maxw=px - 120)
y = rich_lines(d, [[B("Toda semana, um")], [B("acórdão explicado")], [B("em 60 segundos.")]], "Regular", 32, y + 30, maxw=px - 120, gap=1.4)
f = F("Bold", 28)
t = "SIGA  →"
bx, by = 90, y + 40
tw = tl(d, t, f)
d.rounded_rectangle([bx, by, bx + tw + 80, by + 72], radius=36, fill=GOLD)
tx(d, (bx + 40, by + 18), t, f, BLUE)
d.text((90, by + 100), "@prof.osvaldopires.adv", font=F("Medium", 26), fill=BLUE)
footer(d)
im.save("08.png")
print("ok")
