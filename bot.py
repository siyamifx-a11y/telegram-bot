import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("Token")

videos = []
user_index = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Type /video to get a video.")

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not videos:
        await update.message.reply_text("No videos available.")
        return

    index = user_index.get(user_id, 0)
    video_file = videos[index]

    await update.message.reply_video(video_file)

    index = (index + 1) % len(videos)
    user_index[user_id] = index

async def addvideo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        videos.append(update.message.video.file_id)
        await update.message.reply_text("Video added.")
    else:
        await update.message.reply_text("Send a video with this command.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", video))
    app.add_handler(CommandHandler("addvideo", addvideo))

    app.run_polling()

if __name__ == "__main__":
    main()

