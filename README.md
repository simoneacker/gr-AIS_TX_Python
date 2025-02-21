# gr-AIS_TX_Python
A python AIS frame generator plugin for GNU Radio. Offers a source block which accepts a comma-delimited 168-character binary payload string (ex. 01010101...,0101010101...). The block cycles through the list of payloads, inserting each payload into a full 256 bit AIS frame (as defined by ITU-R M.1371-5). Python Time library is used to limit transmit rate to 5 Hz. 

## Dependencies:
- GNU Radio

## Installing the plugin:
```
git clone https://github.com/simoneacker/gr-AIS_TX_Python.git
cd gr-AIS_TX_Python
mkdir build
cd build
cmake ..
make
sudo make install
```

# Credit
I referenced [Trend Micro C++ AIS Plugin](https://github.com/trendmicro/ais) while working on this.
