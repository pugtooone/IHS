"Options {{{

set number
set autoindent
set hlsearch
set incsearch
syntax enable

"}}}

"Plugins {{{

call plug#begin()

" Visual
" syntax highlight
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
" statusline setup
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
" indent blankline (not for vim)
Plug 'lukas-reineke/indent-blankline.nvim'
" icon
Plug 'ryanoasis/vim-devicons'

" Editing
" completions
Plug 'hrsh7th/nvim-cmp'
Plug 'tamago324/cmp-zsh'
Plug 'Shougo/deol.nvim'
" autopair brackets and quotes
Plug 'jiangmiao/auto-pairs'

" Searching 
Plug 'kyazdani42/nvim-web-devicons' " for file icons
Plug 'kyazdani42/nvim-tree.lua'
Plug 'nvim-lua/plenary.nvim' "dependency for telescope
Plug 'nvim-telescope/telescope.nvim'

call plug#end()

"}}}

"Setup & Config {{{

" cmp-zsh plugin setup 
lua << EOF
require'cmp'.setup {
  -- ...
  sources = {
    { name = 'zsh' }
  }
}
EOF

" vim-airline config
let g:airline#extensions#tabline#enabled = 1 "enable tab line
let g:airline#extensions#tabline#left_sep = ' ' "tab line separator
let g:airline#extensions#tabline#left_alt_sep = '|'
let g:airline_powerline_fonts = 1 " enable powerline fonts

"}}}

" vim: foldmethod=marker foldlevel=0 :
