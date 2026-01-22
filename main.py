import os
import asyncio
from datetime import datetime, time, date
import pytz

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

# =====================
# CONFIG
# =====================

TOKEN = os.getenv("TOKEN")

TZ = pytz.timezone("Europe/Rome")

# 21 gennaio cambiato alle 18:30-18:45
START_TIME = time(16, 30)
END_TIME   = time(17, 00)

ACTIVE_DATES = {
    date(2026, 1, 21),
    date(2026, 1, 22),
    date(2026, 1, 23),
}

winner_declared = False

OUTSIDE_MSG = "🕊️ too early / too late 🕊️"

# =====================
# TESTI (IDENTICI AI TUOI)
# =====================

TEXT_1 = """Find the latin letters to find the TikTok account.


夜の湿地は、まるで眠れない夢のように広がっていた。
霧が地面をなぞり、草の葉を濡らし、遠くの木々は P けた影を落としている。
その影は揺れ、まるで私の足元を見張っているかのようだ。

私は歩く。
足音は水に吸い込まれ、音は A まるで存在しないかのように消える。
しかし、耳を澄ますと、どこかで虫が鳴き、どこかで鳥が笑っている。
それはこの場所の「挨拶」だ。

湿った空気の中、私は思い出す。
昔、ここに来た誰かが言った。
「湿地は魂をL いかせる場所だ」と。
その言葉が頭の中で繰り返され、
私は自分の心臓の鼓動を数える。

鼓動は速い。
それは恐怖のせいか、
それともこの場所が私を歓迎しているからか。
どちらにしても、私は前へ進む。
そして、ふと気づく。
私の影が U いつもより長い。
まるで、私の影が別の世界に手を伸ばしているようだ。

古い橋の跡が見える。
木の板は腐り、
釘は錆びて、
そこに誰かの足跡が残っている。
その足跡は深く、
D かい印のように残っていた。
私はそれを追う。

追ううちに、私は小さな池に出た。
水面は静かで、
月がそこに映っている。
その月は E いくつもの顔を持っているように見えた。
一つは優しい、
一つは怒っている、
一つは悲しんでいる。

私はその月を見て、
自分が何を探しているのか考える。
答えは簡単だ。
私はこの場所の秘密を知りたい。
そして、ここにあるものを見つけたい。

そのとき、風が A まるで囁くように吹いた。
「ここにいると、あなたは変わる」と。
私はその言葉を信じたくない。
でも、信じざるを得ない。

湿地の奥へ進むと、
草の間から小さな光が見えた。
それは蛍ではない。
もっと強い光。
私はその光に近づく。
光の中には、小さなP 影が揺れていた。

その影は、私に向かって手を伸ばした。
私は怖くて後退しようとしたが、
足が動かない。
そのとき、影はさらに近づき、
私の名前を呼ぶようにP り返す音を出した。

私はその音を聞いて、
この場所が私を知っていることに気づいた。
私は自分がここにいる理由を理解した。
そして、私は決めた。
私はこの場所から逃げない。

逃げない代わりに、私はこの場所とI いっしょになる。
私の呼吸は湿地の空気と混ざり、
私の足跡は泥の中に溶けていく。
私はこの場所の一部になる。

そして、私の目の前に、
古い石碑が現れた。
そこには文字が刻まれている。
読むことはできない。
しかし、私はその中に C という形を見つけた。
そして、その形は繰り返されていた。

繰り返される C は、
まるでこの場所が何かを伝えようとしているかのようだ。
私は石碑に近づき、
手を触れる。
触れた瞬間、
冷たい感触が体を走った。

その感触は、
私の中の何かを目覚めさせた。
そして、私は思った。
「私はこの湿地の一部だ」と。

湿地の中で、
私は自分の声が消えるのを感じた。
声は水に吸い込まれ、
そして、遠くで O うっとりするような音が鳴った。
その音は、まるで歓迎の歌のようだった。

私はその音に導かれ,
さらに奥へ進む。
すると、草の間から
小さな鳥が飛び出した。
その鳥は一瞬、私を見て,
そして S いせつな鳴き声を残して消えた。

私はその鳴き声を聞いて,
自分がもう元の世界に戻れないことを悟った。
でも、怖くない。
なぜなら、
この場所は私を拒まない。

最後に、私は静かな水面に立ち,
その上に映る月を見た。
月はA まるで私に微笑んでいるようだった。
私はその微笑みを受け取り,
そして、ゆっくりと目を閉じた。

5195
"""

TEXT_2 = """Find the TikTok account for winning a snippet. Remember, alphabet has 26 letters.
(4 letters, 5 numbers)

黑暗。
hēi àn.

海边城市睡了，我听到风在说话。
hǎi biān chéng shì shuì le, wǒ tīng dào fēng zài shuō huà。

土块分开像书，里面有一个个灭亡的名字，我一个一个读。
tǔ kuài fēn kāi xiàng shū，lǐ miàn yǒu yī gè gè miè wáng de míng zì，wǒ yī gè yī gè dú。

影子延长在墙上，每一步都是一个秘密。
yǐng zi yán cháng zài qiáng shàng，měi yī bù dōu shì yī gè mìmì。

五钟一个都没。
wǔ zhōng yī gè dōu méi。

（空白）
(pausa)

四星落下。
sì xīng luò xià。

八只乌鸦带走我名字。
bā zhī wū yā dài zǒu wǒ míng zì。

七次走回七次失。
qī cì zǒu huí qī cì shī。
"""

# =====================
# UTILS
# =====================

def now_it():
    return datetime.now(TZ)

def active():
    now = now_it()
    return now.date() in ACTIVE_DATES and START_TIME <= now.time() <= END_TIME

async def delete_after(msg, delay):
    await asyncio.sleep(delay)
    await msg.delete()

# =====================
# HANDLERS
# =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(OUTSIDE_MSG)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global winner_declared

    if not active():
        await update.message.reply_text(OUTSIDE_MSG)
        return

    today = now_it().day
    text = update.message.text.strip()

    if today == 21:
        msg = await update.message.reply_text(TEXT_1)
        asyncio.create_task(delete_after(msg, 1800))

    elif today == 22:
        msg = await update.message.reply_text(TEXT_2)
        asyncio.create_task(delete_after(msg, 1800))

    elif today == 23:
        # SOLO PRIVATO e SOLO PRIMO CHE SCRIVE YGL
        if update.message.chat.type == "private":
            if text == "YGL" and not winner_declared:
                winner_declared = True
                await update.message.reply_text("pause6741")

# =====================
# MAIN
# =====================

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
