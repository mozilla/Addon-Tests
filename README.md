Tests for addons.mozilla.org (amo)
==================================

Thank you for checking out Mozilla's Addon-Tests test suite.
This repository contains Selenium tests used to test the website addons.mozilla.org.

[![license](https://img.shields.io/badge/license-MPL%202.0-blue.svg)](https://github.com/mozilla/Addon-Tests/blob/master/LICENSE)
[![travis](https://img.shields.io/travis/mozilla/Addon-Tests.svg?label=travis)](http://travis-ci.org/mozilla/Addon-Tests/)
[![dev](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/amo.dev.svg?label=dev)](https://webqa-ci.mozilla.com/job/amo.dev/)
[![stage](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/amo.stage.saucelabs.svg?label=stage)](https://webqa-ci.mozilla.com/job/amo.stage.saucelabs/)
[![prod](https://img.shields.io/jenkins/s/https/webqa-ci.mozilla.com/amo.prod.svg?label=prod)](https://webqa-ci.mozilla.com/job/amo.prod/)
[![requirements](https://img.shields.io/requires/github/mozilla/Addon-Tests.svg)](https://requires.io/github/mozilla/Addon-Tests/requirements/?branch=master)

Getting involved
----------------

We love working with contributors to fill out the Selenium test coverage for Addon-Tests,
but it does require a few skills.
By contributing to our test suite you will have an opportunity to learn and/or improve your
skills with Python, Selenium WebDriver, GitHub, Virtualenv, the Page Object Model, and more.

For some resources for learning about these technologies, take a look at our documentation on 
[Running Web QA automated tests][runningtests].

[runningtests]: https://developer.mozilla.org/en-US/docs/Mozilla/QA/Running_Web_QA_automated_tests

The following contributors have submitted pull requests to Addon-Tests:

https://github.com/mozilla/Addon-Tests/contributors


Questions are always welcome
----------------------------
While we take pains to keep our documentation updated, the best source of information is those 
of us who work on the project.  
Don't be afraid to join us in irc.mozilla.org [#mozwebqa][mozwebqa] to ask questions about our 
Selenium tests.
We also have a [mailing list][mailing_list] available that you are welcome to join and post to.

[mozwebqa]:http://widget01.mibbit.com/?settings=1b10107157e79b08f2bf99a11f521973&server=irc.mozilla.org&channel=%23mozwebqa
[mailing_list]:https://mail.mozilla.org/listinfo/mozwebqa

How to run the tests locally
-----------------------------------------
We maintain a [detailed guide][runningtests] to running our automated tests which can be found on the MDN website.
If you want to get started quickly, you can try following the steps in our quick-start instructions below:

###Clone the repository
If you have cloned this project already then you can skip this, otherwise you'll need to clone this repo using Git.
If you do not know how to clone a GitHub repository, check out this 
[help page] (https://help.github.com/articles/cloning-a-repository/) from GitHub.

If you think you would like to contribute to the tests by writing or maintaining them in the future,
it would be a good idea to create a fork of this repository first, and then clone that.
GitHub also has great instructions for [forking a repository] (https://help.github.com/articles/fork-a-repo/).

###Create or activate a Python virtual environment
You should install this project's dependencies (which is described in the next step) into a virtual environment
in order to avoid impacting the rest of your system, and to make problem solving easier.
If you already have a virtual environment for these tests, then you should activate it, 
otherwise you should create a new one.
For more information on working with virtual environments see our 
[our quickstart guide] (https://wiki.mozilla.org/QA/Execution/Web_Testing/Automation/Virtual_Environments) 
and also [this blog post] (http://www.silverwareconsulting.com/index.cfm/2012/7/24/Getting-Started-with-virtualenv-and-virtualenvwrapper-in-Python).

### Install dependencies
Install the Python packages that are needed to run our tests using pip. In a terminal, 
from the the project root, issue the following command:

    pip install -Ur requirements.txt

### Create a variables.json file
Some of the tests in this repo need to log into the add-ons website and/or PayPal.
We store the credentials (i.e., username and password) to access those sites in a file 
called `variables.json`, which we then pass to the tests via the command line. 
If you want to be able to run any of those tests, you will need your own copy of 
the `variables.json` file, which you will update to contain your own credentials.
To do that, make a copy of the `variables.json` file which exists in the project root
 and update that with your own credentials. 
 You will then pass the name of that file on the command line. 
 For the purposes of the examples below, assume you named your copy of the file `my_variables.json`.

### Run the tests

Tests are run using the command line. Below are a couple of examples of running the tests:

To run all of the desktop tests against the default environment, which is the add-ons development environment:

	py.test --driver=firefox --variables=my_variables.json tests/desktop
	
To run against a different environment, pass in a value for --baseurl, like so:

	py.test --baseurl=https://addons.allizom.org --driver=firefox --variables=my_variables.json tests/desktop

The pytest plugin that we use for running tests has a number of advanced command-line 
options available. To see the options available, try running:

    py.test --help

The full documentation for the plugin can be found at the [pytest-mozwebqa GitHub project page] [pymozwebqa].
[pymozwebqa]: https://github.com/mozilla/pytest-mozwebqa
