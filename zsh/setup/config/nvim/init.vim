
" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
"  ███████╗███████╗██████╗ ██╗ ██████╗    ███╗   ██╗██╗   ██╗██╗███╗   ███╗ "
"  ╚══███╔╝██╔════╝██╔══██╗██║██╔════╝    ████╗  ██║██║   ██║██║████╗ ████║ "
"    ███╔╝ █████╗  ██████╔╝██║██║         ██╔██╗ ██║██║   ██║██║██╔████╔██║ "
"   ███╔╝  ██╔══╝  ██╔══██╗██║██║         ██║╚██╗██║╚██╗ ██╔╝██║██║╚██╔╝██║ "
"  ███████╗███████╗██║  ██║██║╚██████╗    ██║ ╚████║ ╚████╔╝ ██║██║ ╚═╝ ██║ "
"  ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝    ╚═╝  ╚═══╝  ╚═══╝  ╚═╝╚═╝     ╚═╝ "
" " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " " "
                                                                        
"================================================================================
"Options & Variables{{{
"================================================================================

" vim options
set autoindent
set history=500
set hlsearch
set incsearch
set nocompatible 
set number
set smartcase
set splitbelow splitright

" filetype on
syntax enable

" variables
let NVIM_INIT = "/Users/zericchan/.config/nvim"

"}}}
"================================================================================

"================================================================================
"Key Mappings {{{
"================================================================================

let mapleader = "\\"
nnoremap <space> :
" navigate between splits
nnoremap <C-h> <C-w><C-h>
nnoremap <C-j> <C-w><C-j>
nnoremap <C-k> <C-w><C-k>
nnoremap <C-l> <C-w><C-l>
" Telescope
nnoremap <leader>tl <cmd>Telescope find_files<cr>
nnoremap <leader>to <cmd>Telescope oldfiles<cr>
nnoremap <leader>tb <cmd>Telescope buffers<cr>
" NERDTree
nnoremap <C-n> :NERDTree<CR>

"}}}
"================================================================================

"================================================================================
"Plugins {{{
"================================================================================

call plug#begin()

"Visual
" syntax highlighting
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'}
Plug 'tiagofumo/vim-nerdtree-syntax-highlight' " NERDTree syntax highlighting
Plug 'Xuyuanp/nerdtree-git-plugin' "NERDTree git status flags
"statusline
Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'
" icon
Plug 'ryanoasis/vim-devicons'
" indent-blankline
Plug 'lukas-reineke/indent-blankline.nvim'

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
Plug 'L3MON4D3/LuaSnip'
Plug 'saadparwaiz1/cmp_luasnip'
"Plug 'rafamadriz/friendly-snippets'
"autopairs
Plug 'jiangmiao/auto-pairs'

" files searching 
Plug 'preservim/nerdtree' "file system explorer
Plug 'nvim-telescope/telescope.nvim' "fuzzy finder
Plug 'nvim-lua/plenary.nvim' "dependency for telescope

call plug#end()

"}}}
"================================================================================

"================================================================================
"Setup & Config {{{ 
"================================================================================

" colorscheme
  colorscheme pablo

" auto-pairs config

" vim-airline config
  let g:airline_theme = 'cool'
  let g:airline#extensions#tabline#enabled = 1 "enable tab line
  let g:airline#extensions#tabline#left_sep = ' ' "tab line separator
  let g:airline#extensions#tabline#left_alt_sep = '|'
  let g:airline_powerline_fonts = 1 " enable powerline fonts

" NERDTree config
  " NERDTree settings
    let NERDTreeSortHiddenFirst = 1
    let NERDTreeShowHidden = 1
    let NERDTreeShowLineNumbers = 1
  " Exit Vim if NERDTree is the only window remaining in the only tab.
    autocmd BufEnter * if tabpagenr('$') == 1 && winnr('$') == 1 && exists('b:NERDTree') && b:NERDTree.isTabTree() | quit | endif
  " Start NERDTree when Vim is started without file arguments.
    autocmd StdinReadPre * let s:std_in=1
    autocmd VimEnter * if argc() == 0 && !exists('s:std_in') | NERDTree | endif

" nvim-cmp setup
set completeopt=menu,menuone,noselect

lua <<EOF
  -- Setup nvim-cmp.
  local cmp = require'cmp'

  local kind_icons = {
  Text = "",
  Method = "m",
  Function = "",
  Constructor = "",
  Field = "",
  Variable = "",
  Class = "",
  Interface = "",
  Module = "",
  Property = "",
  Unit = "",
  Value = "",
  Enum = "",
  Keyword = "",
  Snippet = "",
  Color = "",
  File = "",
  Reference = "",
  Folder = "",
  EnumMember = "",
  Constant = "",
  Struct = "",
  Event = "",
  Operator = "",
  TypeParameter = "",
}

  cmp.setup({
    snippet = {
      expand = function(args)
         require('luasnip').lsp_expand(args.body) -- For `luasnip` users.
      end,
    },
    window = {
       completion = cmp.config.window.bordered(),
       documentation = cmp.config.window.bordered(),
    },
    mapping = cmp.mapping.preset.insert({
      --["<C-k>"] = cmp.mapping.select_prev_item(),
      --["<C-j>"] = cmp.mapping.select_next_item(),
      ['<C-b>'] = cmp.mapping.scroll_docs(-4),
      ['<C-f>'] = cmp.mapping.scroll_docs(4),
      ['<C-Space>'] = cmp.mapping.complete(),
      ['<C-e>'] = cmp.mapping.abort(),
      ['<CR>'] = cmp.mapping.confirm({ select = true }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
      ["<Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
              cmp.select_next_item()
            elseif luasnip.expandable() then
              luasnip.expand()
            elseif luasnip.expand_or_jumpable() then
              luasnip.expand_or_jump()
            elseif check_backspace() then
              fallback()
            else
              fallback()
            end
          end, {
            "i",
            "s",
          }),
      ["<S-Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
              cmp.select_prev_item()
            elseif luasnip.jumpable(-1) then
              luasnip.jump(-1)
            else
              fallback()
            end
          end, {
            "i",
            "s",
          }),
    }),

  --completion menu box formatting by Neovim-from-scratch
  formatting = {
     fields = { "kind", "abbr", "menu" },
     format = function(entry, vim_item)
       -- Kind icons
       vim_item.kind = string.format("%s", kind_icons[vim_item.kind])
       vim_item.menu = ({
         nvim_lsp = "[LSP]",
         luasnip = "[Snippet]",
         buffer = "[Buffer]",
         path = "[Path]",
	 zsh = "[ZSH]",
       })[entry.source.name]
       return vim_item
     end,
    },

    sources = cmp.config.sources({
      { name = 'nvim_lsp' },
      { name = 'luasnip' },
      { name = 'zsh' },
      { name = 'path' },
    }, {
      { name = 'buffer' },
    }),

    cmp.setup {
      window = {
        documentation = cmp.config.window.bordered(),
      },
    }
  })

  --[[ Set configuration for specific filetype.
  cmp.setup.filetype('gitcommit', {
    sources = cmp.config.sources({
      { name = 'cmp_git' }, -- You can specify the `cmp_git` source if you were installed it.
    }, {
      { name = 'buffer' },
    })
  })
  ]]--

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

--[[
  -- Setup lspconfig.
  local capabilities = require('cmp_nvim_lsp').update_capabilities(vim.lsp.protocol.make_client_capabilities())
  -- Replace <YOUR_LSP_SERVER> with each lsp server you've enabled.
  require('lspconfig')['<YOUR_LSP_SERVER>'].setup {
    capabilities = capabilities
  }
]]--

EOF

"}}}
"================================================================================
" vim: foldmethod=marker foldlevel=0 :
