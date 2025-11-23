# Personal Expense Tracker
# Command-line tool to track daily expenses using plain text files.
# - One file per date: expenses_YYYY-MM-DD.txt
# - Balance stored in balance.txt as "initial,current"
# - Menu: check balance, view expenses, add expense, exit

import os
from datetime import datetime

BALANCE_FILE = "balance.txt"
def pause():
    # Small helper to avoid the menu jumping too fast.
    input("\nPress Enter to continue...")

def migrate_old_expense_files():
    """
    Migration:
    If there are any old expense files that use commas instead of
    pipes, this function converts their lines into the correct
    format:
        ID | Date | Time | Item | Amount
    It is safe to run multiple times.
    """
    for name in os.listdir():
        if not (name.startswith("expenses_") and name.endswith(".txt")):
            continue
        if not os.path.isfile(name):
            continue

        lines_changed = False
        new_lines = []

        with open(name, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                # If it already uses | and has 5 parts, keep as is
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) == 5:
                        new_lines.append(
                            f"{parts[0]} | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]}\n"
                        )
                        continue

                # If it uses commas and has 5 parts, convert
                if "," in line:
                    parts = [p.strip() for p in line.split(",")]
                    if len(parts) == 5:
                        new_lines.append(
                            f"{parts[0]} | {parts[1]} | {parts[2]} | {parts[3]} | {parts[4]}\n"
                        )
                        lines_changed = True
                        continue

                # Otherwise, keep the line as is
                new_lines.append(raw)

        if lines_changed:
            with open(name, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
def load_balance():
    """
    Reads the balance from balance.txt.
    File format: initial_balance,current_balance
    Example: 5000.00,4200.00
    """
    if not os.path.exists(BALANCE_FILE):
        return 0.0, 0.0

    try:
        raw = open(BALANCE_FILE, "r", encoding="utf-8").read().strip()
        if not raw:
            return 0.0, 0.0
        parts = [p.strip() for p in raw.split(",")]
        if len(parts) == 1:
            value = float(parts[0])
            return value, value
        initial = float(parts[0])
        current = float(parts[1])
        return initial, current
    except Exception:
        return 0.0, 0.0

def save_balance(initial, current):
    # Writes the two balances back into balance.txt.
    with open(BALANCE_FILE, "w", encoding="utf-8") as f:
        f.write(f"{initial:.2f},{current:.2f}\n")
def get_expense_files():
    # Returns all active expense files in the current folder.
    files = []
    for name in os.listdir():
        if name.startswith("expenses_") and name.endswith(".txt") and os.path.isfile(name):
            files.append(name)
    return sorted(files)

def read_all_expenses():
    """
    Reads all active expense files and yields tuples:
    (filename, exp_id, date_str, time_str, item, amount)
    """
    for filename in get_expense_files():
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    parts = [p.strip() for p in line.strip().split("|")]
                    if len(parts) != 5:
                        continue
                    exp_id_str, date_str, time_str, item, amount_str = parts
                    try:
                        exp_id = int(exp_id_str)
                        amount = float(amount_str)
                    except ValueError:
                        continue
                    yield filename, exp_id, date_str, time_str, item, amount
        except FileNotFoundError:
            continue
def compute_total_expenses():
    """Adds up all amounts across all active expense files."""
    total = 0.0
    for _fname, _id, _date, _time, _item, amount in read_all_expenses():
        total += amount
    return total
def check_remaining_balance():
    """
    Shows a small report about the user's money:
    - Initial balance
    - Total expenses (from files)
    - Available (current) balance

    Also allows the user to add more money to their balance.
    """
    initial, current = load_balance()
    total_spent = compute_total_expenses()

    print("\n=== Remaining Balance Report ===")
    print(f"Initial balance       : {initial:.2f}")
    print(f"Total expenses to date: {total_spent:.2f}")
    print(f"Available balance     : {current:.2f}")

    choice = input("\nDo you want to add money to your balance? (y/n): ").strip().lower()
    if choice == "y":
        amount_str = input("Enter amount to add: ").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be a positive number.")
            else:
                initial += amount
                current += amount
                save_balance(initial, current)
                print(f"Balance updated. New balance: {current:.2f}")
        except ValueError:
            print("That does not look like a valid number.")
    pause()


def get_next_expense_id(filename):
    
    # The fubnction finds the next ID for a given daily file. If the file does not exist or is empty, ID starts at 1.
    
    if not os.path.exists(filename):
        return 1

    last_id = 0
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.split("|", 1)
                if not parts:
                    continue
                try:
                    last_id = int(parts[0].strip())
                except ValueError:
                    continue
    except FileNotFoundError:
        return 1

    return last_id + 1


def validate_date(date_str):
    # Very light date validation for format YYYY-MM-DD.
    # This keeps things simple while catching obvious mistakes.
    
    if len(date_str) != 10:
        return False
    parts = date_str.split("-")
    if len(parts) != 3:
        return False
    year, month, day = parts
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return False
    return True


def add_new_expense():
    
    # This function asks the user for date, item name and amount.
    # It also validates input, checks balance, then appends the expense into the correct daily file: expenses_YYYY-MM-DD.txt
    
    initial, current = load_balance()
    print(f"\nCurrent available balance: {current:.2f}")

    date_str = input("Enter date (YYYY-MM-DD): ").strip()
    if not validate_date(date_str):
        print("Invalid date format. Expected YYYY-MM-DD.")
        pause()
        return

    item = input("Enter item name (what did you spend on?): ").strip()
    if not item:
        print("Item name cannot be empty.")
        pause()
        return

    amount_str = input("Enter amount spent: ").strip()
    try:
        amount = float(amount_str)
        if amount <= 0:
            print("Amount must be a positive number.")
            pause()
            return
    except ValueError:
        print("That does not look like a valid number.")
        pause()
        return

    # Make sure the user cannot overspend
    if amount > current:
        print("\nInsufficient balance! Cannot save expense.")
        pause()
        return

    print("\nPlease review your expense:")
    print(f"Date  : {date_str}")
    print(f"Item  : {item}")
    print(f"Amount: {amount:.2f}")
    confirm = input("Save this expense? (y/n): ").strip().lower()
    if confirm != "y":
        print("Expense was not saved.")
        pause()
        return

    filename = f"expenses_{date_str}.txt"
    next_id = get_next_expense_id(filename)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{next_id} | {date_str} | {timestamp} | {item} | {amount:.2f}\n")
    except OSError as e:
        print(f"Could not save expense due to a file error: {e}")
        pause()
        return

    current -= amount
    save_balance(initial, current)

    print(f"Expense saved successfully. Remaining balance: {current:.2f}")
    pause()


def search_by_item():
    # Searches through ALL active expense files for a given text in the item name. Results are shown as a flat list.
    
    keyword = input("Enter item name or part of it to search: ").strip().lower()
    if not keyword:
        print("Search text cannot be empty.")
        pause()
        return

    print(f"\n=== Search Results for '{keyword}' ===\n")
    found_any = False

    for fname, exp_id, date_str, time_str, item, amount in read_all_expenses():
        if keyword in item.lower():
            print(
                f"File: {fname} | ID: {exp_id} | Date: {date_str} | Time: {time_str} "
                f"| Item: {item} | Amount: {amount:.2f}"
            )
            found_any = True

    if not found_any:
        print("No matching expenses found.")
    pause()


def search_by_amount():
    
    # Searches through ALL active expense files for an exact matching amount.
    
    amount_str = input("Enter amount to search for: ").strip()
    try:
        target = float(amount_str)
    except ValueError:
        print("That does not look like a valid number.")
        pause()
        return

    print(f"\n=== Search Results for amount '{target:.2f}' ===\n")
    found_any = False

    for fname, exp_id, date_str, time_str, item, amount in read_all_expenses():
        if amount == target:
            print(
                f"File: {fname} | ID: {exp_id} | Date: {date_str} | Time: {time_str} "
                f"| Item: {item} | Amount: {amount:.2f}"
            )
            found_any = True

    if not found_any:
        print("No expenses found matching that amount.")
    pause()


def view_expenses():
    """
    Menu for viewing expenses. Lets the user choose how to search.
    """
    while True:
        print("\n=== View Expenses ===")
        print("1. Search by item name")
        print("2. Search by amount")
        print("3. Back to main menu")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            search_by_item()
        elif choice == "2":
            search_by_amount()
        elif choice == "3":
            return
        else:
            print("Invalid choice. Please pick 1, 2 or 3.")
            pause()


def main():
    """
    Main menu loop of the application.
    It keeps running until the user chooses to Exit.
    """
    # First, migrate any old files that might be using commas
    migrate_old_expense_files()

    while True:
        print("\n=================================================")
        print("             Personal Expense Tracker")
        print("=================================================\n")
        print("1. Check Remaining Balance")
        print("2. View Expenses")
        print("3. Add New Expense")
        print("4. Exit\n")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            check_remaining_balance()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            add_new_expense()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please choose between 1 and 4.")
            pause()


if __name__ == "__main__":
    main()
