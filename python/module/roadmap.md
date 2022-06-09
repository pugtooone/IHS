# Roadmap of pyheartstudio

Current function will be listed here

<h2>File Management</h1>

1. **setPath()** <br>
The first command to setup the user-defined path for the whole class of function.

```python
setPath('Your destinated path')
```

2. **initialize()**<br>Everything should be started with the setPath() Function to select the destinated path before initializing the directory of file management.<br><br>
The function can create a directory destinated for file management. For example **Batch For Vendor** folder.
```py 
setPath('Your own destinated path')
initialize()
``` 
