Selenium Tests for addons.mozilla.org (amo)
====================

Thank you for checking out Mozilla's Addon-Tests test suite. Mozilla and the Mozwebqa team are grateful for the help and hard work of many contributors like yourself.
The following contributors have submitted pull requests to Addon-Tests:

https://github.com/mozilla/Addon-Tests/contributors

Continuous Integration
----------------------

[![Build Status](https://secure.travis-ci.org/mozilla/Addon-Tests.png?branch=master)](http://travis-ci.org/mozilla/Addon-Tests/)

Getting involved as a contributor
------------------------------------------

We love working with contributors to fill out the Selenium test coverage for Addon-Tests, but it does require a few skills.   You will need to know some Python, some Selenium and you will need some basic familiarity with Github.

If you know some Python, it's worth having a look at the Selenium framework to understand the basic concepts of browser based testing and especially page objects. Our suite uses [Selenium WebDriver][webdriver].

If you need to brush up on programming but are eager to start contributing immediately, please consider helping us find bugs in Mozilla [Firefox][firefox] or find bugs in the Mozilla web-sites tested by the [WebQA][webqa] team.

To brush up on Python skills before engaging with us, [Dive Into Python][dive] is an excellent resource.  MIT also has [lecture notes on Python][mit] available through their open courseware.The programming concepts you will need to know include functions, working with classes, and some object oriented programming basics. 

[mit]: http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2011/
[dive]: http://www.diveintopython.net/toc/index.html
[webqa]: http://quality.mozilla.org/teams/web-qa/
[firefox]: http://quality.mozilla.org/teams/desktop-firefox/
[webdriver]: http://seleniumhq.org/docs/03_webdriver.html

Questions are always welcome
----------------------------
While we take pains to keep our documentation updated, the best source of information is those of us who work on the project.  Don't be afraid to join us in irc.mozilla.org #mozwebqa to ask questions about our Selenium tests.  Mozilla also hosts the #mozillians chat room to answer your general questions about contributing to Mozilla.

[mozwebqa]:http://02.chat.mibbit.com/?server=irc.mozilla.org&channel=#mozwebqa
[mozillians]:http://02.chat.mibbit.com/?server=irc.mozilla.org&channel=#mozillians

How to Set up and Build AMO Tests Locally
-----------------------------------------
This repository contains Selenium tests used to test the website addons.mozilla.org.

Mozilla maintains a guide to running Automated tests on our QMO website:

https://quality.mozilla.org/docs/webqa/running-webqa-automated-tests/

###You will need to install the following:

#### Git
If you have cloned this project already then you can skip this!
GitHub has excellent guides for [Windows][GitWin], [MacOSX][GitMacOSX] and [Linux][GitLinux].
[GitWin]: http://help.github.com/win-set-up-git/
[GitMacOSX]: http://help.github.com/mac-set-up-git/
[GitLinux]: http://help.github.com/linux-set-up-git/

#### Python
Before you will be able to run these tests you will need to have [Python 2.6][Python] installed.
[Python]: http://www.python.org/download/releases/2.6.6/

Install pip (for managing Python packages):

    sudo easy_install pip

#### Before you begin
Before you dive into running tests you will want to register for an account on 
[Addons-Dev][AddonsDev].  For security reasons you may want to create
this account with a different username and password than you may have on the production addons site.
[AddonsDev]: https://addons-dev.allizom.org/en-US/firefox/

#### Installing dependencies

If you are using virtualenv, create and activate the virtualenv, then run the following in the project root:

    pip install -r requirements.txt

If you are not using virtualenv, run the following in the project root to install dependencies globally:

    sudo pip install -r requirements.txt

For more information on virtualenv, [see below] (#virtualenv-and-virtualenvwrapper-optionalintermediate-level).

#### Running tests locally

Tests are run using the py.test library. You will find examples here for running all of the tests, tests in one file and running a single test.

WebDriver does not need a Selenium Server or Grid to run so these examples bypass this step and just use the --driver command.

An example of running all tests:

	py.test --driver=firefox --credentials=./credentials.yaml
	
An example of running all of the tests in one file:

	py.test --driver=firefox --credentials=./credentials.yaml tests/desktop/test_details_page.py
	
An example of running one test in a file:

	py.test --driver=firefox --credentials=./credentials.yaml tests/desktop/test_details_page.py -k test_that_external_link_leads_to_addon_website

If running on a Mac, skip tests which require 'native' support:

    py.test --driver=firefox --credentials=./credentials.yaml -m 'not native'
    
Depending on the platform you're running the tests on, run only the tests in the mobile or desktop directories:

    py.test --driver=firefox --credentials=./credentials.yaml tests/desktop
    py.test --driver=firefox --credentials=./credentials.yaml tests/mobile
    
For information about running tests against a Selenium Grid or moz-grid-config see the section in this document about setting up moz-grid-config.


The mozwebqa plugin has advanced command line options for reporting and using browsers. To see the options available, try running:

    py.test --help

Also see the documentation on [davehunt's pytest-mozwebqa Github project page] [pymozwebqa].
[pymozwebqa]: https://github.com/davehunt/pytest-mozwebqa

####Virtualenv and Virtualenvwrapper (Optional/Intermediate level)
While most of us have had some experience using virtual machines, [virtualenv][venv] is something else entirely.  It's used to keep libraries that you install from clashing and messing up your local environment.  After installing virtualenv, installing [virtualenvwrapper][wrapper] will give you some nice commands to use with virtualenv.
[venv]: http://pypi.python.org/pypi/virtualenv
[wrapper]: http://www.doughellmann.com/projects/virtualenvwrapper/

For a more detailed discussion of virtualenv and virtualenvwrapper, check out [our quickstart guide] (https://wiki.mozilla.org/QA/Execution/Web_Testing/Automation/Virtual_Environments) and also [this blog post] (http://www.silverwareconsulting.com/index.cfm/2012/7/24/Getting-Started-with-virtualenv-and-virtualenvwrapper-in-Python).

#### Moz-grid-config (Optional/Intermediate level)
Prerequisites: [Java Runtime Environment][Java JRE], [Apache Ant][ANT]

[Moz-grid-config][moz-grid] is a project containining our Selenium Grid configuration. It uses Apache Ant to run the Selenium hub or node to the configuration defined in the yaml files.

We recommend git cloning the repository for a couple of reasons:

1. The commands to launch a node or hub are all pre-configured and as simple as typing `ant launch-hub` or `ant launch-node`
2. The paths to browser binaries and nodes can be stored in configuration (yaml) files
3. It contains a jar file of the latest Selenium in it's lib directory

(If you prefer to download Selenium it's own, you can do that from [here][Selenium Downloads])
You will need to make sure that the name of your Firefox application matches one of the names in moz-grid-config/grid_configuration.yml.  As an example:  even though Firefox typically installs without a version number in the name, moz-grid-config requires it to be named "Firefox <version number>".app on mac. 

[moz-grid]:https://github.com/mozilla/moz-grid-config
[ANT]: http://ant.apache.org/
[Java JRE]: http://www.oracle.com/technetwork/java/javase/downloads/index.html
[Selenium Downloads]: http://code.google.com/p/selenium/downloads/list


Writing Tests
-------------

If you want to get involved and add more tests then there's just a few things
we'd like to ask you to do:

1. Use an existing file from this repository as a template for all new tests and page objects
2. Follow our simple [style guide][Style Guide]
3. Fork this project with your own GitHub account
4. Add your test into the "tests" folder and the necessary methods for it into the appropriate file in "pages"
5. Make sure all tests are passing and submit a pull request with your changes

[GitHub Templates]: https://github.com/mozilla/mozwebqa-test-templates 
[Style Guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide

License
-------
This software is licensed under the [MPL] 2.0:

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.

[MPL]: http://www.mozilla.org/MPL/2.0/
