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
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac



########################################################
# Michealaneous
########################################################
shopt -s extglob

#########################################################
# Aliases
#########################################################
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias h='history | tail'
alias open='xdg-open'
alias grep='grep --color=auto'
alias ls='ls --color=auto'
alias lab="ssh -Y m195922@mich316csd21u.academy.usna.edu"
alias jeremy="ssh -Y sipes@site.furiousmac.com"
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

#########################################################
# Git Initialize Step
#########################################################
# If not in ~ this fails
cd
git pull >/dev/null &
cd -
clear
