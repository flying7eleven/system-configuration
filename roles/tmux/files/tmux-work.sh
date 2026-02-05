#!/usr/bin/env bash

SESSION="work"

# Check if session already exists
if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Session '$SESSION' already exists. Attaching..."
    exec tmux attach-session -t "$SESSION"
fi

# Create the requested windows
tmux new-session -d -s "$SESSION" -n "dada-bot" -c "$HOME/dev/dada-bot"
tmux new-window -t "$SESSION" -n "dada-scripts" -c "$HOME/dev/dada-scripts"
tmux new-window -t "$SESSION" -n "db-changes" -c "$HOME/dev/db-changes"
tmux new-window -t "$SESSION" -n "rufnummern_tickets" -c "$HOME/dev/dada-rufnummern-tickets"
tmux new-window -t "$SESSION" -n "mnps" -c "$HOME/dev/mobile-number-porting-service"

# Attach to session
tmux select-window -t "$SESSION:1"
exec tmux attach-session -t "$SESSION"
