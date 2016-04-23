# SJTU EC310

[![SJTU EC310][course-badge]][course-link]

[course-badge]: https://img.shields.io/badge/SJTU-EC310-brightgreen.svg
[course-link]: http://www.sjtu.edu.cn/

> Implementation for SJTU EC310 Econometrics.

## Install

Assume we've got Python 2.7.x and PIP.
Also, [Virtualenv](https://virtualenv.pypa.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) are recommended.

Clone and install dependencies.
```
$ git clone https://github.com/arrowrowe/ec310.git && cd ec310
$ pip install -r requirements.txt
```

You may need this.
```
$ export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## Usage

Let's pick Lab01 as an example.

```
# Directly output the report.
$ python lab01/main.py

# Output to a file.
$ python lab01/main.py > lab01/lab01.log

# Interactively play with its result.
$ ipython
In [1]: run -n lab01/main.py
In [2]: lab = Lab01()
```

## Contribution

Feel free to [open](https://github.com/arrowrowe/ec310/issues/new) [issues](https://github.com/arrowrowe/ec310/issues) or [send](https://github.com/arrowrowe/ec310/compare) [PRs](https://github.com/arrowrowe/ec310/pulls)!
