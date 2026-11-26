# Uras English Cup - leveled word bank
#
# Curated for a 7-year-old (Grade 1-2 level, Turkish MEB themes + football, cars, video games).
# The dwyl/english-words list (~470k words, unfiltered, ungraded) is only a spelling reference;
# it is not used as a source because it has no difficulty levels and includes unsuitable words.
#
# Run:  python -I vocab.py
#   1) drops words the site already teaches (weekly words, Word Tower, Typing Turbo)
#   2) writes the VOCAB_LEVELS block into uras-english-cup.html between the VOCAB markers
#   3) writes kelime-listesi.html (printable) - build.ps1 turns it into kelime-listesi.pdf
import html, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE / 'uras-english-cup.html'

# en : tr : emoji (emoji optional)
LEVELS = [
 dict(n=1, name='Starter', tr='Başlangıç', sub='1. sınıf · kısa ve somut kelimeler (3–4 harf)', words='''
ant:karınca:🐜|hen:tavuk:🐔|goat:keçi:🐐|lamb:kuzu:🐑|van:minibüs:🚐|jet:jet uçağı:✈️|cap:kasket:🧢|mug:kupa bardak:☕
pot:tencere:🍲|jam:reçel:🍓|nut:fındık:🥜|pie:turta:🥧|tea:çay:🍵|zoo:hayvanat bahçesi:🦁|mum:anne:👩|dad:baba:👨
lip:dudak:👄|toe:ayak parmağı:🦶|hug:sarılmak:🤗|sit:oturmak:🪑|eat:yemek yemek:🍽️|see:görmek:👀|new:yeni:🆕|old:eski / yaşlı:👴
wet:ıslak:💦|dry:kuru:☀️|fun:eğlence:🎉|net:file:🥅|fan:taraftar:📣|hop:sekmek:🐇|tap:dokunmak:👆|hill:tepe:⛰️
lake:göl:🏞️|park:park:🛝|road:yol:🛣️|tyre:lastik:🛞|seat:koltuk:💺|horn:korna:📯|lamp:lamba:💡|wall:duvar:🧱
roof:çatı:🏠|desk:sıra / masa:🪑|rice:pirinç:🍚|soup:çorba:🍲|corn:mısır:🌽|pear:armut:🍐|kiwi:kivi:🥝|knee:diz:🦵
neck:boyun|hair:saç:💇|face:yüz:🙂|head:baş:🗣️|ring:yüzük:💍|bell:zil:🔔|gift:hediye:🎁|doll:oyuncak bebek:🪆
drum:davul:🥁|race:yarış:🏁|taxi:taksi:🚕|fast:hızlı:💨|gold:altın:🥇|shop:dükkan:🏪|farm:çiftlik:🚜|nest:yuva:🪺
'''),
 dict(n=2, name='Explorer', tr='Kaşif', sub='1.–2. sınıf · günlük hayat, okul ve oyun (4–6 harf)', words='''
jersey:forma:👕|coach:antrenör:📋|match:maç:⚽|boots:krampon:👟|wheel:tekerlek:🛞|brake:fren:🛑|driver:sürücü:🧑‍✈️|petrol:benzin:⛽
scooter:scooter:🛴|tractor:traktör:🚜|puzzle:yapboz:🧩|guitar:gitar:🎸|piano:piyano:🎹|paper:kağıt:📄|glue:yapıştırıcı:🧴|eraser:silgi:🧽
lesson:ders:📚|class:sınıf:🏫|laugh:gülmek:😂|cry:ağlamak:😢|angry:kızgın:😠|tired:yorgun:🥱|hungry:aç:🍽️|thirsty:susamış:🥤
scared:korkmuş:😨|brave:cesur:🦸|strong:güçlü:💪|tall:uzun boylu:🦒|short:kısa:📏|clean:temiz:🧼|dirty:kirli:🧹|quiet:sessiz:🤫
loud:gürültülü:📢|cookie:kurabiye:🍪|candy:şeker:🍬|pasta:makarna:🍝|salad:salata:🥗|cherry:kiraz:🍒|melon:kavun:🍈|peach:şeftali:🍑
potato:patates:🥔|tomato:domates:🍅|onion:soğan:🧅|butter:tereyağı:🧈|salt:tuz:🧂|spoon:kaşık:🥄|fork:çatal:🍴|plate:tabak:🍽️
glass:bardak:🥛|soap:sabun:🧼|brush:fırça:🪥|mirror:ayna:🪞|pillow:yastık:🛏️|watch:kol saati:⌚|tablet:tablet:📱|screen:ekran:🖥️
button:düğme:🔘|level:seviye:🆙|bread:ekmek:🍞|uncle:amca / dayı:👨|aunt:teyze / hala:👩|cousin:kuzen:🧒|garden:bahçe:🌳|street:sokak:🏘️
'''),
 dict(n=3, name='Player', tr='Oyuncu', sub='2. sınıf · fiiller, sıfatlar, futbol ve araba kelimeleri (5–8 harf)', words='''
referee:hakem:🧑‍⚖️|whistle:düdük:📯|corner:korner:🚩|penalty:penaltı:⚽|striker:forvet:⚽|defender:defans oyuncusu:🛡️|captain:kaptan:©️|trophy:kupa / ödül:🏆
medal:madalya:🏅|engine:motor:⚙️|helmet:kask:⛑️|traffic:trafik:🚦|bridge:köprü:🌉|tunnel:tünel:🚇|station:istasyon:🚉|airport:havalimanı:🛫
island:ada:🏝️|forest:orman:🌲|mountain:dağ:⛰️|river:nehir:🏞️|beach:plaj:🏖️|desert:çöl:🏜️|ocean:okyanus:🌊|planet:gezegen:🪐
dragon:ejderha:🐉|octopus:ahtapot:🐙|dolphin:yunus:🐬|shark:köpekbalığı:🦈|whale:balina:🐳|parrot:papağan:🦜|camel:deve:🐫|puppy:yavru köpek:🐶
kitten:yavru kedi:🐱|controller:oyun kolu:🎮|joystick:joystick:🕹️|practice:antrenman:🏋️|swim:yüzmek:🏊|ride:binmek:🚲|drive:araba sürmek:🚗|push:itmek:👐
pull:çekmek:🪢|carry:taşımak:🎒|build:inşa etmek:🏗️|draw:çizmek:✏️|read:okumak:📖|sing:şarkı söylemek:🎤|listen:dinlemek:👂|speak:konuşmak:🗣️
think:düşünmek:🤔|help:yardım etmek:🤝|share:paylaşmak:🤲|wait:beklemek:⏳|hurry:acele etmek:🏃|finish:bitirmek:🏁|start:başlamak:▶️|quick:çabuk:⚡
heavy:ağır:🏋️|light:hafif:🪶|empty:boş:🫙|full:dolu:🍽️|round:yuvarlak:⚪|square:kare:🟦|circle:daire:⭕|triangle:üçgen:🔺
Monday:pazartesi|Tuesday:salı|Wednesday:çarşamba|Thursday:perşembe|Friday:cuma
'''),
 dict(n=4, name='Champion', tr='Şampiyon', sub='2.–3. sınıf · iki kelimelik ifadeler ve kısa cümleler', words='''
seat belt:emniyet kemeri:🚗|traffic light:trafik ışığı:🚦|police car:polis arabası:🚓|fire truck:itfaiye aracı:🚒|free kick:serbest vuruş:⚽|corner kick:korner atışı:🚩|game over:oyun bitti:🎮|next level:sonraki seviye:🆙
press start:başlata bas:▶️|high score:en yüksek skor:🏆|best friend:en iyi arkadaş:🤝|ice cream:dondurma:🍦|hot dog:sosisli sandviç:🌭|swimming pool:yüzme havuzu:🏊|summer holiday:yaz tatili:🏖️|race car:yarış arabası:🏎️
football match:futbol maçı:🏟️|golden cup:altın kupa:🏆|bus stop:otobüs durağı:🚏|birthday cake:doğum günü pastası:🎂|good night:iyi geceler:🌙|see you soon:yakında görüşürüz:👋|well played:iyi oynadın:👏|my turn:sıra bende:🙋
I scored a goal!:Gol attım!:⚽|Can I play, please?:Oynayabilir miyim lütfen?:🙋|Let's go to the park.:Hadi parka gidelim.:🛝|My favourite colour is blue.:En sevdiğim renk mavi.:🔵|I am faster than you!:Senden daha hızlıyım!:🏃|The referee blows the whistle.:Hakem düdüğü çalar.:📯|Put on your seat belt.:Emniyet kemerini tak.:🚗|Press start to play.:Oynamak için başlata bas.:▶️
We are the champions!:Biz şampiyonuz!:🏆|I can ride a bike.:Bisiklete binebilirim.:🚲|What time is it?:Saat kaç?:⏰|It is my turn.:Sıra bende.:🙋|Good night, Mum.:İyi geceler anne.:🌙|The car is very fast.:Araba çok hızlı.:🏎️|I like to play games.:Oyun oynamayı severim.:🎮|Pass the ball, please.:Topu pas ver lütfen.:⚽
'''),
]

def parse(block):
    out = []
    for item in re.split(r'[|\n]', block):
        item = item.strip()
        if not item:
            continue
        parts = item.split(':')
        out.append(dict(en=parts[0], tr=parts[1], e=parts[2] if len(parts) > 2 else ''))
    return out

def existing_words(src):
    words = set(w.lower() for w in re.findall(r"W\('([^']+)'", src))
    m = re.search(r"const TOWER_EXTRA=TX\((.*?)\);\n", src, re.S)
    if m:
        tx = re.sub(r"'\s*\+\s*'", '', m.group(1)).strip().strip("'")
        words |= set(x.split(':')[0].lower() for x in tx.split('|') if x)
    m = re.search(r"const TYPE_POOLS=\[(.*?)\n\];", src, re.S)
    if m:
        words |= set(w.lower() for w in re.findall(r"'([^']+)'", m.group(1)))
    return words

def main():
    src = SITE.read_text(encoding='utf-8')
    have = existing_words(src)
    seen = set()
    levels = []
    dropped = []
    for L in LEVELS:
        kept = []
        for w in parse(L['words']):
            k = w['en'].lower()
            if k in have or k in seen:
                dropped.append(w['en'])
                continue
            seen.add(k)
            kept.append(w)
        levels.append(dict(n=L['n'], name=L['name'], tr=L['tr'], sub=L['sub'], words=kept))

    # 1) JS block for the site
    js_levels = []
    for L in levels:
        packed = '|'.join(':'.join([w['en'], w['tr']] + ([w['e']] if w['e'] else [])) for w in L['words'])
        js_levels.append("{n:%d,name:%s,tr:%s,sub:%s,words:TX(%s)}" % (
            L['n'], json.dumps(L['name'], ensure_ascii=False), json.dumps(L['tr'], ensure_ascii=False),
            json.dumps(L['sub'], ensure_ascii=False), json.dumps(packed, ensure_ascii=False)))
    block = ("/* VOCAB:BEGIN (generated by vocab.py - edit the list there, then run it) */\n"
             "const VOCAB_LEVELS=[\n " + ",\n ".join(js_levels) + "\n];\n"
             "/* VOCAB:END */")
    if '/* VOCAB:BEGIN' not in src:
        sys.exit('VOCAB markers not found in uras-english-cup.html')
    src = re.sub(r"/\* VOCAB:BEGIN.*?/\* VOCAB:END \*/", lambda _: block, src, flags=re.S)
    SITE.write_text(src, encoding='utf-8', newline='\n')

    # 2) printable word list (+ the 12 weekly units already on the site)
    weeks = re.findall(r"\{n:(\d+),lv:\d,tr:'([^']*)',en:'([^']*)'", src)
    rows = []
    for L in levels:
        cells = ''.join(
            f"<div class='row'><span class='e'>{html.escape(w['e'])}</span><span class='en'>{html.escape(w['en'])}</span>"
            f"<span class='tr'>{html.escape(w['tr'])}</span><span class='ck'></span></div>" for w in L['words'])
        rows.append(f"<section class='lvl'><h2>Level {L['n']} · {html.escape(L['name'])} "
                    f"<span>({html.escape(L['tr'])})</span></h2><p class='sub'>{html.escape(L['sub'])} · "
                    f"{len(L['words'])} kelime · öğrendiğin kelimenin kutusuna ✓ koy</p><div class='cols'>{cells}</div></section>")
    total = sum(len(L['words']) for L in levels)
    week_list = ''.join(f"<li><b>Week {n}</b> · {html.escape(en)} <span>({html.escape(tr)})</span></li>" for n, tr, en in weeks)
    page = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><title>Uras English Cup · Kelime Listesi</title>
<style>
@page {{ size: A4; margin: 14mm 12mm; }}
* {{ box-sizing: border-box }}
body {{ font-family: "Segoe UI", Arial, sans-serif; color: #132029; margin: 0; font-size: 11pt }}
header {{ background: #140a2e; color: #fff; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; border-bottom: 4px solid #ff2e88 }}
header h1 {{ margin: 0; font-size: 22pt; color: #ffc93c }}
header p {{ margin: 4px 0 0; color: #e9d5ff }}
.how {{ border: 2px dashed #22d3ee; border-radius: 10px; padding: 8px 12px; margin-bottom: 10px; font-size: 10pt }}
.how ul {{ margin: 4px 0 0 18px; padding: 0 }}
.lvl {{ break-before: page }}
.lvl:first-of-type {{ break-before: auto }}
h2 {{ font-size: 16pt; margin: 6px 0 2px; color: #7a1f7a }}
h2 span {{ color: #55665c; font-size: 12pt; font-weight: 600 }}
.sub {{ margin: 0 0 6px; color: #55665c }}
.cols {{ columns: 2; column-gap: 18px; border-top: 2px solid #132029; padding-top: 4px }}
.row {{ display: flex; align-items: center; gap: 8px; padding: 3px 4px; border-bottom: 1px solid #e2e8f0; break-inside: avoid }}
.row .e {{ width: 20px; flex: none; font-size: 11pt; text-align: center; font-family: "Segoe UI Emoji", "Segoe UI", sans-serif }}
.row .en {{ font-weight: 700; font-size: 11.5pt }}
.row .tr {{ flex: 1; color: #334155; font-size: 10pt }}
.row .ck {{ width: 13px; height: 13px; flex: none; border: 1.5px solid #94a3b8; border-radius: 3px }}
.weeks {{ break-before: page }}
.weeks ul {{ columns: 2; padding-left: 18px }}
.weeks span {{ color: #55665c }}
footer {{ margin-top: 10px; font-size: 9pt; color: #64748b }}
</style></head><body>
<header><h1>Uras English Cup · Kelime Listesi</h1><p>Yeni kelime bankası: {total} kelime ve ifade, 4 seviye · ozgencilimge-prog.github.io/UrasWebSite</p></header>
<div class="how"><b>Nasıl kullanılır?</b><ul>
<li>Her gün aynı seviyeden 5 kelime seçin. Önce sesli okuyun, sonra Uras tekrar etsin.</li>
<li>Kelimeyi bilince sağdaki kutuya ✓ koyun. Bir seviye bitince bir sonrakine geçin.</li>
<li>Sitede <b>Word Bank</b> bölümünde bu kelimelere dokunup dinleyebilirsiniz; Typing Turbo ve Word Tower da bu kelimeleri kullanır.</li></ul></div>
{''.join(rows)}
<section class="weeks"><h2>Sitedeki 12 haftalık konu</h2><p class="sub">Bu kelimeler haftalık görevlerde zaten var; listede tekrar edilmedi.</p><ul>{week_list}</ul></section>
<footer>Kelimeler 1.–2. sınıf düzeyine ve Uras'ın ilgi alanlarına (futbol, arabalar, oyunlar) göre seçildi.</footer>
</body></html>"""
    (HERE / 'kelime-listesi.html').write_text(page, encoding='utf-8')
    print(f"levels: {[len(L['words']) for L in levels]} | total new: {total} | skipped (already on site): {len(dropped)} -> {', '.join(dropped)}")

if __name__ == '__main__':
    main()
