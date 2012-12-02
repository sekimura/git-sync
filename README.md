git-sync: a simple tool to mirror git repositories
==================================================

git-sync.py -d /var/local/git-mirror/ https://github.com/sekimura/dotfiles

# checkout from synced repo for readonly purpose.

    git clone --local --shared \
        /var/local/git-mirror/github.com/sekimura/dotfiles \
        dotfiles-readonly

# working repo to commit upstream

    git clone --reference \
        /var/local/git-mirror/github.com/sekimura/dotfiles \
        git@github.com:sekimura/text-markdown-discount.git dotfiles

