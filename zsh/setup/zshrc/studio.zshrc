# zeric's zsh startup script for IHS devices

#{{{

# run the following command on the command line to back this zshrc up, and create your own
# cp $HOME/.zshrc $HOME/.zshrc_backup && vim $HOME/.zshrc

# Option 
  setopt always_to_end
  setopt auto_cd
  setopt auto_pushd
  setopt csh_null_glob
  setopt extended_glob
  setopt hist_ignore_dups
  setopt hist_ignore_space
  setopt hist_verify
  setopt no_flow_control
  setopt no_global_rcs
  setopt prompt_subst
  setopt pushd_ignore_dups
  setopt rc_expand_param
  setopt rc_quotes

# Modules
  zmodload zsh/complist

# Functions
  autoload -U compinit
  compinit
  # zsh Completions
    zstyle ':completion:*' format %d
    zstyle ':completion:*:warnings' format 'No matches: %d'
    zstyle ':completion:*:descriptions' format %B%U%d%u%b
    zstyle ':completion:*' group-name ''
    zstyle ':completion:*' verbose yes
    zstyle ':completion:*' auto-description 'specify: %d'
    zstyle ':completion:*:default' list-prompt '%S%P%M%s'
    zstyle ':completion:::::' completer _complete _approximate #approximate completion setup
    zstyle ':completion:*:approximate:*' max-errors 2
    zstyle ':completion:*:corrections' format '%B%d [errors: %e]%b'

# Alias
  alias -g C=" | cat -n"
  alias D="cd $HOME/Desktop"
  alias -g L=" | less"
  alias l="ls -lAGh"
  alias l1="ls -1AG"
  alias prod="cd $HOME/Desktop/Production"
  alias pgrep="pgrep -li"
  alias dv="dirs -v"

# Parameters
  PS1=$'%S[%!]%s %n %S[%~]%s %# '
  PS4=$'+%N:%{\e[43m%}%i%{\e[0m%}:%_>'
  typeset -U CDPATH="$CDPATH:$HOME/Desktop/(Production|PRODUCTION)"
  typeset -U FPATH="$FPATH:$HOME/.zfunc"
  SHELL_SESSION_HISTORY=0
  HISTFILE="${HISTFILE:-$HOME/.zsh_history}"
  HISTSIZE=10000
  SAVEHIST=10000
  DIRSTACKSIZE=8

# File Management
  # create HISTFILE if there is none
  if [[ ! -e $HOME/.zsh_history ]]; then
        touch $HOME/.zsh_history
  fi

  # Clean up Desktop screenshots
  if [[ ! -d $HOME/Desktop/Screenshots ]]; then
  	mkdir $HOME/Desktop/Screenshots
  	mv -i $HOME/Desktop/Screenshot*(.) $HOME/Desktop/Screenshots(/)
  else
  	mv -i $HOME/Desktop/Screenshot*(.) $HOME/Desktop/Screenshots(/)
  fi

  # Clean up RL sent sessions
  if [[ -d $HOME/Desktop/RL ]]; then
  	mv -i $HOME/Desktop/RL/Sending/sent* $HOME/Desktop/RL/Sent
  fi

# Sourcing plugins
# download git by running the command: xcode-select --install, which is used to clone the plugins to the device
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

# zsh-syntax-highlighting config
  ZSH_HIGHLIGHT_HIGHLIGHTERS=( main brackets )
  ZSH_HIGHLIGHT_STYLES[command]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[function]='fg=magenta,blod'
  ZSH_HIGHLIGHT_STYLES[path]='fg=yellow,blod'
  ZSH_HIGHLIGHT_STYLES[history-expansion]='fg=blue,bg=yellow,blod'

# vim: set foldmethod=marker foldlevel=0 :

#}}}
