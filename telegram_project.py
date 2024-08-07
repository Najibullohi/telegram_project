from telegram import Update 
from telegram.ext import Updater, CommandHandler, CallbackContext

tasks = {}


def start(update, context):
    user_id = update.effective_chat.id
    if user_id not in tasks:
        tasks[user_id] = []
    update.message.reply_text("Welcome Use /add <task> to add a task, /list to see tasks.")

def add(update, context):
    user_id = update.effective_chat.id
    task = ''.join(context.args)
    if task :
        task[user_id].append(task)
        update.message.reply_text(f"Added task: {task}")
    else:
        update.message.reply_text("Write a task")

def list_task(update, context):
    user_id = update.effective.id
    if user_id in tasks and tasks[user_id]:
        task_list = "\n".join(tasks[user_id])
        update.message.reply_text(f"Your tasks:\n{task_list}")
    else:
        update.message.reply_text("You have no tasks.")

def main():
    updater = Updater("7369350626:AAGeeTIChHzZrAr6WaKCpXRvostsZ9KhwJs", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("list", list_task))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()