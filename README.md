# DANASOFT 

DanaSoft is a python interface based on PyQt4. 

![](images/fastmapping_train_fam.png)

## Installation 

1.  If you are using Anaconda create a new environment with python's version 2.7 (in a terminal) :

   ```shell
   conda create -n danasoft_env python=2.7
   activate danasoft_env
   ```

2. Manual install PyQt4 on this environment

3. Install numpy : conda install numpy

4. Download **danasoft** from github :

   ```shell
   git clone https://github.com/tinmarD/DanaSoft
   ```

### Data Directory  : 

The data files are not provided on github to save space. 

You need to set the data directory path in the *config.py* file at line 10 : 

```python
SOFT_NAME = "Dana Soft"
DATA_PATH = r'C:\Path\to\data\directory'
```

### Install 

5. In the terminal, go in the root directory and run the following command :

```shell
python setup.py install
```



## Launch

There are 2 solutions to launch the software : 

1. Open the file danasoft/danasoft.py with python 

   OR

2. If step 5 was completed, you can open the software by calling danasoft in a terminal



