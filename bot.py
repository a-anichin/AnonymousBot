import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ========== ЧИТАЕМ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ ==========
BOT_TOKEN = os.getenv('BOT_TOKEN')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== КОМАНДА /START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ на команду /start"""
    await update.message.reply_text(
        "👋 Привет! Я анонимный бот.\n\n"
        "Просто напиши мне любое сообщение, и я анонимно перешлю его в группу.\n"
        "Никто не узнает, кто его отправил!"
    )

# ========== ОБРАБОТКА СООБЩЕНИЙ ИЗ ЛИЧКИ ==========
async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылает сообщения из лички в группу"""
    try:
        # Проверяем, что сообщение пришло из личного чата
        if update.message.chat.type == "private":
            
            # Отправляем в группу копию сообщения (скрывая отправителя)
            await context.bot.copy_message(
                chat_id=GROUP_CHAT_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
            
            # Подтверждаем отправителю
            await update.message.reply_text(
                "✅ Ваше сообщение анонимно отправлено в группу!"
            )
            
            logger.info(f"Сообщение переслано от {update.message.from_user.id}")
            
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await update.message.reply_text(
            "❌ Произошла ошибка при отправке. Попробуйте позже."
        )

# ========== ОБРАБОТКА КОМАНДЫ /STATS (опционально) ==========
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Простая статистика (только для владельца)"""
    # Узнайте свой ID через @userinfobot и замените число ниже
    if update.message.from_user.id == 123456789:  # ЗАМЕНИТЕ НА СВОЙ ID
        await update.message.reply_text(
            f"📊 Статистика:\n"
            f"Бот активен и работает!\n"
            f"ID группы: {GROUP_CHAT_ID}"
        )
    else:
        await update.message.reply_text("У вас нет доступа к этой команде.")

# ========== ЗАПУСК БОТА ==========
if __name__ == '__main__':
    print("🚀 Запуск бота...")
    
    # Создаем приложение
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    
    # ИСПРАВЛЕННЫЙ ОБРАБОТЧИК для сообщений из лички
    # Используем filters.ChatType.PRIVATE вместо filters.PRIVATE
    application.add_handler(
        MessageHandler(
            filters.ChatType.PRIVATE & ~filters.COMMAND,
            forward_to_group
        )
    )
    
    # Запускаем бота
    print("✅ Бот запущен! Нажмите Ctrl+C для остановки.")
    application.run_polling()
