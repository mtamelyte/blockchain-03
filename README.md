# Libbitcoin setup and testing using Windows Subsystem for Linux
## Setting up libbitcoin

1. If you don't already have it, install WSL in Powershell.
````
wsl --install
````
2. Install dependencies.
```
sudo apt install -y build-essential autoconf automake libtool pkg-config git
sudo apt install -y libboost-all-dev libssl-dev
```
3. Install Boost 1.65 (current versions will not work with the required version of libbitcoin).
````
cd ~
wget https://sourceforge.net/projects/boost/files/boost/1.65.1/boost_1_65_1.tar.gz/download -O boost_1_65_1.tar.gz

tar -xzf boost_1_65_1.tar.gz
cd boost_1_65_1

./bootstrap.sh --prefix=/usr/local/boost-1.65
sudo ./b2 install

sudo ldconfig
````
4. Install an older version of libsecp256k1
````
cd ~
git clone https://github.com/bitcoin-core/secp256k1.git
cd secp256k1
git checkout 1e6f1f5ad5e7f1e3ef79313ec02023902bf8175c

./autogen.sh
./configure --prefix=/usr/local --enable-module-recovery
make
sudo make install
sudo ldconfig
````
5. Install libbitcoin library v3 (parts of the code are deprecated and will not run with the current version).
```
git clone https://github.com/libbitcoin/libbitcoin-system.git libbitcoin-v3

cd libbitcoin-v3
git checkout v3.5.0

./autogen.sh

export BOOST_ROOT=/usr/local/boost-1.65
export BOOST_INCLUDEDIR=/usr/local/boost-1.65/include  
export BOOST_LIBRARYDIR=/usr/local/boost-1.65/lib

./configure --prefix=/usr/local \
    --with-boost=/usr/local/boost-1.65

make
sudo make install
sudo ldconfig
```
6. Manually patch an outdated file to have the right dependencies - run this command and add ````#include <cstddef>````  next to all the other dependencies, then save with Ctrl+X, Y, Enter.
````
nano include/bitcoin/bitcoin/wallet/dictionary.hpp
````
7. Patch another outdated file - delete the ````override```` keyword in line 71.
````
nano include/bitcoin/bitcoin/log/file_collector.hpp
````
8. Reinstall headers with the patches.
````
sudo rm -rf /usr/local/include/bitcoin
sudo make install
sudo ldconfig
````
9. Finally, clone this directory and run ```make```.
10. To run the program, run ```./main```.