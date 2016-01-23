# PyScraping
Simple demo of web scraping in Python

### Purpose

PyScraping is designed to be a primer for how to scrape web resources using python.

### Requirements

1. Python 2.7
2. BeautifulSoup4 
3. html5lib

*Recommended:*
pip, virtualenv

### Quick Start

Assuming you have installed *python*, *pip*, and *virtualenv*, see the following commands to run the example code.

1. Establish a virtualenv...
<pre>
$ virtualenv path/to/my/environments/pyscraping
</pre>
2. Activate your environment...
  * On *nix
  <pre>
  $ source path/to/my/environments/pyscraping/bin/activate
  </pre>
  * On Windows
  <pre>
  C:\Path\To\Environments\pyscraping\Scripts\activate
  </pre>
3. Install the required libraries to the *pyscraping* environment
<pre>
pip install -r requirements.txt
</pre>
4. Run the driver script
<pre>
python PyScraping.py
</pre>
5. All downloaded files will be found in \PyScraping\nfl_example and parsed files will be found in \PyScraping\nfl_example\parsed

### Helpful Links

* [Virtual Environments](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [Windows virtualenv installation](http://pymote.readthedocs.org/en/latest/install/windows_virtualenv.html)
  * *Note*: The *get-pip.py* script mentioned in the article above has moved. You can find it here: [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
* [HOWTO Fetch Internet Resources Using urllib2](https://docs.python.org/2/howto/urllib2.html)
* [Beautiful Soup Documentation](http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
