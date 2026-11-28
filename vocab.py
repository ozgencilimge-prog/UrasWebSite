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
 dict(n=1, name='Starter', tr='Başlangıç', sub='1. sınıf · kısa ve somut kelimeler, temel fiiller (3–5 harf)', words='''
ant:karınca:🐜|hen:tavuk:🐔|goat:keçi:🐐|lamb:kuzu:🐑|van:minibüs:🚐|jet:jet uçağı:✈️|cap:kep / şapka:🧢|mug:kupa bardak:☕
pot:tencere:🍲|cheese:peynir:🧀|nut:fıstık / kuruyemiş:🥜|pie:turta:🥧|tea:çay:🍵|zoo:hayvanat bahçesi:🦁|mum:anne:👩|dad:baba:👨
lip:dudak:👄|toe:ayak parmağı:🦶|hug:sarılmak:🤗|sit:oturmak:🪑|eat:yemek yemek:🍽️|see:görmek:👀|new:yeni:🆕|old:eski / yaşlı:👴
wet:ıslak:💦|dry:kuru:☀️|fun:eğlence:🎉|net:file:🥅|fan:taraftar:📣|hop:sekmek:🐇|tap:dokunmak:👆|hill:tepe:⛰️
lake:göl:🏞️|park:park:🛝|road:yol:🛣️|tyre:lastik:🛞|seat:koltuk:💺|kite:uçurtma:🪁|lamp:lamba:💡|wall:duvar:🧱
roof:çatı:🏠|tent:çadır:⛺|rice:pirinç:🍚|soup:çorba:🍲|corn:mısır:🌽|pear:armut:🍐|kiwi:kivi:🥝|knee:diz:🦵
neck:boyun|hair:saç:💇|face:yüz:🙂|snail:salyangoz:🐌|ring:yüzük:💍|bell:zil:🔔|gift:hediye:🎁|doll:oyuncak bebek:🪆
bubble:baloncuk:🫧|bone:kemik:🦴|flower:çiçek:🌻
drum:davul:🥁|race:yarış:🏁|taxi:taksi:🚕|fast:hızlı:💨|gold:altın:🥇|shop:dükkan:🏪|farm:çiftlik:🚜|nest:yuva:🪺
'''),
 dict(n=2, name='Explorer', tr='Kaşif', sub='1.–2. sınıf · günlük hayat, duygular, zaman ve yer (4–7 harf)', words='''
jersey:forma:👕|coach:antrenör:📋|match:maç:⚽|football boots:krampon:👟|wheel:tekerlek:🛞|brake:fren:🛑|driver:sürücü:🚙|petrol:benzin:⛽
scooter:scooter:🛴|tractor:traktör:🚜|puzzle:yapboz:🧩|guitar:gitar:🎸|piano:piyano:🎹|paper:kağıt:📄|glue:yapıştırıcı:🧴|sponge:sünger:🧽
lesson:ders:📚|class:sınıf:🏫|laugh:gülmek:😂|cry:ağlamak:😢|angry:kızgın:😠|tired:yorgun:🥱|hungry:aç:🍽️|thirsty:susamış:🥤
scared:korkmuş:😨|brave:cesur:🦸|strong:güçlü:💪|tall:uzun boylu:🦒|short:kısa:📏|clean:temiz:🧼|broom:süpürge:🧹|quiet:sessiz:🤫
loud:gürültülü:📢|biscuit:bisküvi:🍪|sweets:şeker:🍬|pasta:makarna:🍝|salad:salata:🥗|cherry:kiraz:🍒|melon:kavun:🍈|peach:şeftali:🍑
potato:patates:🥔|tomato:domates:🍅|onion:soğan:🧅|butter:tereyağı:🧈|salt:tuz:🧂|spoon:kaşık:🥄|fork:çatal:🍴|plate:tabak:🍽️
glass:bardak:🥛|soap:sabun:🧼|brush:fırça:🪥|mirror:ayna:🪞|basket:sepet:🧺|watch:kol saati:⌚|tablet:tablet:📱|screen:ekran:🖥️
button:düğme:🔘|level:seviye:🆙|bread:ekmek:🍞|uncle:amca / dayı:👨|aunt:teyze / hala:👩|cousin:kuzen:🧒|garden:bahçe:🏡|street:sokak:🏘️
'''),
 dict(n=3, name='Player', tr='Oyuncu', sub='2. sınıf · fiiller, sıfatlar, aylar, futbol ve araba kelimeleri (5–10 harf)', words='''
referee:hakem:🟨|stadium:stadyum:🏟️|corner:korner:🚩|penalty:penaltı:⚽|striker:forvet:⚽|defender:defans oyuncusu:🛡️|captain:kaptan:🧑‍✈️|trophy:kupa / ödül:🏆
medal:madalya:🏅|engine:motor:⚙️|helmet:kask:⛑️|traffic:trafik:🚦|bridge:köprü:🌉|tunnel:tünel:🚇|station:istasyon:🚉|airport:havalimanı:🛫
island:ada:🏝️|forest:orman:🌲|mountain:dağ:⛰️|river:nehir:🏞️|beach:plaj:🏖️|desert:çöl:🏜️|ocean:okyanus:🌊|planet:gezegen:🪐
dragon:ejderha:🐉|octopus:ahtapot:🐙|dolphin:yunus:🐬|shark:köpekbalığı:🦈|whale:balina:🐳|parrot:papağan:🦜|camel:deve:🐫|puppy:yavru köpek:🐶
kitten:yavru kedi:🐱|controller:oyun kolu:🎮|joystick:joystick:🕹️|practice:antrenman:🏋️|swim:yüzmek:🏊|ride:binmek:🚲|drive:araba sürmek:🚗|push:itmek:👐
pull:çekmek:🪢|carry:taşımak:🎒|build:inşa etmek:🏗️|draw:çizmek:✏️|read:okumak:📖|sing:şarkı söylemek:🎤|listen:dinlemek:👂|speak:konuşmak:🗣️
think:düşünmek:🤔|help:yardım etmek:🤝|share:paylaşmak:🤲|wait:beklemek:⏳|hurry:acele etmek:🏃|finish:bitirmek:🏁|start:başlamak:▶️|quick:çabuk:⚡
heavy:ağır:🏋️|light:hafif:🪶|empty:boş:🫙|full:dolu:🔋|round:yuvarlak:🌕|square:kare:🟦|circle:daire:⭕|triangle:üçgen:🔺
Monday:pazartesi|Tuesday:salı|Wednesday:çarşamba|Thursday:perşembe|Friday:cuma
'''),
 dict(n=4, name='Champion', tr='Şampiyon', sub='2.–3. sınıf · iki kelimelik ifadeler ve kısa cümleler', words='''
seat belt:emniyet kemeri:🚗|traffic light:trafik ışığı:🚦|police car:polis arabası:🚓|fire truck:itfaiye aracı:🚒|free kick:serbest vuruş:⚽|corner kick:korner atışı:🚩|game over:oyun bitti:🎮|next level:sonraki seviye:🆙
press start:başlata bas:▶️|high score:en yüksek skor:🏆|best friend:en iyi arkadaş:🤝|ice cream:dondurma:🍦|hot dog:sosisli sandviç:🌭|swimming pool:yüzme havuzu:🏊|summer holiday:yaz tatili:🏖️|racing car:yarış arabası:🏎️
football match:futbol maçı:🏟️|golden cup:altın kupa:🏆|bus stop:otobüs durağı:🚏|birthday cake:doğum günü pastası:🎂|good night:iyi geceler:🌙|see you soon:yakında görüşürüz:👋|well played:iyi oynadın:👏|my turn:sıra bende:🙋
I scored a goal!:Gol attım!:⚽|Can I play, please?:Oynayabilir miyim lütfen?:🙋|Let's go to the park.:Hadi parka gidelim.:🛝|My favourite colour is blue.:En sevdiğim renk mavi.:🔵|I am faster than you!:Senden daha hızlıyım!:🏃|The referee blows the whistle.:Hakem düdüğü çalar.:🏟️|Put on your seat belt.:Emniyet kemerini tak.:🚗|Press start to play.:Oynamak için başlata bas.:▶️
We are the champions!:Biz şampiyonuz!:🏆|I can ride a bike.:Bisiklete binebilirim.:🚲|What time is it?:Saat kaç?:⏰|It is my turn.:Sıra bende.:🙋|Good night, Mum.:İyi geceler anne.:🌙|The car is very fast.:Araba çok hızlı.:🏎️|I like to play games.:Oyun oynamayı severim.:🎮|Pass the ball, please.:Topu pas ver lütfen.:⚽
'''),
]

# Extra words picked by hand from "english words/1-A1 A1 Beginner.pdf".
# That PDF is the 1000 most frequent dwyl words, so it also has adult, violent and swear words;
# only concrete, everyday words that suit a 7-year-old are taken. Added to the Word Bank level shown.
A1_ADD = {
 1: '''
air:hava:🌬️|art:sanat:🎨|card:kart:🃏|city:şehir:🏙️|day:gün:☀️|fire:ateş:🔥|food:yiyecek:🍔|kids:çocuklar:🧒
man:adam:👨|leaf:yaprak:🍃|name:isim:📛|news:haber:📰|night:gece:🌙|page:sayfa:📄|rock:kaya:🪨|room:oda:🛋️
son:oğul:👦|song:şarkı:🎵|time:zaman:⏰|town:kasaba:🏘️|TV:televizyon:📺|week:hafta:📅|word:kelime:🔤|year:yıl:🗓️
hour:saat (60 dakika):⏱️|bank:banka:🏦|club:kulüp:⚽|cool:havalı:😎|dark:karanlık:🌑|easy:kolay:👌|hard:zor:🧱|nice:güzel / hoş:😊
good:iyi:👍|bad:kötü:👎|love:sevmek:❤️|like:hoşlanmak:😍|play:oynamak:🤹|walk:yürümek:🚶|talk:konuşmak:💬|call:aramak:📞
come:gelmek:👋|give:vermek:🎁|take:almak:🫴|make:yapmak:🛠️|buy:satın almak:🛒|pay:ödemek:💳|robot:robot:🤖|cut:kesmek:✂️
add:eklemek:➕|open:açmak:📂|shell:deniz kabuğu:🐚|send:göndermek:📤|find:bulmak:🔍|ask:sormak:❓|want:istemek:🙏|need:ihtiyaç duymak:🆘
try:denemek:💪|web:örümcek ağı:🕸️|end:son:🔚|half:yarım:🌓|side:yan / taraf:↔️
''',
 2: '''
answer:cevap:💬|learn:öğrenmek:📚|know:bilmek:🧠|feel:hissetmek:🤗|hear:duymak:👂|look:bakmak:👀|move:hareket etmek:🏃|turn:dönmek:🔄
show:göstermek:👉|lose:kaybetmek:😞|film:film:🎬|video:video:📹|radio:radyo:📻|heart:kalp:❤️|earth:dünya / yeryüzü:🌍|space:uzay:🚀
ground:zemin / yer:🟫|sound:ses:🔊|voice:insan sesi:🗣️|story:hikaye:📖|idea:fikir:💡|party:parti:🎉|price:fiyat:🏷️|ladder:merdiven:🪜
police:polis:👮|child:çocuk:🧒|woman:kadın:👩|parents:anne baba:👨‍👩‍👦|young:genç:🧑|little:küçük:🤏|huge:kocaman:🐘|funny:komik:😂
crazy:çılgın:🤪|amazing:harika:🤩|super:süper:🦸|ready:hazır:✅|sure:emin:👍|safe:güvenli:🦺|free:serbest / bedava:🆓|true:doğru:✔️
wrong:yanlış:❌|first:birinci:🥇|second:ikinci:🥈|third:üçüncü:🥉|early:erken:🌅|late:geç:🌙|today:bugün:📅|tonight:bu gece:🌃
soon:yakında:⏳|again:tekrar:🔁|always:her zaman:♾️|never:asla:🚫|near:yakın:📍|far:uzak:🏔️|inside:içeride:🏠|outside:dışarıda:🌳
in:içinde|on:üstünde|under:altında|above:yukarısında:⬆️|below:aşağısında:⬇️|behind:arkasında:🔙|next to:yanında:👫
''',
 3: '''
January:ocak:❄️|February:şubat:❄️|March:mart:🌱|April:nisan:🌷|May:mayıs:🌸|June:haziran:☀️|July:temmuz:🏖️|August:ağustos:🍉
September:eylül:🍂|October:ekim:🎃|November:kasım:🍁|December:aralık:🎄
season:mevsim / sezon:🌦️|league:lig:🏆|volcano:yanardağ:🌋|track:pist:🛤️|training:antrenman:🏋️|history:tarih:📜|science:bilim:🔬|language:dil:🗣️
English:İngilizce:🇬🇧|internet:internet:🌐|online:çevrim içi:💻|student:öğrenci:🧑‍🎓|question:soru:❓|problem:sorun:🧩|example:örnek:💡|number:sayı:🔢
important:önemli:⭐|different:farklı:🔀|difficult:zor:🧗|perfect:mükemmel:💯|popular:popüler:🌟|together:birlikte:🤝|everyone:herkes:👨‍👩‍👧‍👦|everything:her şey:🌈
something:bir şey:❓|remember:hatırlamak:🧠|understand:anlamak:💡|believe:inanmak:🙏|happen:olmak / gerçekleşmek:⚡|visit:ziyaret etmek:🏠|enjoy:keyfini çıkarmak:😄|follow:takip etmek:👣
forget:unutmak:🤷|please:lütfen:🙏|sorry:özür dilerim:😔|thanks:teşekkürler:💐|okay:tamam:👌|hey:hey:👋
''',
}

# More Level 4 (Champion) phrases and short sentences, so every level has 12 packs of 10.
CHAMPION_ADD = '''
goal kick:kale vuruşu:🥅|penalty kick:penaltı vuruşu:⚽|kick-off:başlama vuruşu:⚽|half time:devre arası:⏱️|full time:maç sonu:🏁|extra time:uzatma:⏰|team captain:takım kaptanı:🧑‍✈️|home team:ev sahibi takım:🏠
away team:deplasman takımı:🚌|score a goal:gol at:⚽|save the ball:topu kurtar:🧤|throw-in:taç atışı:🙌|golden boot:altın ayakkabı:👟|player of the match:maçın oyuncusu:🌟|race track:yarış pisti:🏁|pit stop:pit stop:🔧
car wash:araba yıkama:🧽|petrol station:benzin istasyonu:⛽|car park:otopark:🅿️|speed limit:hız sınırı:🚦|sports car:spor araba:🏎️|school bus:okul otobüsü:🚌|fire station:itfaiye istasyonu:🚒|police station:karakol:🚓
video game:video oyunu:🎮|new game:yeni oyun:🆕|save game:oyunu kaydet:💾|level up:seviye atla:🆙|bonus level:bonus seviye:⭐|extra life:ekstra can:❤️|power up:güçlendirme:⚡|start button:başlat düğmesi:▶️
pause button:durdur düğmesi:⏸️|good luck:iyi şanslar:🍀|happy new year:mutlu yıllar:🎆|thank you very much:çok teşekkürler:🙏|excuse me:afedersiniz:🙋|I'm sorry:özür dilerim:😔|no problem:sorun değil:👌|come on:hadi:💪
let's go:hadi gidelim:🚀|watch out:dikkat et:⚠️|be careful:dikkatli ol:⚠️|hurry up:acele et:⏩|slow down:yavaşla:🐢|sit down:otur:🪑|stand up:ayağa kalk:🧍|line up:sıraya gir:🚶|clean up:topla / temizle:🧹
I scored two goals.:İki gol attım.:⚽|My team won the match.:Takımım maçı kazandı.:🏆|The goalkeeper saved the ball.:Kaleci topu kurtardı.:🧤|The referee shows a yellow card.:Hakem sarı kart gösteriyor.:🟨
We play football after school.:Okuldan sonra futbol oynarız.:⚽|My favourite team is red and white.:En sevdiğim takım kırmızı beyaz.:🔴|The race car is very fast.:Yarış arabası çok hızlı.:🏎️|Dad washes the car.:Babam arabayı yıkar.:🧽
We stop at the red light.:Kırmızı ışıkta dururuz.:🚦|The bus is full of children.:Otobüs çocuklarla dolu.:🚌|I want to be a racing driver.:Yarış pilotu olmak istiyorum.:🏁|Can I play a video game?:Video oyunu oynayabilir miyim?:🎮
I am on level ten!:Onuncu seviyedeyim!:🆙|Press the button to jump.:Zıplamak için düğmeye bas.:🔘|I won the game!:Oyunu kazandım!:🏆|Let's play together.:Hadi birlikte oynayalım.:🤝|It is my birthday today.:Bugün benim doğum günüm.:🎂
I have a new red ball.:Yeni kırmızı bir topum var.:⚽|My sister likes to read.:Ablam okumayı sever.:📖|My dad is a good cook.:Babam iyi yemek yapar.:🍳|I brush my teeth every morning.:Her sabah dişlerimi fırçalarım.:🪥
I go to bed at nine.:Saat dokuzda yatarım.:🛏️|It is time for school.:Okul zamanı.:🏫|Open your English book.:İngilizce kitabını aç.:📘|Listen and repeat.:Dinle ve tekrar et.:👂|Raise your hand, please.:Lütfen elini kaldır.:✋
Can I go to the toilet?:Tuvalete gidebilir miyim?:🚻|I am hungry. Let's eat!:Acıktım. Hadi yiyelim!:🍽️|I like pizza and juice.:Pizza ve meyve suyu severim.:🍕|The cat is on the sofa.:Kedi kanepenin üstünde.:🐱|The dog is under the bed.:Köpek yatağın altında.:🐶
Look at the big plane!:Şu büyük uçağa bak!:✈️|The sun is hot today.:Bugün güneş sıcak.:☀️|Put on your hat and coat.:Şapkanı ve montunu giy.:🧥|How are you today?:Bugün nasılsın?:🙂|I am fine, thank you.:İyiyim, teşekkür ederim.:👍
What is your favourite colour?:En sevdiğin renk ne?:🎨|How old is your sister?:Ablan kaç yaşında?:👧|Where do you live?:Nerede yaşıyorsun?:🏠|I live in a big city.:Büyük bir şehirde yaşıyorum.:🏙️|Kaan has a blue bike.:Kaan’ın mavi bir bisikleti var.:🚲
The train goes very fast.:Tren çok hızlı gider.:🚂|I can count to twenty.:Yirmiye kadar sayabilirim.:🔢|Monday is my football day.:Pazartesi benim futbol günüm.:📅|We have English on Friday.:Cuma günü İngilizce dersimiz var.:📘|I love my family very much.:Ailemi çok seviyorum.:❤️
The game starts at five.:Maç beşte başlıyor.:⏰|Kick the ball into the goal!:Topu kaleye vur!:🥅|Run fast and catch the ball!:Hızlı koş ve topu yakala!:🏃|Good game, everyone!:Herkese iyi oyunlar!:👏
'''
LEVEL_SIZE = 120   # 12 packs of 10 words in every Word Quest level

def parse(block):
    out = []
    for item in re.split(r'[|\n]', block):
        item = item.strip()
        if not item:
            continue
        parts = item.split(':')
        out.append(dict(en=parts[0], tr=parts[1], e=parts[2] if len(parts) > 2 else ''))
    return out

# Turkish for game words that appear only in Typing Turbo (no translation stored on the site)
EXTRA_TR = {
 'goal': 'gol / kale', 'red car': 'kırmızı araba', 'big ball': 'büyük top', 'blue bus': 'mavi otobüs', 'my dog': 'benim köpeğim',
 'go left': 'sola git', 'run fast': 'hızlı koş', 'green apple': 'yeşil elma', 'two goals': 'iki gol', 'hello Uras': 'merhaba Uras',
 'I like cars.': 'Arabaları severim.', 'Kick the ball!': 'Topa vur!', 'I am seven.': 'Yedi yaşındayım.', 'My car is red.': 'Arabam kırmızı.',
 'Hello, I am Uras.': 'Merhaba, ben Uras.', 'Ready, set, go!': 'Yerlerinize, hazır, başla!', 'I can jump.': 'Zıplayabilirim.', 'Open the door.': 'Kapıyı aç.', 'hello Defne': 'merhaba Defne', 'hi Kuzey': 'selam Kuzey', 'run Aras': 'koş Aras', 'Kuzey is my friend.': 'Kuzey benim arkadaşım.', 'Pass the ball, Aras!': 'Topu pas ver Aras!', 'Hello, Dora!': 'Merhaba Dora!', 'Defne likes cats.': 'Defne kedileri sever.', 'Asel has a pen.': 'Asel’in bir kalemi var.',
}
EXTRA_EMOJI = {'goal': '🥅', 'red car': '🚗', 'big ball': '⚽', 'blue bus': '🚌', 'my dog': '🐶', 'go left': '⬅️', 'run fast': '🏃', 'green apple': '🍏',
 'two goals': '⚽', 'hello Uras': '👋', 'I like cars.': '🏎️', 'Kick the ball!': '🦵', 'I am seven.': '7️⃣', 'My car is red.': '🚗',
 'Hello, I am Uras.': '👋', 'Ready, set, go!': '🏁', 'I can jump.': '🦘', 'Open the door.': '🚪'}

COLOR_EMOJI = {'red': '🔴', 'blue': '🔵', 'green': '🟢', 'yellow': '🟡', 'black': '⚫', 'white': '⚪', 'orange': '🟠', 'pink': '🩷', 'purple': '🟣', 'brown': '🟤', 'grey': '⚪'}
DPAD_EMOJI = {'up': '⬆️', 'down': '⬇️', 'left': '⬅️', 'right': '➡️'}
KEYCAP = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

def unq(s):
    return s[1:-1].replace("\\'", "'")

def parse_weeks(src):
    block = src[src.index('const WEEKS=['):src.index('const NW=')]
    weeks = []
    for ch in re.split(r"\n \{n:", block)[1:]:
        h = re.match(r"(\d+),lv:(\d),tr:'([^']*)',en:'([^']*)',src:'([^']*)',chunk:(\"[^\"]*\"|'[^']*'),chunkTr:'([^']*)'", ch)
        wk = dict(n=int(h.group(1)), lv=int(h.group(2)), tr=h.group(3), en=h.group(4), chunk=unq(h.group(6)), chunkTr=h.group(7), words=[])
        for en, tr, p, ex in re.findall(r"W\('([^']*)','([^']*)',(\{[^}]*\}|'[^']*'),(\"[^\"]*\"|'(?:[^'\\]|\\.)*')\)", ch):
            if p.startswith("'"):
                e = unq(p)
            elif "e:'" in p:
                e = re.search(r"e:'([^']*)'", p).group(1)
            elif 'car' in p:
                e = COLOR_EMOJI.get(en, '🚗')
            elif 'dpad' in p:
                e = DPAD_EMOJI.get(en, '🎮')
            else:
                e = ''
            wk['words'].append(dict(en=en, tr=tr, e=e, ex=unq(ex)))
        for i, (en, tr, ex) in enumerate(re.findall(r"\['(\w+)','([^']*)',(\"[^\"]*\"|'[^']*')\]", ch)):
            wk['words'].append(dict(en=en, tr=tr, e=KEYCAP[i] if i < 10 else '', ex=unq(ex)))
        weeks.append(wk)
    return weeks

def parse_tower(src):
    m = re.search(r"const TOWER_EXTRA=TX\((.*?)\);\n", src, re.S)
    tx = re.sub(r"'\s*\+\s*'", '', m.group(1)).strip().strip("'")
    out = []
    for x in tx.split('|'):
        if x:
            p = x.split(':')
            out.append(dict(en=p[0], tr=p[1] if len(p) > 1 else '', e=p[2] if len(p) > 2 else ''))
    return out

def parse_typing(src):
    m = re.search(r"const TYPE_POOLS=\[(.*?)\n\];", src, re.S)
    return re.findall(r"'([^']+)'", m.group(1))

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
        for w in parse(L['words'] + '\n' + A1_ADD.get(L['n'], '') + '\n' + (CHAMPION_ADD if L['n'] == 4 else '')):
            k = w['en'].lower()
            if k in have or k in seen:
                dropped.append(w['en'])
                continue
            seen.add(k)
            kept.append(w)
        levels.append(dict(n=L['n'], name=L['name'], tr=L['tr'], sub=L['sub'], words=kept))

    # Balance: every level gets exactly LEVEL_SIZE words; extra words move up to the next level
    for i in range(len(levels) - 1):
        if len(levels[i]['words']) > LEVEL_SIZE:
            extra = levels[i]['words'][LEVEL_SIZE:]
            levels[i]['words'] = levels[i]['words'][:LEVEL_SIZE]
            levels[i + 1]['words'] = extra + levels[i + 1]['words']
    short = [L['n'] for L in levels if len(L['words']) < LEVEL_SIZE]
    if short:
        print('WARNING: levels with fewer than', LEVEL_SIZE, 'words:', short)
    levels[-1]['words'] = levels[-1]['words'][:LEVEL_SIZE]

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

    # 2) printable list of EVERY word the site uses, in three parts
    weeks = parse_weeks(src)
    tower = parse_tower(src)
    typing = parse_typing(src)
    tr_of, e_of = {}, {}
    for wk in weeks:
        for w in wk['words']:
            tr_of.setdefault(w['en'].lower(), w['tr']); e_of.setdefault(w['en'].lower(), w['e'])
    for L in levels:
        for w in L['words']:
            tr_of.setdefault(w['en'].lower(), w['tr']); e_of.setdefault(w['en'].lower(), w['e'])
    for w in tower:
        tr_of.setdefault(w['en'].lower(), w['tr']); e_of.setdefault(w['en'].lower(), w['e'])
    for k, v in EXTRA_TR.items():
        tr_of.setdefault(k.lower(), v)
    for k, v in EXTRA_EMOJI.items():
        if not e_of.get(k.lower()):
            e_of[k.lower()] = v

    taken = set(w['en'].lower() for wk in weeks for w in wk['words']) | set(w['en'].lower() for L in levels for w in L['words'])
    others, seen_o = [], set()
    for en in [w['en'] for w in tower] + typing:
        k = en.lower()
        if k in taken or k in seen_o:
            continue
        seen_o.add(k)
        others.append(dict(en=en, tr=tr_of.get(k, ''), e=e_of.get(k, '')))
    missing = [w['en'] for w in others if not w['tr']]
    groups = [
        ('Kısa kelimeler', '3–4 harf', [w for w in others if ' ' not in w['en'] and len(w['en']) <= 4]),
        ('Orta kelimeler', '5–6 harf', [w for w in others if ' ' not in w['en'] and 5 <= len(w['en']) <= 6]),
        ('Uzun kelimeler', '7+ harf', [w for w in others if ' ' not in w['en'] and len(w['en']) >= 7]),
        ('İkili ifadeler', 'iki kelime', [w for w in others if ' ' in w['en'] and not re.search(r'[.?!]$', w['en'])]),
        ('Cümleler', 'tam cümle', [w for w in others if re.search(r'[.?!]$', w['en'])]),
    ]

    def row(w, ex=''):
        exh = f"<small class='ex'>{html.escape(ex)}</small>" if ex else ''
        return (f"<div class='row'><span class='e'>{html.escape(w['e'])}</span><span class='w'><b>{html.escape(w['en'])}</b> "
                f"<span class='tr'>{html.escape(w['tr'])}</span>{exh}</span><span class='ck'></span></div>")

    part1 = ''.join(
        f"<div class='wk'><h3>Week {wk['n']} · {html.escape(wk['en'])} <span>({html.escape(wk['tr'])})</span> "
        f"<em>Level {wk['lv']}</em></h3><p class='chunk'>🗣️ {html.escape(wk['chunk'])} <span>· {html.escape(wk['chunkTr'])}</span></p>"
        f"<div class='cols'>{''.join(row(w, w['ex']) for w in wk['words'])}</div></div>" for wk in weeks)
    part2 = ''.join(
        f"<div class='wk'><h3>Level {L['n']} · {html.escape(L['name'])} <span>({html.escape(L['tr'])})</span></h3>"
        f"<p class='sub'>{html.escape(L['sub'])} · {len(L['words'])} kelime</p>"
        f"<div class='cols'>{''.join(row(w) for w in L['words'])}</div></div>" for L in levels)
    part3 = ''.join(
        f"<div class='wk'><h3>{html.escape(t)} <span>({html.escape(s)})</span></h3><p class='sub'>{len(ws)} kelime / ifade</p>"
        f"<div class='cols'>{''.join(row(w) for w in ws)}</div></div>" for t, s, ws in groups if ws)
    n1 = sum(len(wk['words']) for wk in weeks)
    n2 = sum(len(L['words']) for L in levels)
    n3 = len(others)
    total = n1 + n2 + n3
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
.row .w {{ flex: 1; min-width: 0 }}
.row .w b {{ font-size: 11.5pt }}
.row .tr {{ color: #334155; font-size: 10pt }}
.row .ex {{ display: block; color: #64748b; font-size: 8.5pt; font-style: italic }}
.row .ck {{ width: 13px; height: 13px; flex: none; border: 1.5px solid #94a3b8; border-radius: 3px }}
.part {{ break-before: page }}
.part:first-of-type {{ break-before: auto }}
.part > h2 {{ font-size: 18pt; margin: 4px 0 2px; color: #7a1f7a; border-bottom: 3px solid #ff2e88; padding-bottom: 2px }}
.part > p {{ margin: 2px 0 8px; color: #55665c }}
.wk {{ break-inside: avoid; margin: 10px 0 12px }}
.wk h3 {{ margin: 0 0 2px; font-size: 13.5pt; color: #132029 }}
.wk h3 span {{ color: #55665c; font-weight: 600; font-size: 11pt }}
.wk h3 em {{ font-style: normal; font-size: 9pt; background: #fff3c4; border-radius: 6px; padding: 1px 6px; margin-left: 4px }}
.chunk {{ margin: 0 0 4px; font-size: 10pt }}
.chunk span {{ color: #55665c }}
.toc {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 10px }}
.toc div {{ border: 2px solid #132029; border-radius: 10px; padding: 8px 10px; background: #fffdf5 }}
.toc b {{ display: block; font-size: 18pt; color: #7a1f7a }}
footer {{ margin-top: 10px; font-size: 9pt; color: #64748b }}
</style></head><body>
<header><h1>Uras English Cup · Tüm Kelimeler</h1><p>Sitede kullanılan {total} kelime ve ifade · ozgencilimge-prog.github.io/UrasWebSite</p></header>
<div class="toc"><div><b>{n1}</b>Bölüm 1 · 12 haftalık görevlerin kelimeleri</div><div><b>{n2}</b>Bölüm 2 · Word Bank (4 seviye)</div><div><b>{n3}</b>Bölüm 3 · Oyun kelimeleri (Word Tower, Typing Turbo)</div></div>
<div class="how"><b>Nasıl kullanılır?</b><ul>
<li>Her gün 5 kelime seçin. Önce sesli okuyun, sonra Uras tekrar etsin.</li>
<li>Kelimeyi bilince sağdaki kutuya ✓ koyun.</li>
<li>Bölüm 1 haftalık görevlerle aynı sırada. Bölüm 2 ve 3'teki kelimeler Word Bank, Typing Turbo ve Word Tower oyunlarında çıkar.</li>
<li>Her kelime listede bir kez yazıldı; birden fazla oyunda geçse de tekrar edilmedi.</li></ul></div>
<section class="part"><h2>Bölüm 1 · 12 haftalık görevler</h2><p>Listen &amp; Find, Penalty, Memory, Letter Race ve Fill the Gap bu kelimeleri kullanır. Altındaki italik cümle, sitede kelimeyle birlikte okunan örnek cümledir.</p>{part1}</section>
<section class="part"><h2>Bölüm 2 · Word Bank</h2><p>Sitenin Word Bank bölümündeki yeni kelimeler, kolaydan zora 4 seviye.</p>{part2}</section>
<section class="part"><h2>Bölüm 3 · Oyun kelimeleri</h2><p>Word Tower ve Typing Turbo'da çıkan diğer kelime, ifade ve cümleler, uzunluğa göre.</p>{part3}</section>
<footer>Kelimeler 1.–2. sınıf düzeyine ve Uras'ın ilgi alanlarına (futbol, arabalar, oyunlar) göre seçildi. Hikaye cümleleri (Sentence Builder) bu listede yok.</footer>
</body></html>"""
    (HERE / 'kelime-listesi.html').write_text(page, encoding='utf-8')
    print(f"word bank levels: {[len(L['words']) for L in levels]} | skipped (already on site): {', '.join(dropped)}")
    print(f"PDF parts: weekly={n1} word bank={n2} game words={n3} | total={total}")
    if missing:
        print('MISSING TURKISH:', ' | '.join(missing))

if __name__ == '__main__':
    main()
