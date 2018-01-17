syntax enable
filetype plugin indent on
autocmd BufEnter * let &titlestring = ' ' . expand("%:t")
set title

set autoindent
set showmatch
set expandtab
set softtabstop=2
set shiftwidth=2

au BufRead,BufNewFile *.sage setfiletype python

autocmd FileType make set noexpandtab softtabstop=0
autocmd FileType text set spell linebreak textwidth=72
autocmd FileType markdown set spell linebreak textwidth=72 softtabstop=4 shiftwi                                                                                        dth=4
autocmd Filetype python set softtabstop=4 shiftwidth=4
autocmd Filetype php set nocindent nosmartindent indentexpr=""
autocmd Filetype php set autoindent
autocmd Filetype tex set nocindent nosmartindent indentexpr=""
autocmd Filetype tex set autoindent spell linebreak textwidth=72
"autocmd FileType cpp\|c\|sh set

highlight clear SpellBad
highlight SpellBad ctermfg=1 cterm=underline
highlight clear SpellCap
highlight SpellCap ctermfg=4 cterm=underline

set pastetoggle=<F2>
" F8 turns off smart indenting in an emergency
:nnoremap <F8> :setl nocin nosi inde=<CR>

autocmd Filetype java set makeprg=javac\ %
set errorformat=%A%f:%l:\ %m,%-Z%p^,%-C%.%#
map <F9> :make<Return>:copen<Return>
map <F10> :cprevious<Return>
map <F11> :cnext<Return>


