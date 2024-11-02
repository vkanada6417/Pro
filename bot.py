import subprocess  # Импортируем библиотеку для выполнения команд терминала
import logging  # Импортируем библиотеку для логирования
from telegram import Update  # Импортируем класс Update для работы с обновлениями Telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes  # Импортируем необходимые классы для создания бота

# Токен вашего бота Telegram
ТOKEN = ""

# Функция для взаимодействия с моделью LLaMA через командную строку Ollama
def query_llama(prompt: str) -> str:
    try:
        # Запускаем команду ollama CLI для генерации ответа от модели
        result = subprocess.run(
            ["ollama", "run", "llama3.2"],  # Команда запуска модели llama3.2 в Ollama
            input=f"{prompt}\n/bye\n",  # Отправляем запрос и команду /bye для завершения сеанса
            capture_output=True,  # Указываем, что нужно захватить вывод команды
            text=True,  # Вывод будет возвращен в виде строки
            check=True  # Вызывает ошибку, если команда завершается с ошибкой
        )
        return result.stdout.strip()  # Возвращаем ответ модели, убрав лишние пробелы
    except subprocess.CalledProcessError as e:
        # Логируем ошибку в случае неудачи выполнения команды
        logging.error(f"Ошибка при генерации ответа от LLaMA: {e.stderr}")
        return "Извините, не удалось получить ответ от модели LLaMA."

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот на базе LLaMA. Спроси меня о чем угодно!")

# Обработчик входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text  # Получаем текст сообщения от пользователя
    logging.info(f"Получено сообщение: {user_message}")
    
    # Получаем ответ от модели LLaMA
    bot_response = query_llama(user_message)
    logging.info(f"Ответ LLaMA: {bot_response}")
    
    # Отправляем ответ пользователю
    await update.message.reply_text(bot_response)

# Основная функция для запуска бота и настройки обработчиков
def main():
    # Настраиваем логирование
    logging.basicConfig(level=logging.INFO)
    
    # Создаем приложение (Telegram бот)
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Добавляем обработчики для команд и сообщений
    app.add_handler(CommandHandler("start", start))  # Обработчик для команды /start
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Обработчик для текстовых сообщений (не команд)
    
    # Запускаем опрос для получения сообщений
    logging.info("Бот запускается...")
    app.run_polling()  # Запускает бота в режиме опроса для получения обновлений

# Запуск бота
if __name__ == "__main__":
    main()
