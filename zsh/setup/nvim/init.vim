set number

call plug#begin()

" Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'hrsh7th/nvim-cmp'
Plug 'tamago324/cmp-zsh'
Plug 'Shougo/deol.nvim'

call plug#end()

" cmp-zsh plugin setup
lua << EOF
require'cmp'.setup {
  -- ...
  sources = {
    { name = 'zsh' }
  }
}
EOF
