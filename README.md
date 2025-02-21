# gr-AIS_TX_Python
A python AIS frame generator plugin for GNU Radio. Offers a source block which accepts a comma-delimited 168-character binary payload string (ex. 01010101...,0101010101...). The block cycles through the list of payloads, inserting each payload into a full 256 bit AIS frame (as defined by ITU-R M.1371-5). Python Time library is used to limit transmit rate to 5 Hz. 

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

## Dependencies:
- GNU Radio

## Notes:
- Project structure is defined by gr_modtool (installed with GNU Radio)
- Important files are AIS_Frame_Generator.py (in python/AIS_TX_Python/) and AIS_TX_Python_AIS_Frame_Generator.block.yml (in grc/). The python file contains the plugin code and the yml file defines the GUI block for gnuradio-companion.

# Credit
I referenced [Trend Micro C++ AIS Plugin](https://github.com/trendmicro/ais) while working on this.
