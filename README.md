# Preprocessing the Chinese Gigaword Datset

The scripts in this repository dump the text of the Gigaword dataset into preporcessed headline and paragraph files, for use 
with summarization tasks. The pipeline of the scirpt is (1) merging data in the corpus, (2) tokenizing words by jieba, (3) convering simplified chinese into tranditional chinese (or you can do the inverse translation).

See my [blog post on flattening the Gigaword corpus](https://blog.nelsonliu.me/2017/09/23/flattening-the-gigaword-corpus/) for 
more information about how the code in this repo works.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

To run this code, you must have **GNU Parallel**. This can be installed on Ubuntu with:

```
sudo apt-get install parallel
```

This project was developed in Python 3.6, but should work with Python 3.x and 2.x.
Please raise an issue if you find that this is not the case.

[Conda](https://conda.io/) will set up a virtual environment with the exact
version of Python used for development along with all the dependencies
needed to run the code in this package.

1.  [Download and install conda](https://conda.io/docs/download.html).

2.  Create a conda environment with Python 3.6.

    ```
    conda create -n flat python=3.6
    ```

3.  Now activate the conda environment.

    ```
    source activate flat
    ```

4.  Install the required dependencies with `pip`.

    ```
    pip install -r requirements.txt
    ```

5.  Install the required SpaCy data pack.
    ```
    python -m spacy link jieba zh
    ```
    
## Usage

[`flatten_one_gigaword.py`](./flatten_one_gigaword.py) takes in the path of a Gigaword data file
and an output directory to write a flattened version to. The bash script at 
[`flatten_all_gigaword.sh`](./flatten_all_gigaword.sh) is a thin wrapper that feeds the paths of all the
Gigaword data files to [`flatten_one_gigaword.py`](./flatten_one_gigaword.py) and combines the final output.
[`flatten_all_gigaword.sh`](./flatten_all_gigaword.sh) takes in three positional arguments:

1.  The path to the Gigaword directory (unzip files by uncommenting unzip part in ([`flatten_all_gigaword.sh`](./flatten_all_gigaword.sh).

2.  A directory to write the flattened files to and the final combined output. 
    It will be created if it does not exist.

3. The number of files to process at once.

For example, you can run:

```
./flatten_all_gigaword.sh ./data/gigaword_eng_5/ tmp/ 24
```

to extract data (in parallel, processing 24 files at a time) from the Gigaword corpus 
at `./data/gigaword_eng_5/` and write the flattened files + combined output to `tmp/`. 

Simplified2tranditional Chinese Conversion:
follow conversion instrction from (opencc-python)[https://github.com/yichen0831/opencc-python]
``` python
from opencc import OpenCC
cc = OpenCC('s2t')  # convert from Simplified Chinese to Traditional Chinese
# can also set conversion by calling set_conversion
# cc.set_conversion('s2tw')
to_convert = '开放中文转换'
converted = cc.convert(to_convert)
```
### Command Line

```sh
usage: python -m opencc [-h] [-i <file>] [-o <file>] [-c <conversion>]
                        [--in-enc <encoding>] [--out-enc <encoding>]

optional arguments:
  -h, --help            show this help message and exit
  -i <file>, --input <file>
                        Read original text from <file>. (default: None = STDIN)
  -o <file>, --output <file>
                        Write converted text to <file>. (default: None = STDOUT)
  -c <conversion>, --config <conversion>
                        Conversion (default: None)
  --in-enc <encoding>   Encoding for input (default: UTF-8)
  --out-enc <encoding>  Encoding for output (default: UTF-8)

example with UTF-8 encoded file:

  python -m opencc -c s2t -i my_simplified_input_file.txt -o my_traditional_output_file.txt

See https://docs.python.org/3/library/codecs.html#standard-encodings for list of encodings.
```

### Conversions 轉換

* `hk2s`: Traditional Chinese (Hong Kong standard) to Simplified Chinese

* `s2hk`: Simplified Chinese to Traditional Chinese (Hong Kong standard)

* `s2t`: Simplified Chinese to Traditional Chinese

* `s2tw`: Simplified Chinese to Traditional Chinese (Taiwan standard)

* `s2twp`: Simplified Chinese to Traditional Chinese (Taiwan standard, with phrases)

* `t2hk`: Traditional Chinese to Traditional Chinese (Hong Kong standard)

* `t2s`: Traditional Chinese to Simplified Chinese

* `t2tw`: Traditional Chinese to Traditional Chinese (Taiwan standard)

* `tw2s`: Traditional Chinese (Taiwan standard) to Simplified Chinese

* `tw2sp`: Traditional Chinese (Taiwan standard) to Simplified Chinese (with phrases)
