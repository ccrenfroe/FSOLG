# Requirements for Web Scrapper


## Packages
[Pandas]()

[Selenimum](https://selenium-python.readthedocs.io/)

[Requests] (https://pandas.pydata.org/)


## Webdriver
[Selenium Webdriver docs](https://selenium-python.readthedocs.io/installation.html)
In order for Selenium to work, it needs a webdriver. The driver depends on the browser you want to use, and are referenced to by the Selenium docs [here](https://selenium-python.readthedocs.io/installation.html#drivers). ** Make sure to add it to your PATH. **

### Windows
Path can be found by going to the *Control Panel*, then searching for *environmental variables*.

## Linux 
Extract the file with:
```
tar -xvzf [driver_name]*
```
Make it executable
```
Make it executable:

chmod +x [driver]
```
Add the driver to your PATH so other tools can find it:
```
export PATH=$PATH:/path-to-extracted-file/.
```
Paraphrased from [this](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)

## Mac
I recommend using Chromium since it runs the fastest.

[Guide] (https://www.kenst.com/2015/03/including-the-chromedriver-location-in-macos-system-path/)
