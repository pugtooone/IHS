# zeric's zsh startup script
# run the following command on the command line to back this zshrc up, and create your own
# cp $HOME/.zshrc $HOME/.zshrc_backup && vim $HOME/.zshrc

# vim setup 
if [[ ! -e $HOME/.vimrc ]]; then
	touch $HOME/.vimrc
	print "set number" >$HOME/.vimrc
fi

# Option 
  setopt extended_glob
  setopt rc_expand_param
  setopt rc_quotes
  setopt auto_cd
  setopt hist_ignore_dups
  setopt hist_ignore_space
  setopt hist_verify
  setopt always_to_end

# Functions
  autoload -U compinit
  # zsh Completions
    zstyle ':completion:*' format %d
    zstyle ':completion:*:warnings' format 'No matches: %d'
    zstyle ':completion:*:descriptions' format %B%d%b
    zstyle ':completion:*' group-name ''
  autoload -U backitup
  autoload -U retest
  autoload -U jpgdrag
  autoload -U l1

# Alias
  alias l="ls -lAh"
  # alias l1="ls -1AG | cat -n"
  alias -g D="$HOME/Desktop"
  alias -g prod="$HOME/Desktop/Production"

# Parameters
  PS1=$'%{\e[33m%}[%!]%{\e[0m%} %n %{\e[33m%}[%1~]%{\e[0m%} %# '
  PS1=$'+%N:%{\e[33m%}[%i]%{\e[0m%}> '
  CDPATH="$CDPATH:$HOME/Desktop"
  HISTFILE="$HOME/.zsh_history"
  HISTSIZE=10000
  SAVEHIST=10000

# File Management
  mv -i $HOME/Desktop/Screenshot*(.) $HOME/Desktop/Screenshots(/)

vim: set foldmethod=marker foldlevel=0 :
