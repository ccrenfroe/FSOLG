# Requirements for Web Scrapper


## Packages
[Pandas](https://pandas.pydata.org/)

[Selenimum](https://selenium-python.readthedocs.io/)

[Requests](https://github.com/psf/requests)


## Webdriver
[Selenium Webdriver docs](https://selenium-python.readthedocs.io/installation.html)
In order for Selenium to work, it needs a webdriver. The driver depends on the browser you want to use, and are referenced to by the Selenium docs [here](https://selenium-python.readthedocs.io/installation.html#drivers). ** Make sure to add it to your PATH. **

I recommend using Chromium since it runs the fastest.

## Windows
Example using Chrome Driver
- Install the latest stable release of Chrome Driver [link](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- Unzip the file
- Move chromedriver.exe to C:\Windows. This will add it to your PATH since 
Path can be found by going to the *Control Panel*, then searching for *environmental variables*.

## Linux 
- Extract the file with:
```
tar -xvzf [driver_name]*
```
- Make it executable
```
Make it executable:

chmod +x [driver]
```
- Add the driver to your PATH so other tools can find it:
```
export PATH=$PATH:/path-to-extracted-file/.
```
Paraphrased from [this](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu)

## Mac
- Install the latest stable release of Chrome Driver [link](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- Move to **/usr/local/bin folder**
- Go to downloads folder and unpack chromedriver file
- Run this command : ** mv chromedriver /usr/local/bin **

Paraphrased from [this](https://www.swtestacademy.com/install-chrome-driver-on-mac/)

## After Installation
Make sure to update your driver to whichever webdriver you chose. For example, if you chose Chrome Driver, make sure the driver is updated to webdriver.Chrome(). Refer to line 33, labeled Webdriver, in the Webscraper code.

## Troublshooting
If difficulty arises with Python trying to find the Webdriver, refer to [this](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-snippets/) documentation
