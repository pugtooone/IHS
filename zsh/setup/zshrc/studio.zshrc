# zeric's zsh startup script for IHS devices
# run the following command on the command line to back this zshrc up, and create your own
# cp $HOME/.zshrc $HOME/.zshrc_backup && vim $HOME/.zshrc

# vim setup 
if [[ ! -e $HOME/.vimrc ]]; then
	touch $HOME/.vimrc
	print "set number" >$HOME/.vimrc
fi

# Option 
  setopt always_to_end
  setopt auto_cd
  setopt extended_glob
  setopt hist_ignore_dups
  setopt hist_ignore_space
  setopt hist_verify
  setopt no_flow_control
  setopt rc_expand_param
  setopt rc_quotes

# Functions
  autoload -U compinit
  # zsh Completions
    zstyle ':completion:*' format %d
    zstyle ':completion:*:warnings' format 'No matches: %d'
    zstyle ':completion:*:descriptions' format %B%d%b
    zstyle ':completion:*' group-name ''

# Alias
  alias l="ls -lAh"
  alias l1="ls -1AG | cat -n"
  alias -g D="$HOME/Desktop"
  alias -g prod="$HOME/Desktop/Production"

# Parameters
  PS1=$'%{\e[32m%}[%!]%{\e[0m%} %n %{\e[34m%}[%1~]%{\e[0m%} %# '
  PS4=$'+%N:%{\e[43m%}%i%{\e[0m%}:%_>'
  CDPATH="$CDPATH:$HOME/Desktop"
  FPATH="$FPATH:$HOME/.zfunc"
  HISTFILE="$HOME/.zsh_history"
  HISTSIZE=10000
  SAVEHIST=10000

# zsh-syntax-highlighting config
  ZSH_HIGHLIGHT_HIGHLIGHTERS=( main brackets )
  ZSH_HIGHLIGHT_STYLES[command]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[function]='fg=magenta,blod'
  ZSH_HIGHLIGHT_STYLES[path]='fg=yellow,blod'
  ZSH_HIGHLIGHT_STYLES[history-expansion]='fg=blue,bg=yellow,blod'

# File Management

  if [[ ! -d $HOME/Desktop/Screenshots ]]; then
  	mkdir $HOME/Desktop/Screenshots
  	mv -i $HOME/Desktop/Screenshot*(.) $HOME/Desktop/Screenshots(/)
  else
  	mv -i $HOME/Desktop/Screenshot*(.) $HOME/Desktop/Screenshots(/)
  fi

vim: set foldmethod=marker foldlevel=0 :
