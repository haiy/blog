---
title: 家用ubuntu服务器常用管理
layout: post
---

## {{page.title}}

<p class="meta">04 Aug 2018</p>

Table of Contents
=================
  
* [1 ubuntu网络配置](#1-ubuntu网络配置)
    * [命令行管理网络信息](#命令行管理网络信息)
    * [界面网络管理工具](#界面网络管理工具)
 * [2 apt源，pip源，conda源配置](#2-apt源pip源conda源配置)
 * [分屏管理tmux](#分屏管理tmux)
 * [3 vim编辑器简单配置](#3-vim编辑器简单配置)
    * [配置](#配置)
    * [快捷键](#快捷键)
 * [4 语言编码和时间配置](#4-语言编码和时间配置)
 * [5 配置不同版本的gcc](#5-配置不同版本的gcc)
 * [6 git proxy配置](#6-git-proxy配置)
 * [7 ngrok server配置](#7-ngrok-server配置)
 * [8 如何添加一个自定义启动service](#8-如何添加一个自定义启动service)
 * [9 配置默认编辑器](#9-配置默认编辑器)
 * [10 nginx配置支持websocket代理,端口映射](#10-nginx配置支持websocket代理端口映射)
 * [Refs](#refs)


### 1 ubuntu网络配置

如果是server版的ubuntu，需要检查下nm(network manager)有没有正常。
默认情况是使用配置文件来管理网络的。

#### 命令行管理网络信息

```
# 查看所有网络设备信息
ifconfig
docker0   Link encap:Ethernet  HWaddr 02:42:01:1c:a2:d9  
          inet addr:172.17.0.1  Bcast:0.0.0.0  Mask:255.255.0.0
          UP BROADCAST MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

enp0s31f6 Link encap:Ethernet  HWaddr 34:97:f6:87:bc:f0  
          inet addr:192.168.1.106  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::98e6:5e44:fb4d:8949/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:5308 errors:0 dropped:0 overruns:0 frame:0
          TX packets:5483 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:4761657 (4.7 MB)  TX bytes:752189 (752.1 KB)
          Interrupt:16 Memory:df200000-df220000 

# 重启当前使用的网络设备
sudo ifdown enp0s31f6
sudo ifup enp0s31f6

# 命令行修改网络配置
sudo vim /etc/network/interfaces
 source /etc/network/interfaces.d/*
 
# The loopback network interface
auto lo
iface lo inet loopback
 
auto enp0s31f6
# 如果需要dhcp方式，直接将static修改为dhcp，删掉下面的address,netmask,gateway配置
iface enp0s31f6 inet static
address 192.168.1.106
netmask 255.255.255.0
gateway 192.168.1.1

```

#### 界面网络管理工具

```
# 先安装网络管理工具
sudo apt-get install network-manager

# 检查界面工具是否接管了网络管理
# 确保第6行managed为true
sudo vim /etc/NetworkManager/NetworkManager.conf 
1 [main]
2 plugins=ifupdown,keyfile,ofono
3 dns=dnsmasq
4 
5 [ifupdown]
6 managed=true

# 重启网络服务
sudo reboot
```

### 2 apt源，pip源，conda源配置

- apt源

```
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
sudo vim /et/apt/sources.list

# ubuntu 16.04粘贴下面的

deb http://mirrors.aliyun.com/ubuntu/ xenial main
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main

deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main

deb http://mirrors.aliyun.com/ubuntu/ xenial universe
deb-src http://mirrors.aliyun.com/ubuntu/ xenial universe
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates universe

deb http://mirrors.aliyun.com/ubuntu/ xenial-security main
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main
deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security universe
```

- pip源

```
mkdir -p ~/.pip
vim ~/.pip/pip.conf

# copy and paste 
[global]
index-url=http://pypi.douban.com/simple
trusted-host = pypi.douban.com 
```

- conda环境以及源

下载conda：

```
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-4.4.10-Linux-x86_64.sh
```

安装配置:

```
# 配置环境变量
export CONDA_HOME=/opt/conda  
export PATH=$PATH:/opt/conda/bin


mv Miniconda3-4.4.10-Linux-x86_64.sh miniconda.sh

# 安装到/opt/conda
./miniconda.sh -b -p /opt/conda 

# 配置mirror
conda config --set show_channel_urls yes && \
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ && \
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ && \
conda config --remove channels defaults && \
conda config --system --set auto_update_conda false && \

# 创建一个py35环境
conda create -p $CONDA_HOME/envs/py35 python=3.5 

# 使用这个py35环境

source activate py35
```

### 分屏管理tmux

安装及简单配置

```
# ubuntu 
sudo apt-get install tmux

# mac
brew install tmux

# short alias 
alias tl='tmux list-sessions'
alias ta='tmux attach -t' 
alias td='tmux attach -d -t' 
alias tn='tmux new-session -s'

```

### 3 vim编辑器简单配置

#### 配置
```
set nu
execute pathogen#infect()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => General
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Sets how many lines of history VIM has to remember
set history=700

" Enable filetype plugins
filetype plugin on
filetype indent on

" Set to auto read when a file is changed from the outside
set autoread

" With a map leader it's possible to do extra key combinations
" like <leader>w saves the current file
let mapleader = ","
let g:mapleader = ","

" Fast saving
nmap <leader>w :w!<cr>

" :W sudo saves the file 
" (useful for handling the permission-denied error)
command W w !sudo tee % > /dev/null


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => VIM user interface
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Set 7 lines to the cursor - when moving vertically using j/k
set so=7

" Turn on the WiLd menu
set wildmenu

" Ignore compiled files
set wildignore=*.o,*~,*.pyc
if has("win16") || has("win32")
    set wildignore+=*/.git/*,*/.hg/*,*/.svn/*,*/.DS_Store
else
    set wildignore+=.git\*,.hg\*,.svn\*
endif

"Always show current position
set ruler

" Height of the command bar
set cmdheight=2

" A buffer becomes hidden when it is abandoned
set hid

" Configure backspace so it acts as it should act
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

" Ignore case when searching
set ignorecase

" When searching try to be smart about cases 
set smartcase

" Highlight search results
set hlsearch

" Makes search act like search in modern browsers
set incsearch 

" Don't redraw while executing macros (good performance config)
set lazyredraw 

" For regular expressions turn magic on
set magic

" Show matching brackets when text indicator is over them
set showmatch 
" How many tenths of a second to blink when matching brackets
set mat=2

" No annoying sound on errors
set noerrorbells
set novisualbell
set t_vb=
set tm=500

" Add a bit extra margin to the left
set foldcolumn=1
set fdm=indent


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Colors and Fonts
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Enable syntax highlighting
syntax enable 

try
    colorscheme desert
catch
endtry

set background=dark

" Set extra options when running in GUI mode
if has("gui_running")
    set guioptions-=T
    set guioptions-=e
    set t_Co=256
    set guitablabel=%M\ %t
endif

" Set utf8 as standard encoding and en_US as the standard language
set encoding=utf8

" Use Unix as the standard file type
set ffs=unix,dos,mac


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Files, backups and undo
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Turn backup off, since most stuff is in SVN, git et.c anyway...
set nobackup
set nowb
set noswapfile


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Text, tab and indent related
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Use spaces instead of tabs
set expandtab

" Be smart when using tabs ;)
set smarttab

" 1 tab == 4 spaces
set shiftwidth=4
set tabstop=4

" Linebreak on 500 characters
set lbr
set tw=500

set ai "Auto indent
set si "Smart indent
set wrap "Wrap lines





"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Moving around, tabs, windows and buffers
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Treat long lines as break lines (useful when moving around in them)
map j gj
map k gk

" Map <Space> to / (search) and Ctrl-<Space> to ? (backwards search)
map <space> /
map <c-space> ?

" Disable highlight when <leader><cr> is pressed
map <silent> <leader><cr> :noh<cr>

" Smart way to move between windows
map <C-j> <C-W>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" Close the current buffer
map <leader>bd :Bclose<cr>

" Close all the buffers
map <leader>ba :1,1000 bd!<cr>

" Useful mappings for managing tabs
map <leader>tn :tabnew<cr>
map <leader>to :tabonly<cr>
map <leader>tc :tabclose<cr>
map <leader>tm :tabmove 
map <leader>t<leader> :tabnext 

" Opens a new tab with the current buffer's path
" Super useful when editing files in the same directory
map <leader>te :tabedit <c-r>=expand("%:p:h")<cr>/

" Switch CWD to the directory of the open buffer
map <leader>cd :cd %:p:h<cr>:pwd<cr>

" Specify the behavior when switching between buffers 
try
  set switchbuf=useopen,usetab,newtab
  set stal=2
catch
endtry

" Return to last edit position when opening files (You want this!)
autocmd BufReadPost *
     \ if line("'\"") > 0 && line("'\"") <= line("$") |
     \   exe "normal! g`\"" |
     \ endif
" Remember info about open buffers on close
set viminfo^=%


""""""""""""""""""""""""""""""
" => Status line
""""""""""""""""""""""""""""""
" Always show the status line
set laststatus=2

" Format the status line
set statusline=\ %{HasPaste()}%F%m%r%h\ %w\ \ CWD:\ %r%{getcwd()}%h\ \ \ Line:\ %l


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Editing mappings
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Remap VIM 0 to first non-blank character
map 0 ^


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Ack searching and cope displaying
"    requires ack.vim - it's much better than vimgrep/grep
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" When you press gv you Ack after the selected text
vnoremap <silent> gv :call VisualSelection('gv', '')<CR>

" Open Ack and put the cursor in the right position
map <leader>g :Ack 

" When you press <leader>r you can search and replace the selected text
vnoremap <silent> <leader>r :call VisualSelection('replace', '')<CR>

" Do :help cope if you are unsure what cope is. It's super useful!
"
" When you search with Ack, display your results in cope by doing:
"   <leader>cc
"
" To go to the next search result do:
"   <leader>n
"
" To go to the previous search results do:
"   <leader>p
"
map <leader>cc :botright cope<cr>
map <leader>co ggVGy:tabnew<cr>:set syntax=qf<cr>pgg
map <leader>n :cn<cr>
map <leader>p :cp<cr>


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Spell checking
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Pressing ,ss will toggle and untoggle spell checking
map <leader>ss :setlocal spell!<cr>

" Shortcuts using <leader>
map <leader>sn ]s
map <leader>sp [s
map <leader>sa zg
map <leader>s? z=


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Misc
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Remove the Windows ^M - when the encodings gets messed up
"noremap <Leader>m mmHmt:%s/<C-V><cr>//ge<cr>'tzt'm

" Quickly open a buffer for scribble
map <leader>q :e ~/buffer<cr>

" Quickly open a markdown buffer for scribble
map <leader>x :e ~/buffer.md<cr>

" Toggle paste mode on and off
map <leader>pp :setlocal paste!<cr>


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" => Helper functions
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
function! CmdLine(str)
    exe "menu Foo.Bar :" . a:str
    emenu Foo.Bar
    unmenu Foo
endfunction 

function! VisualSelection(direction, extra_filter) range
    let l:saved_reg = @"
    execute "normal! vgvy"

    let l:pattern = escape(@", '\\/.*$^~[]')
    let l:pattern = substitute(l:pattern, "\n$", "", "")

    if a:direction == 'b'
        execute "normal ?" . l:pattern . "^M"
    elseif a:direction == 'gv'
        call CmdLine("Ack \"" . l:pattern . "\" " )
    elseif a:direction == 'replace'
        call CmdLine("%s" . '/'. l:pattern . '/')
    elseif a:direction == 'f'
        execute "normal /" . l:pattern . "^M"
    endif

    let @/ = l:pattern
    let @" = l:saved_reg
endfunction


" Returns true if paste mode is enabled
function! HasPaste()
    if &paste
        return 'PASTE MODE  '
    en
    return ''
endfunction

" Don't close window, when deleting a buffer
command! Bclose call <SID>BufcloseCloseIt()
function! <SID>BufcloseCloseIt()
   let l:currentBufNum = bufnr("%")
   let l:alternateBufNum = bufnr("#")

   if buflisted(l:alternateBufNum)
     buffer #
   else
     bnext
   endif

   if bufnr("%") == l:currentBufNum
     new
   endif

   if buflisted(l:currentBufNum)
     execute("bdelete! ".l:currentBufNum)
   endif
endfunction
```

#### 快捷键

```
Movement

h …move left
l …move right
k …move up
j …move down

line move 

0 …first column of the line
^ …first non-blank character of the line
w …jump to next word
W …jump to next word, ignore punctuation
e …jump to word-end
E …jump to word-end, ignore punctuation
b …jump to word-beginning
B …jump to word-beginning, ignore punctuation
ge …jump to previous word-ending
gE …jump to previous word-ending, ignore punctuation
g_ …jump to last non-blank character of the line
$ …jump to the last character of the line

Editing

d …delete the characters from the cursor position up the position given by the next command (for example d$ deletes all character from the current cursor position up to the last column of the line).
c …change the character from the cursor position up to the position indicated by the next command.
x …delete the character under the cursor.
X …delete the character before the cursor (Backspace).
y …copy the characters from the current cursor position up to the position indicated by the next command.
p …paste previous deleted or yanked (copied) text after the current cursor position.
P …paste previous deleted or yanked (copied) text before the current cursor position.
r …replace the current character with the newly typed one.
s …substitute the text from the current cursor position up to the position given by the next command with the newly typed one.
. …repeat the last insertion or editing command (x,d,p…).


```

- [vim keyboard shortcuts](https://haihome.top/vim)
- [basic tutorials](https://medium.freecodecamp.org/learn-linux-vim-basic-features-19134461ab85)

### 4 语言编码和时间配置

```
sudo apt-get install git vim tmux bzip2 tzdata locales

sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen
locale-gen

# time
ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
dpkg-reconfigure -f noninteractive tzdata
```

### 5 配置不同版本的gcc

不同版本的gcc编译产生的bin在使用so的时候有可能有一定的兼容性问题，所以需要找对版本

以gcc4.8为例，比较粗暴的方法,


**方法一**

```
apt-get install -y cmake gcc-4.8 g++-4.8 cpp-4.8
cd /usr/bin
rm gcc g++ cpp
ln -s gcc-4.8 gcc
ln -s g++-4.8 g++
ln -s cpp-4.8 cpp
```

**方法二**

```
sudo apt-get install gcc-4.9 gcc-4.9 g++-4.9 g++-4.9
gcc --version
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 10
sudo update-alternatives --install /usr/bin/cc cc /usr/bin/gcc 30
sudo update-alternatives --set cc /usr/bin/gcc
sudo update-alternatives --install /usr/bin/c++ c++ /usr/bin/g++ 30
sudo update-alternatives --set c++ /usr/bin/g++
gcc --version
```

### 6 git proxy配置

- git的ssh协议方式的代理

```
# 本地启动了shadowsocks的代理服务，1080端口
vim ~/.ssh/config
Host github.com
    User                    git
    ProxyCommand            nc -x localhost:1080 %h %p
        
```

- git http方式代理

```
# 配置代理 
git config --global http.proxy socks5://localhost:1080

# 取消代理
git config --global --unset http.proxy

```



### 7 ngrok server配置

**内网穿透工具对比**

- frp个人开发，稳定性有待验证，ngrok已经商业化
- ngrok websocket已经支持且能看到每个连接和请求日志
- ngrok 2.X闭源

**编译**

```
cd ngrok
rm -rf device.* rootCA.* linux_amd64/
NGROK_DOMAIN="master.haihome.top"
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -subj "/CN=$NGROK_DOMAIN" -days 5000 -out rootCA.pem
openssl genrsa -out device.key 2048
openssl req -new -key device.key -subj "/CN=$NGROK_DOMAIN" -out device.csr
openssl x509 -req -in device.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device.crt -days 5000
rm -f assets/client/tls/ngrokroot.crt
cp -f rootCA.pem assets/client/tls/ngrokroot.crt
make clean
GOOS="linux" GOARCH="amd64" make release-server
GOOS="linux" GOARCH="amd64" make release-client
GOOS="darwin" GOARCH="amd64" make release-client
GOOS="linux" GOARCH="arm" make release-client
cd ..
rm -rf device.* rootCA.* linux_amd64/
rm -r -f bin/
mkdir -p bin
cp start_*.sh ./bin/
cp -f ngrok/device.* ngrok/rootCA.* ngrok/bin/linux_amd64/* ./bin/
```

- [SELFHOSTING.md](https://github.com/inconshreveable/ngrok/blob/master/docs/SELFHOSTING.md)
- [ngrok/releases](https://github.com/inconshreveable/ngrok/releases)
- [go/wiki](https://github.com/golang/go/wiki/Ubuntu)

### 8 如何添加一个自定义启动service

以ngrok部署为例：

```
# 确认所需可执行文件在
haiy@air:~/settings/ngrok/bin$ ls
deploy_system_service.sh    ngrok* ngrok.service 

# 编写ngrok.service，定义执行环境

[Unit]
Description=ngrok client
After=network.target

[Service]
User=root
TimeoutStartSec=30
ExecStart=/usr/local/bin/ngrok -config /etc/ngrok/ngrok-config -log=/var/log/ngrok.log -subdomain=jupyter start jupyter

[Install]
WantedBy=multi-user.target

# 写一个部署脚本，方便测试,deploy_system_service.sh

cp ngrok /usr/local/bin/ngrok
cp ngrokd /usr/local/bin/ngrokd
mkdir -p /etc/ngrok
cp -f ngrok-config /etc/ngrok/ngrok-config

mkdir -p /usr/lib/systemd/system/

cp -f ngrok.service /usr/lib/systemd/system/

# 启动 frp 并设置开机启动
systemctl enable ngrok
systemctl start ngrok
systemctl status ngrok

# 执行部署
sudo ./deploy_system_service.sh

# 查看service状态
systemctl status ngrok.service
 
# 查看服务日志
journalctl -u ngrok.service
```


### 9 配置默认编辑器

```
sudo update-alternatives --config editor
https://askubuntu.com/questions/13447/how-do-i-change-the-default-text-editor
```

### 10 nginx配置支持websocket代理,端口映射

```
DogKeeper:~/settings# cat /etc/nginx/sites-enabled/my-site.conf 

server {
    listen 443;
    server_name jupyter.com;
    ssl on;
    ssl_certificate /983.pem;
    ssl_certificate_key /83.key;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
    # websocket反向代理支持
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
}

server {
    listen 443;
    
    # 所有子域名映射
    server_name *.master.com;
    ssl on;
    ssl_certificate /559.pem;
    ssl_certificate_key /559.key;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    # 特定端口代理支持
	proxy_set_header Host $http_host:9000;
	proxy_set_header X-NginX-Proxy true;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_read_timeout 86400;
    location / {
        proxy_pass http://127.0.0.1:9000;
    }
}
```



### Refs

- [ubunut nm doc](https://help.ubuntu.com/community/NetworkManager)
- [aliyun mirror](https://opsx.alibaba.com/mirror?lang=zh-cn)
- [http-proxy](https://stackoverflow.com/questions/128035/how-do-i-pull-from-a-git-repository-through-an-http-proxy)
- [sock proxy](http://cms-sw.github.io/tutorial-proxy.html)
- [git-for-the-http-transport](https://stackoverflow.com/questions/15227130/using-a-socks-proxy-with-git-for-the-http-transport)



