# Roadmap of pyheartstudios

Current function will be listed here

<h2>File Management</h1>

1. **setPath()** <br>
The first command to setup the user-defined path for the whole class of function.

```python
from pyheartstudios import FileManagement as fm

fm.setPath('Your destinated path')
```

2. **initialize()**<br>Everything should be started with the setPath() Function to select the destinated path before initializing the directory of file management.<br><br>
The function can create a directory destinated for file management. For example **Batch For Vendor** folder.
```py 
from pyheartstudios import FileManagement as fm

setPath('Your own destinated path')
initialize()
``` 

## Image Check
1. **setImageSpec()**
<br><br>
Initialize the required Image Spec for the class.

```python
from pyheartstudios import ImageCheck as ic

ic.setImageSpec((1200,1200),300,1)
#dimension, ppi, color profile
```

## Future Plan

* ### File Management

    1. Combine **setPath()** function with the **initialize** function to reduce the function redundancy.

    2. More parameter for  **initialize()** function to let users have more choices in setting up their application.

* ### Image Check
    1. Increase the number of parameter to improve flexibility.
