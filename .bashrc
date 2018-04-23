#######################################
#      HISTORY      
#######################################
HISTCONTROL=ignoreboth
shopt -s histappend
HISTSIZE=1000
HISTFILESIZE=2000


######################################
#   WINDOW  
######################################
shopt -s checkwinsize
#Window title is m195922@directory
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\033[01;32m\]\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w\[\033[0m\]\$ "
    ;;
*)
    ;;
esac



########################################################
# Michealaneous
########################################################
shopt -s extglob
umask 026

#########################################################
# Aliases
#########################################################
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias h='history | tail'
alias open='xdg-open'
alias grep='grep --color=auto'
alias ls='ls -F --color=auto'
alias lab="ssh -Y m195922@mich316csd21u.academy.usna.edu"
alias jeremy="ssh -Y sipes@site.furiousmac.com"
alias porpoise="ssh -Y bssipes@gigether.net"
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

#########################################################
# Git Initialize Step
#########################################################
# If not in ~ this fails
cd
git pull 2>&1 >/dev/null &
cd -
clear
