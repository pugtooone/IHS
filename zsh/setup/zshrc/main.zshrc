# oh-my-zsh setup {{{
#---------------------------------------------------------------------------
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="agnoster"

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment one of the following lines to change the auto-update behavior
# zstyle ':omz:update' mode disabled  # disable automatic updates
# zstyle ':omz:update' mode auto      # update automatically without asking
# zstyle ':omz:update' mode reminder  # just remind me to update when it's time

# Uncomment the following line to change how often to auto-update (in days).
# zstyle ':omz:update' frequency 13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# You can also set it to another string to have that shown instead of the default red dots.
# e.g. COMPLETION_WAITING_DOTS="%F{yellow}waiting...%f"
# Caution: this setting can cause issues with multiline prompts in zsh < 5.7.1 (see #5765)
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(git
	web-search
	zsh-autosuggestions
	)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"

#}}}

# zeric's startup {{{

# Options
  # setopt extened_glob
  setopt rc_expand_param
  setopt rc_quotes
  # setopt auto_cd
  setopt no_global_rcs
  setopt prompt_subst

# Parameters
  PS4=$'+%N:%{\e[43m%}%i%{\e[0m%}:%_>'
  PATH="$PATH:/Users/zeric.chan/homebrew/bin"
  CDPATH="$HOME/Desktop"
  FPATH="$FPATH:$HOME/.zfunc"
  NVIM="$HOME/.config/nvim"

# Functions
  autoload -U compinit
  # Completion
    zstyle ':completion:*:message' format %d
    zstyle ':completion:*:warnings' format 'No matches: %d'
    zstyle ':completion:*:descriptions' format %B%d%b
    zstyle ':completion:*' group-name ''
  autoload -U backitup
  autoload -U retest
  autoload -U l1
  autoload -U jpgdrag
  autoload -U pngdrag

# Modules
  zmodload zsh/zpty #cmp-zsh requirement
  zmodload zsh/complist

# Aliases
  alias -g D="$HOME/Desktop"
  alias -g brand="$HOME/Desktop/DOCUMENTS/Brand"
  alias imgdrag="mv -i **/*(.) ." 
  alias seeallfiles="ls **/*(.) | cat -n"
  alias zgit="cd $HOME/.zeric/.zgit"

# Startup commands
  clear  
  neofetch
  cowsay -f dragon 'Roar!! I don''t want OT!!'

# File management
  mv -i $HOME/Desktop/Screenshot* "$HOME/Desktop/DOCUMENTS/Screenshots"
  mv -i $HOME/Desktop/RL/Sending/sent* $HOME/Desktop/RL/Sent
  rm $HOME/Desktop/**/*Thumbs.db

# Source for programs
  source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  source /Users/zeric.chan/.config/broot/launcher/bash/br

# zsh-syntax-highlighting config
  ZSH_HIGHLIGHT_HIGHLIGHTERS=( main brackets )
  ZSH_HIGHLIGHT_STYLES[command]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=blue,bold'
  ZSH_HIGHLIGHT_STYLES[function]='fg=magenta,blod'
  ZSH_HIGHLIGHT_STYLES[path]='fg=yellow,blod'
  ZSH_HIGHLIGHT_STYLES[history-expansion]='fg=blue,bg=yellow,blod'

#}}}

vim: set foldmethod=marker foldlevel=0: 2>/dev/null
