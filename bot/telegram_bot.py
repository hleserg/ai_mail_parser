from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from mail.mail_processor import process_mail

# Шаблон функции запуска бота
async def process_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Обработка писем... Ожидайте.")
    excel_path = process_mail()
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open(excel_path, 'rb'))


def run_bot():
    # Здесь вставьте ваш токен Telegram
    app = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN").build()
    app.add_handler(CommandHandler("process", process_command))
    app.run_polling()
