# zeric's zsh startup script for IHS devices
# run the following command on the command line to back this zshrc up, and create your own
# cp $HOME/.zshrc $HOME/.zshrc_backup && vim $HOME/.zshrc

# Option 
  setopt always_to_end
  setopt auto_cd
  setopt extended_glob
  setopt hist_ignore_dups
  setopt hist_ignore_space
  setopt hist_verify
  setopt no_flow_control
  setopt no_global_rcs
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
  alias l="ls -lAGh"
  alias l1="ls -1AG | cat -n"
  alias D="cd $HOME/Desktop"
  alias prod="cd $HOME/Desktop/Production"
  alias pgrep="pgrep -li"

# Parameters
  PS1=$'%{\e[1;36m%}[%!]%{\e[0m%} %{\e[1;32m%}%n%{\e[0m%} %{\e[1;36m%}[%1~]%{\e[0m%} %# '
  PS4=$'+%N:%{\e[43m%}%i%{\e[0m%}:%_>'
  CDPATH="$CDPATH:$HOME/Desktop"
  FPATH="$FPATH:$HOME/.zfunc"
  HISTFILE="$HOME/.zsh_history"
  HISTSIZE=10000
  SAVEHIST=10000

# zsh-syntax-highlighting config
  ZSH_HIGHLIGHT_HIGHLIGHTERS=( main brackets )

# File Management

  if [[ ! -d $HOME/Desktop/Screenshots ]]; then
  	mkdir $HOME/Desktop/Screenshots
  	mv -i $HOME/Desktop/Screenshot*(.) $HOME/Desktop/Screenshots(/)
  else
  	mv -i $HOME/Desktop/Screenshot*(.) $HOME/Desktop/Screenshots(/)
  fi

# Sourcing plugins
# download git by running the command: xcode-select --install, which is used to clone the plugins to the device
source ~/.zsh/zsh-autosuggestions/zsh-autosuggestions.zsh
source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

vim: set foldmethod=marker foldlevel=0 : 2>/dev/null
