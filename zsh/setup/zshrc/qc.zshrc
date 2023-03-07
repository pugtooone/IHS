
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#  ███████╗███████╗██████╗ ██╗ ██████╗     ███████╗███████╗██╗  ██╗ #
#  ╚══███╔╝██╔════╝██╔══██╗██║██╔════╝     ╚══███╔╝██╔════╝██║  ██║ #
#    ███╔╝ █████╗  ██████╔╝██║██║            ███╔╝ ███████╗███████║ #
#   ███╔╝  ██╔══╝  ██╔══██╗██║██║           ███╔╝  ╚════██║██╔══██║ #
#  ███████╗███████╗██║  ██║██║╚██████╗     ███████╗███████║██║  ██║ #
#  ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝     ╚══════╝╚══════╝╚═╝  ╚═╝ #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#=================================================================
# oh-my-zsh setup {{{
#=================================================================
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
ZSH_THEME="Zeric's agnoster"

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
plugins=(
	git
	web-search
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
#=================================================================

#=================================================================
# zeric's startup {{{

# Options
  # setopt always_to_end
  # setopt auto_cd
  # setopt auto_pushd
  setopt chase_links
  setopt csh_null_glob
  # setopt extended_glob
  setopt hist_allow_clobber
  # setopt hist_ignore_dups
  setopt hist_reduce_blanks
  # setopt hist_verify
  setopt inc_append_history
  setopt ksh_glob
  setopt list_ambiguous
  setopt no_clobber
  setopt prompt_subst
  # setopt pushd_ignore_dups
  setopt rc_expand_param
  setopt rc_quotes

# Modules
  zmodload zsh/zpty #cmp-zsh requirement
  zmodload zsh/complist

# Functions
  # autoload -U compinit
  # compinit
  # Completion
    zstyle ':completion:*:message' format %d
    zstyle ':completion:*:warnings' format 'No matches: %d'
    zstyle ':completion:*:descriptions' format %B%d%b
    zstyle ':completion:*' group-name ''
    zstyle ':completion:*' verbose yes
    zstyle ':completion:*' auto-description 'specify: %d'
    zstyle ':completion:*:default' list-prompt '%S%P%M%s' #prompt setup for complist
    zstyle ':completion:*:default' menu 'select=0' 
    zstyle ':completion:::::' completer _complete _approximate #approximate completion setup
    zstyle ':completion:*:approximate:*' max-errors 2
    zstyle ':completion:*:corrections' format '%B%d [errors: %e]%b'
  autoload -U backitup
  autoload -U charsort
  autoload -U exportdrag
  autoload -U imgcount
  autoload -U drag_kip_swatch
  autoload -U l1
  autoload -U newimgver
  autoload -U pr_template
  autoload -U qcstart
  autoload -U retest
  autoload -U rl_aem
  autoload -U ToSendFolder

# Parameters
  PS4=$'+%N:%{\e[43m%}%i%{\e[0m%}:%_>'
  typeset -U path=(
       $(brew --prefix)/Cellar/ruby/3.2.1/bin
		   $(brew --prefix)/lib/ruby/gems/3.1.0/bin
		   $path
		   $(brew --prefix)/bin
		   $HOME/.bin/zbin
		   $HOME/.bin/pybin
		   )

  typeset -U cdpath=(
                     .
                     $HOME/Desktop
		     )

  typeset -U fpath=(
                    $fpath
		    $HOME/.zfunc
		    )

  export HOMEBREW_EDITOR=nvim
  export PYTHONPATH="$HOME/.bin/pybin/"

  typeset PYBIN="$HOME/.bin/pybin/"
  typeset ZBIN="$HOME/.bin/zbin/"

  typeset NVIM="$HOME/.config/nvim"
  typeset NVIM_INIT="$HOME/.config/nvim/init.vim"
  typeset ZGIT="$HOME/.zeric/.zgit"

  # associative array for the IHS zshrc
  typeset -A ihsrc=( 
                    qc $HOME/.zeric/.zgit/IHS/zsh/setup/zshrc/qc.zshrc 
		    stud $HOME/.zeric/.zgit/IHS/zsh/setup/zshrc/studio.zshrc 
		    ) 

  export SAVEHIST=50000

# Alias
  # builtins 
  alias D="cd $HOME/Desktop/"
  alias down="cd $HOME/Downloads"
  alias dv="dirs -v"
  alias zgit="cd $HOME/.zeric/.zgit/"
  alias zfunc="cd $HOME/.zfunc/"
  alias zer="cd $HOME/.zeric/"
  alias config="cd $HOME/.config/"
  alias pyhs="cd $HOME/.zeric/.zgit/pyhs"
  alias pybin="$HOME/.bin/pybin/"
  alias zbin="$HOME/.bin/zbin/"
  alias pgrep="pgrep -li"
  alias -g O="open ."
  # external commands
  alias dmen="open -a dmenu-mac"
  alias imgid="identify"
  # alias htop="sudo htop"
  alias ls="colorls -A --sd"
  alias l="colorls -lA --sd --git-status"
  alias lr="colorls -report"
  alias ltree="colorls --tree"
  alias py3="python3"
  alias py3pyhs="python3 /Users/zeric.chan/.zeric/.zgit/pyhs/pyhs/Menu.py"
  # IHS
  alias brand="open $HOME/Desktop/DOCUMENTS/Brand"
  alias google_ser_ac="print $GOOGLE_SERVICE_AC | pbcopy; print 'Google Service Account copied to the clipboard'"
  alias ihse="ihs_email.py"
  alias imgdrag="mv -i **/*(.) ." 
  alias ppt="open -a 'Microsoft PowerPoint' '$HOME/Desktop/DOCUMENTS/QC/Retouch Note.pptx'"
  alias renamePNG="rename -d ' copy' $HOME/Desktop/EXPORTS/PNG/*"
  alias rl_check="time rl_check"
  alias ser="cd /Volumes/Studio/CLIENTS"
  alias tbq="cd $HOME/Desktop/To Be QC"
  alias TSF="ToSendFolder"
  alias xl="open -a 'Microsoft Excel' '/Users/zeric.chan/Desktop/DOCUMENTS/QC/finder_search.xlsx'"
  # misc
  alias showargs="printf '>>>%s<<<\n'"

# Startup commands
  clear  
  neofetch
  # cowsay -f dragon 'Roar!! I don''t want OT!!'
  # File management
    mv -i $HOME/Desktop/RL/Sending/sent* $HOME/Desktop/RL/Sent
    rm $HOME/Desktop/**/Thumbs.db

# Sourcing programs
  source $(brew --prefix)/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  source $(brew --prefix)/share/zsh-autosuggestions/zsh-autosuggestions.zsh
  source /Users/zeric.chan/.config/broot/launcher/bash/br

# config
  # run-help for builtin commands
  # copy the help files to a directory of your choice first
    typeset -U HELPDIR="$HOME/.zsh_help"
    unalias run-help
    autoload run-help

  # zsh-syntax-highlighting config
    ZSH_HIGHLIGHT_HIGHLIGHTERS=( main brackets )
    ZSH_HIGHLIGHT_STYLES[command]='fg=blue,bold'
    ZSH_HIGHLIGHT_STYLES[builtin]='fg=blue,bold'
    ZSH_HIGHLIGHT_STYLES[alias]='fg=blue,bold'
    ZSH_HIGHLIGHT_STYLES[function]='fg=magenta,blod'
    ZSH_HIGHLIGHT_STYLES[path]='fg=yellow,blod'
    ZSH_HIGHLIGHT_STYLES[history-expansion]='fg=blue,bg=yellow,blod'

  # zsh-autosuggestions config
    ZSH_AUTOSUGGEST_STRATEGY=( history completion )

  # agnoster.zsh-theme setup
    customize_agnoster() {
  	prompt_segment 'red' '' '%{\e[33m%}%B\uf12a %!%b%{\e[0m%}'
    }
    AGNOSTER_PROMPT_SEGMENTS=("customize_agnoster" "${AGNOSTER_PROMPT_SEGMENTS[@]}")

#}}}
#=================================================================
