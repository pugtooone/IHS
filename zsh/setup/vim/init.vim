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
" snippet engine
Plug 'SirVer/ultisnips'
Plug 'quangnguyen30192/cmp-nvim-ultisnips'
" autopair brackets and quotes
Plug 'jiangmiao/auto-pairs'

" files searching 
Plug 'kyazdani42/nvim-web-devicons' " for file icons
Plug 'nvim-telescope/telescope.nvim'
Plug 'nvim-lua/plenary.nvim' "dependency for telescope

call plug#end()

"}}}

"Setup & Config {{{

" nvim-cmp setup
set completeopt=menu,menuone,noselect

lua <<EOF
  -- Setup nvim-cmp.
  local cmp = require'cmp'

  cmp.setup({
    snippet = {
      expand = function(args)
        vim.fn["UltiSnips#Anon"](args.body) -- enable ultisnips
      end,
    },
    window = {
       completion = cmp.config.window.bordered(),
       documentation = cmp.config.window.bordered(),
    },
    mapping = cmp.mapping.preset.insert({
      ['<C-b>'] = cmp.mapping.scroll_docs(-4),
      ['<C-f>'] = cmp.mapping.scroll_docs(4),
      ['<C-Space>'] = cmp.mapping.complete(),
      ['<C-e>'] = cmp.mapping.abort(),
      ['<CR>'] = cmp.mapping.confirm({ select = true }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
    }),
    sources = cmp.config.sources({
      { name = 'nvim_lsp' },
      { name = 'ultisnips' }, -- sourcing ultisnips
    }, {
      { name = 'buffer' },
    })
  })

  -- Set configuration for specific filetype.
  -- cmp.setup.filetype('gitcommit', {
  --  sources = cmp.config.sources({
  --    { name = 'cmp_git' }, -- You can specify the `cmp_git` source if you were installed it.
  --  }, {
  --    { name = 'buffer' },
  --  })
  --})

  -- Use buffer source for `/` (if you enabled `native_menu`, this won't work anymore).
  cmp.setup.cmdline('/', {
    mapping = cmp.mapping.preset.cmdline(),
    sources = {
      { name = 'buffer' }
    }
  })

  -- Use cmdline & path source for ':' (if you enabled `native_menu`, this won't work anymore).
  cmp.setup.cmdline(':', {
    mapping = cmp.mapping.preset.cmdline(),
    sources = cmp.config.sources({
      { name = 'path' }
    }, {
      { name = 'cmdline' }
    })
  })

  -- Setup lspconfig.
  -- local capabilities = require('cmp_nvim_lsp').update_capabilities(vim.lsp.protocol.make_client_capabilities())
  -- Replace <YOUR_LSP_SERVER> with each lsp server you've enabled.
  --require('lspconfig')[''].setup {
  --  capabilities = capabilities
  --}
  
  -- cmp-zsh plugin setup 
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
