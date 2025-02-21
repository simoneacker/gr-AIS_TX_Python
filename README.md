# gr-AIS_TX_Python
Python AIS frame generator plugin for GNU Radio. Offers single source block which accepts a comma-delimited 168-character binary payload string (ex. 01010101....,0101010101.....). The block inserts each payload into a full 256 bit AIS frame (as defined by ITU-R M.1371-5). If multiple payloads are provided, they are cycled through one at a time. Python Time library is used to limit transmit to 5 Hz. 

Installing the plugin:
```
git clone https://github.com/simoneacker/gr-AIS_TX_Python.git
cd gr-AIS_TX_Python
mkdir build
cd build
cmake ..
make
sudo make install
```
