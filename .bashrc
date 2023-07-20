#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

#alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '

alias ls='exa -1 --icons --colour=always'
alias lsd='exa --icons --colour=always -lah'

eval "$(starship init bash)"

[[ $- == *i* ]] && source /usr/share/blesh/ble.sh

