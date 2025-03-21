<h2 align="center">based64</h2>

> python script to decode or encode files to base64.

### requirements

- python 3.10

### usage

> [!WARNING]  
> be aware that if ``-f`` or ``--files`` flag is ommited, the script will encode all files located in the specified directory as well as in their subdirectories. yeah...

copy and paste the ``based64.py`` in the directory that you would like to encode all the files and execute ``python3 based64.py`` or ``python3 based64.py --decode`` to decode them.

example to encode by passing individual files with
`` -f, --files ``
flag:

``` bash
$ python3 based64.py -f file1.txt ~/Downloads/file2.png
```

decoding:

``` bash
$ python3 based64.py -f file1.txt -d
```

### know issues

- files named with a space - for example, ``random file.txt`` - will throw an exception during decoding. So if you are going to use this AMAZING script, please, give your items a proper name.
