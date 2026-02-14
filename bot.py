import os
import math
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# TOKEN Render environmentdoan olinadi
TOKEN = os.getenv(8173974361:AAEmoPlZRP_OYQqNxpGN_NUvo_EtsKdabic)

# 40 ta savol difficulty (-2 dan +2 gacha)
difficulties = [random.uniform(-2, 2) for _ in range(40)]

# Rasch ehtimollik
def rasch_probability(theta, b):
    return 1 / (1 + math.exp(-(theta - b)))

# Theta hisoblash (MLE)
def estimate_theta(responses, max_iter=20):
    theta = 0.0
    for _ in range(max_iter):
        num = 0
        den = 0
        for x, b in zip(responses, difficulties):
            p = rasch_probability(theta, b)
            num += x - p
            den += p * (1 - p)
        if den == 0:
            break
        theta += num / den
    return round(theta, 4)

def scale_score(theta):
    return round((theta + 3) / 6 * 100, 2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Rasch Professional Bot\n\n"
        "Format:\n"
        "/check Ism 35ta_yopiq | 5ta_ochiq\n\n"
        "Misol:\n"
        "/check Ali 1,0,1,...(35) | 2,1,0,2,1"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = " ".join(context.args)
        name, rest = text.split(" ", 1)
        closed_part, open_part = rest.split("|")

        closed = list(map(int, closed_part.strip().split(",")))
        open_scores = list(map(int, open_part.strip().split(",")))

        if len(closed) != 35 or len(open_scores) != 5:
            await update.message.reply_text("35 yopiq + 5 ochiq javob kiriting.")
            return

        open_norm = [x/2 for x in open_scores]
        responses = closed + open_norm

        theta = estimate_theta(responses)
        score = scale_score(theta)

        await update.message.reply_text(
            f"📈 {name} natijasi:\n"
            f"Theta: {theta}\n"
            f"Score: {score}"
        )

    except:
        await update.message.reply_text("Format xato.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check", check))

print("Bot ishga tushdi...")

app.run_polling()
