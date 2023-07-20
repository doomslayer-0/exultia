if status is-interactive
    # Commands to run in interactive sessions can go here
end
starship init fish | source
export PATH="$HOME/.config/emacs/bin:$HOME/.cargo/bin:$HOME/.local/bin:$PATH"
