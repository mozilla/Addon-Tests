Selenium Tests for addons.mozilla.org (amo)
====================

This repository contains Selenium tests written in Python for testing the website addons.mozilla.org.

Skills needed for contributing effectively
------------------------------------------

We love working with contributors to fill out the Selenium test coverage for addons, but it does require a few skills.   If you want to contribute automated tests to AMO, you will need to know some Python, some Selenium and you will need some basic familiarity with Github.

If you know some Python, it's worth having a look at the Selenium framework to understand the basic concepts of browser based testing and especially page objects. We've got a branch which uses [Selenium RC][SeRC] and a branch which uses [Selenium Webdriver][webdriver]

If you need to brush up on programming but are eager to start contributing immediately, please consider helping us find bugs in Mozilla [Firefox][firefox] or find bugs in the Mozilla web-sites tested by the [WebQA][webqa] team.

To brush up on  Python skills before engaging with us, [Dive Into Python][dive] is an excellent resource.  MIT also has [lecture notes on Python][mit] available through their open courseware.The programming concepts you will need to know include functions, working with classes, and some object oriented programming basics. 

[mit]: http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-189-a-gentle-introduction-to-programming-using-python-january-iap-2011/
[dive]: http://diveintopython.nfshost.com/toc/index.html
[webqa]: http://quality.mozilla.org/teams/web-qa/
[firefox]: http://quality.mozilla.org/teams/desktop-firefox/
[SeRC]: http://seleniumhq.org/docs/05_selenium_rc.html
[webdriver]: http://seleniumhq.org/docs/03_webdriver.html

Questions are always welcome
----------------------------
While we take pains to keep our documentation updated, the best source of information is those of us who work on the project.  Don't be afraid to join us in irc.mozilla.org #mozwebqa to ask questions about our Selenium tests.  Mozilla also hosts the #mozillians chat room to answer your general questions about contributing to Mozilla.

[mozwebqa]:http://02.chat.mibbit.com/?server=irc.mozilla.org&channel=#mozwebqa
[mozillians]:http://02.chat.mibbit.com/?server=irc.mozilla.org&channel=#mozillians

How to Set up and Build AMO Tests Locally
-----------------------------------------
This repository contains Selenium tests used to test the website addons.mozilla.org.  This readme file describes who to set up your environment to run the Selenium tests on your local machine.  [This wiki page][softvision] has instructions specific to windows.

[softvision]: https://wiki.mozilla.org/QA_SoftVision_Team/WebQA_Automation

###You will need to install the following:

### Java
You will need a version of the [Java Runtime Environment][JRE] installed

[JRE]: http://www.oracle.com/technetwork/java/javase/downloads/index.html

### Python
Before you will be able to run these tests you will need to have Python 2.6 installed.

### Requirements.txt
This will install several Python libraries needed for running our tests including pytest and our own mozwebqa plugin.

Run

    easy_install pip

followed by

    sudo pip install -r requirements.txt
    
__note__

If you are running on Ubuntu/Debian you will need to do following first

    sudo apt-get install python-setuptools
    
to install the required Python libraries.

###Virtualenv and Virtualenvwrapper
While most of us have had some experience using virtual machines, [virtualenv][venv] is something else entirely.  It's used to keep libraries that you install from clashing and messing up your local environment.  After installing virtualenv, installing [virtualenvwrapper][wrapper] will give you some nice commands to use with virtualenvwrapper.

[venv]: http://pypi.python.org/pypi/virtualenv
[wrapper]: http://www.doughellmann.com/projects/virtualenvwrapper/

### Moz-grid-config

[Moz-grid-config][moz-grid] is a separate repository containining our Selenium grid configuration.  We recommend git cloning the repository for a couple of reasons:

1. It will give you access to a profile containing certificate exceptions which you will need.
2. It contains a jar file of the latest Selenium in it's lib directory

(If you prefer to download Selenium it's own, you can do that from [here][Selenium Downloads])

To start the Selenium jar file with the moz-grid-config firefox profile, run the following command line:

    java -jar <your path here>/moz-grid-config/lib/selenium-server-standalone-<current version>.jar -firefoxProfileTemplate <your path here>/moz-grid-config/firefoxprofiles/certificateExceptions/

You will need to make sure that the name of your Firefox application matches one of the names in moz-grid-config/grid_configuration.yml.  As an example:  even though Firefox typically installs without a version number in the name, moz-grid-config requires it to be named "Firefox <version number>".app on mac. 

[Selenium Downloads]: http://code.google.com/p/selenium/downloads/list
[moz-grid]:https://github.com/mozilla/moz-grid-config
### Running tests locally

Tests are run using the py.test library.  You will find examples here for running all of the tests, tests in one file and running a single test.

An example of running all tests:

	py.test --browser="Firefox 7 on Mac OS X" --credentials=/credentials.yaml
	
An example of running all of the tests in one file:

	py.test --browser="Firefox 7 on Mac OS X" --credentials=/credentials.yaml -q tests/test_details_page.py
	
An example of running one test in a file:

	py.test  --browser="Firefox 7 on Mac OS X" --credentials=/credentials.yaml -q tests/test_details_page.py -k test_that_external_link_leads_to_addon_website

To run the user accounts tests:

1. Create an account on the AMO instance
2. Edit the credentials.yaml with your credentials
3. Run the tests with:

		py.test --credentials=~/credentials.yaml

For more command line options access https://github.com/davehunt/pytest-mozwebqa

Writing Tests
-------------

If you want to get involved and add more tests then there's just a few things
we'd like to ask you to do:

1. Use the [template files][GitHub Templates] for all new tests and page objects
2. Follow our simple [style guide][Style Guide]
3. Fork this project with your own GitHub account
4. Add your test into the "tests" folder and the necessary methods for it into the appropriate file in "pages"
5. Make sure all tests are passing, and submit a pull request with your changes

[GitHub Templates]: https://github.com/AutomatedTester/mozwebqa-test-templates
[Style Guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide

License
-------
This software is licensed under the [Mozilla Tri-License][MPL]:

    ***** BEGIN LICENSE BLOCK *****
    Version: MPL 1.1/GPL 2.0/LGPL 2.1

    The contents of this file are subject to the Mozilla Public License Version
    1.1 (the "License"); you may not use this file except in compliance with
    the License. You may obtain a copy of the License at
    http://www.mozilla.org/MPL/

    Software distributed under the License is distributed on an "AS IS" basis,
    WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
    for the specific language governing rights and limitations under the
    License.

    The Original Code is Mozilla WebQA Selenium Tests.

    The Initial Developer of the Original Code is Mozilla.
    Portions created by the Initial Developer are Copyright (C) 2011
    the Initial Developer. All Rights Reserved.

    Contributor(s):
      Dave Hunt <dhunt@mozilla.com>

    Alternatively, the contents of this file may be used under the terms of
    either the GNU General Public License Version 2 or later (the "GPL"), or
    the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
    in which case the provisions of the GPL or the LGPL are applicable instead
    of those above. If you wish to allow use of your version of this file only
    under the terms of either the GPL or the LGPL, and not to allow others to
    use your version of this file under the terms of the MPL, indicate your
    decision by deleting the provisions above and replace them with the notice
    and other provisions required by the GPL or the LGPL. If you do not delete
    the provisions above, a recipient may use your version of this file under
    the terms of any one of the MPL, the GPL or the LGPL.

    ***** END LICENSE BLOCK *****

[MPL]: http://www.mozilla.org/MPL/
