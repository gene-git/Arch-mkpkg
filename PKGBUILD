#
# Sample PKGBUILD to build mkpkg from git HEAD  
#
# Build :
#   mkdir src ; cd src
#   git clone https://github.com/gene-git/Arch-mkpkg
#   cd .. ; makepkg   
#
# Maintainer: Gene C <arch@sapience.com>
# Contributor: 
# 
pkgname='mkpkg'
pkgdesc='Tool to enhance package building (git)'
_gitname='Arch-mkpkg'
_branch='master'

pkgver=2.1.0.r5.g1f87990
pkgrel=1

url="https://github.com/gene-git/Arch-mkpkg"

arch=(any)
license=(MIT)
depends=('python')
makedepends=()
_mkpkg_depends=('python>minor')

source=()

pkgver() {
    cd "${srcdir}/${_gitname}"
    git describe --tags --long | sed -E 's/^v//;s/([^-]*-g)/r\1/;s/-/./g' 
}

prepare() {
    cd "${srcdir}/${_gitname}"
    git fetch
    git clean -f
    git pull origin $_branch
}

build() {
    cd ${srcdir}/${_gitname}
    poetry build
}

package() {
    cd "${srcdir}/${_gitname}"
    ./do-install ${pkgdir}
}
# vim:set ts=4 sts=4 sw=4 et:
