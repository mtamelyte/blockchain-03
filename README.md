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
## Testavimas su duotais hash'ais
Paleidus kodą kaip yra, Merkle Root Hash buvo neteisingas ir nesutapo su Merkle Root Hash iš 100000 bloko, bet pakeitus į encode_base16 į encode_hash, gautas teisingas rezultatas.
<img width="1205" height="536" alt="Screenshot 2025-11-26 164656" src="https://github.com/user-attachments/assets/58c58681-1a26-43eb-8db5-3cba96d2045f" />

<img width="978" height="285" alt="Screenshot 2025-11-25 225304" src="https://github.com/user-attachments/assets/96b759aa-8387-4f98-bfb5-1ffd443bccf2" />

<img width="969" height="248" alt="Screenshot 2025-11-26 164648" src="https://github.com/user-attachments/assets/8c45594d-013c-4a7c-8478-2a42534e90f4" />

## Testavimas su kitais hash'ais
Pasirinktas 150001-asis Bitcoin blokas, kuriame buvo įtraukta 10 tranzakcijų, ir jų hash'ai sudėti į programą vietoj testinių pavyzdžių.

<img width="1221" height="542" alt="Screenshot 2025-11-26 164042" src="https://github.com/user-attachments/assets/3a65c35d-2d9b-439c-adba-4a08a653ff55" />
<img width="980" height="522" alt="Screenshot 2025-11-26 164035" src="https://github.com/user-attachments/assets/6022ef28-a398-43dc-a222-c672301aea0d" />
