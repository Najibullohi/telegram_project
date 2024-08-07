from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import CallbackQueryHandler
from collections import defaultdict

TOKEN = '7311265297:AAH1FR-hC57hIW3IvfwlKFdAnZ-8tn_zv-w'

tasks = defaultdict(list)
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if not tasks.get(user_id):
        tasks[user_id] = []
        update.message.reply_text("Welcome! You are now registered. Use /add <task name> to add tasks.")
    else:
        update.message.reply_text("Welcome back! Use /add <task name> to add tasks.")

def add(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    task_name = ' '.join(context.args)
    if task_name:
        tasks[user_id].append(task_name)
        update.message.reply_text(f"Task added: {task_name}")
        list_tasks(update, context)
    else:
        update.message.reply_text("Please provide a task name. Usage: /add <task name>")

def list_tasks(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if tasks.get(user_id):
        task_list = '\n'.join(f"{i+1}. {task}" for i, task in enumerate(tasks[user_id]))
        update.message.reply_text(f"Your tasks:\n{task_list}")
    else:
        update.message.reply_text("You have no tasks yet.")

def delete(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        task_number = int(context.args[0]) - 1
        if 0 <= task_number < len(tasks[user_id]):
            removed_task = tasks[user_id].pop(task_number)
            update.message.reply_text(f"Task removed: {removed_task}")
            list_tasks(update, context)
        else:
            update.message.reply_text("Invalid task number.")
    except (IndexError, ValueError):
        update.message.reply_text("Please provide a valid task number. Usage: /delete <task number>")

def edit(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        task_number = int(context.args[0]) - 1
        new_name = ' '.join(context.args[1:])
        if 0 <= task_number < len(tasks[user_id]) and new_name:
            old_task = tasks[user_id][task_number]
            tasks[user_id][task_number] = new_name
            update.message.reply_text(f"Task updated from '{old_task}' to '{new_name}'")
            list_tasks(update, context)
        else:
            update.message.reply_text("Invalid task number or missing new name.")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /edit <task number> <new name>")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/start - Register or start interacting with the bot\n"
        "/add <task name> - Add a new task\n"
        "/list - List all tasks\n"
        "/delete <task number> - Delete a task by number\n"
        "/edit <task number> <new name> - Edit a task by number\n"
        "/help - Show this help message"
    )

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('add', add))
    dispatcher.add_handler(CommandHandler('list', list_tasks))
    dispatcher.add_handler(CommandHandler('delete', delete))
    dispatcher.add_handler(CommandHandler('edit', edit))
    dispatcher.add_handler(CommandHandler('help', help_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()