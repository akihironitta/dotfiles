alias reload="source ~/.zshrc"
alias jn="jupyter notebook ~ &"
# alias slack="slack >/dev/null 2>/dev/null &"
# alias discord="discord >/dev/null 2>/dev/null &"
# alias firefox="firefox >/dev/null 2>/dev/null &"
alias emcas="emacs"

if [ "$(uname)" = "Darwin" ]; then
    alias la="ls -aGF"
    alias ls="ls -GF"
    alias ll="ls -lGF"
    alias lg="ls -l -gGF"
    alias mupdf="mupdf-gl"
    alias cvlc="vlc -I dummy"

elif [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
    alias exa="exa-linux-x86_64"
    alias ls="ls --color --classify"
    alias la="ls --color --classify -a"
    alias ll="ls --color --classify -h -l"
    alias lg="ls --color --classify -h -l -g"
    alias chrome="google-chrome"

    ca() {
        conda activate $1
        conda deactivate
        conda deactivate
        conda activate $1
    }

else
    echo "Skipping 10-alias.zsh"
fi
