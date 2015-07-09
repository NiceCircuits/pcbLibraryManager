# pcbLibraryManager
Manager and generator for pcb libraries. Some day will work with multiple CAD packages (KiCad, Eagle etc.) Written in Python 3.

## Structure:
* generator modules, like *libraryMosfet*. Contains top level code to generate whole libraries. Every generator module contains one class inherited from *libraryManager.library*. Can be executed by itself or from other file. Library is created when new instance of class is created. Library is created in current working directory. Library generator modules can generate needed symbol or footprints or (preferably) use classes defined in *symbols* and *footprints* directories. Parts can be also inherited from classes in *parts* directory.