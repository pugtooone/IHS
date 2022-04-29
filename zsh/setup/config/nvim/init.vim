"Options {{{

set autoindent
set history=500
set hlsearch
set incsearch
set nocompatible 
set number
set smartcase

filetype on

syntax enable

"}}}

"Key Mappings {{{

let mapleader = "\\"
nnoremap <space> :
nnoremap <leader>tl <cmd>Telescope find_files<cr>
nnoremap <leader>to <cmd>Telescope oldfiles<cr>
nnoremap <leader>tb <cmd>Telescope buffers<cr>

"}}}

"Plugins {{{

call plug#begin()

"Visual
" syntax highlight
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
" statusline setup
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
" indent blankline
Plug 'lukas-reineke/indent-blankline.nvim'
" icon
Plug 'ryanoasis/vim-devicons'

"Editing
" completions
Plug 'neovim/nvim-lspconfig'
Plug 'hrsh7th/cmp-nvim-lsp'
Plug 'hrsh7th/cmp-buffer'
Plug 'hrsh7th/cmp-path'
Plug 'hrsh7th/cmp-cmdline'
Plug 'hrsh7th/nvim-cmp'
Plug 'tamago324/cmp-zsh'
Plug 'Shougo/deol.nvim'
" autopair brackets and quotes
Plug 'jiangmiao/auto-pairs'

" files searching 
Plug 'kyazdani42/nvim-web-devicons' " for file icons
Plug 'nvim-telescope/telescope.nvim'
Plug 'nvim-lua/plenary.nvim' "dependency for telescope

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
