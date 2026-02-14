import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from rasch import estimate_theta, scale_score
from database import init_db, save_student, get_ranking

TOKEN = os.getenv("8173974361:AAEmoPlZRP_OYQqNxpGN_NUvo_EtsKdabic")

init_db()

difficulties = [random.uniform(-2, 2) for _ in range(40)]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 Professional Rasch Test Bot\n\n"
        "Format:\n"
        "/check Ism 1,0,1,...(35) | 2,1,0,2,1"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = " ".join(context.args)
        name_part, answers_part = text.split(" ", 1)
        closed_part, open_part = answers_part.split("|")

        closed = list(map(int, closed_part.strip().split(",")))
        open_scores = list(map(int, open_part.strip().split(",")))

        if len(closed) != 35 or len(open_scores) != 5:
            await update.message.reply_text("35 yopiq + 5 ochiq kerak.")
            return

        open_norm = [x/2 for x in open_scores]
        responses = closed + open_norm

        theta = estimate_theta(responses, difficulties)
        score = scale_score(theta, 100)

        save_student(name_part, theta, score)

        await update.message.reply_text(
            f"📈 {name_part} natijasi:\n"
            f"Theta: {theta}\n"
            f"Score: {score}"
        )

    except Exception as e:
        await update.message.reply_text("Format xato.")

async def ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_ranking()
    text = "🏆 Reyting:\n\n"
    for i, (name, score) in enumerate(data, 1):
        text += f"{i}. {name} - {score}\n"
    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("check", check))
app.add_handler(CommandHandler("ranking", ranking))

app.run_polling()
