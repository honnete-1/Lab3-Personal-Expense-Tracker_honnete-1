#!/bin/bash
# archive_expenses.sh
# Simple helper script to archive daily expense files by date.
# It moves expenses_YYYY-MM-DD.txt into the archives/ folder and
# logs what it did. It can also search inside the archives.

ARCH_DIR="archives"
LOG_FILE="archive_log.txt"

# Making sure that archive directory exists
mkdir -p "$ARCH_DIR"

echo "1) Archive expense file by date"
echo "2) Search archived expenses by date"
echo "3) Exit"
read -rp "Choose option (1-3): " choice

if [ "$choice" = "1" ]; then
    read -rp "Enter date (YYYY-MM-DD): " target_date
    file="expenses_${target_date}.txt"

    if [ -f "$file" ]; then
        timestamp=$(date +%s)
        newname="${file%.txt}_$timestamp.txt"
        mv "$file" "$ARCH_DIR/$newname"
        echo "$(date): Archived $file as $newname" >> "$ARCH_DIR/$LOG_FILE"
        echo "Archived successfully."
    else
        echo "No expense file found for that date in the current folder."
    fi

elif [ "$choice" = "2" ]; then
    read -rp "Enter date to search for (YYYY-MM-DD): " look_date
    echo "Searching archived files for $look_date..."
    if ! grep -R "$look_date" -n "$ARCH_DIR"; then
        echo "No archived records found for that date."
    fi
else
    echo "Goodbye!"
fi

