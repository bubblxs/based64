<h2 align="center">based64</h2>

to run these tests, you must create the directory ``files``  in this very same dir and place some files inside it.

```
based64/
├── tests/
      ├── files/
      |     ├── test.png
      |     └── test.txt
      ├── tests.py
      └── tests.sh
...
```
the ``tests.py`` will test all the functions and ``tests.sh`` will test the python script itself by running it with individuals tests files as args.

to run them

``` bash
$ python3 -m unittest
```

``` bash
$ bash tests.sh
```