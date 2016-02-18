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
[running Web QA automated tests][running-tests].

All of [these awesome contributors][contributors] have opened pull requests
against this repository.


Questions are always welcome
----------------------------
While we take pains to keep our documentation updated, the best source of information is those
of us who work on the project.  
Don't be afraid to join us in irc.mozilla.org [#mozwebqa][mozwebqa] to ask questions about our
Selenium tests.
We also have a [mailing list][mailing_list] available that you are welcome to join and post to.

How to run the tests locally
-----------------------------------------
We maintain a [detailed guide][running-tests] to running our automated tests which can be found on the MDN website.
If you want to get started quickly, you can try following the steps in our quick-start instructions below:

### Clone the repository
If you have cloned this project already then you can skip this, otherwise you'll need to clone this repo using Git.
If you do not know how to clone a GitHub repository, check out this
[help page][git-clone] from GitHub.

If you think you would like to contribute to the tests by writing or maintaining them in the future,
it would be a good idea to create a fork of this repository first, and then clone that.
GitHub also has great instructions for [forking a repository][git-fork].

### Create or activate a Python virtual environment
You should install this project's dependencies (which is described in the next step) into a virtual environment
in order to avoid impacting the rest of your system, and to make problem solving easier.
If you already have a virtual environment for these tests, then you should activate it,
otherwise you should create a new one.
For more information on working with virtual environments see our
[summary][virtualenv].

### Install dependencies
Install the Python packages that are needed to run our tests using pip. In a terminal,
from the the project root, issue the following command:

```bash
$ pip install -Ur requirements.txt
```

### Create test variables files

#### API
Some tests use the [Add-ons Server API][api] to create necessary test data in
the application. For this to work you will need to
[obtain a key and a secret][api-credentials] from the API Credentials
Management Page and place then in a JSON file with the following format:

```json
{
  "api": {
    "addons.allizom.org": {
      "jwt_issuer": "",
      "jwt_secret": ""
    },
    "addons-dev.allizom.org": {
      "jwt_issuer": "",
      "jwt_secret": ""
    }
  }
}
```

You will need an entry in this file for each environment you intend to use the
API for. This file will then need to be referenced on the command line using
the `--variables` option.

Tests that use the [super-create][api-super-create] endpoint require a user
in the `Accounts:SuperCreate` group. Speak to a member of the add-ons or Web QA
team to be added to this group.

#### PayPal
Some of the tests in this repo need to log into PayPal. If you want to be able
to run any of these tests, you will need to place your PayPal credentials in a
JSON file with the following format:

```json
{
  "paypal": {
    "email": "",
    "password": ""
  }
}
```

This file will then need to be referenced on the command line using the
`--variables` option.

### Run the tests
Tests are run using the command line. Below are a couple of examples of running the tests:

To run all of the desktop tests against the default environment, which is the add-ons development environment:

```bash
$ py.test --driver Firefox --variables api.json --variables paypal.json tests/desktop
```

To run against a different environment, pass in a value for `--base-url`, like so:

```bash
$ py.test --base-url https://addons.allizom.org --driver Firefox --variables api.json --variables paypal.json  tests/desktop
```

The pytest plugin that we use for running tests has a number of advanced
command line options available. To see the options available, run
`py.test --help`. The full documentation for the plugin can be found
[here][pytest-selenium].

[contributors]: https://github.com/mozilla/Addon-Tests/contributors
[git-clone]: https://help.github.com/articles/cloning-a-repository/
[git-fork]: https://help.github.com/articles/fork-a-repo/
[irc]: http://widget01.mibbit.com/?settings=1b10107157e79b08f2bf99a11f521973&server=irc.mozilla.org&channel=%23mozwebqa
[list]: https://mail.mozilla.org/listinfo/mozwebqa
[pytest-selenium]: http://pytest-selenium.readthedocs.org/
[running-tests]: https://developer.mozilla.org/en-US/docs/Mozilla/QA/Running_Web_QA_automated_tests
[virtualenv]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Automation/Virtual_Environments
[api]: http://addons-server.readthedocs.org
[api-credentials]: http://addons-server.readthedocs.org/en/latest/topics/api/auth.html#access-credentials
[api-super-create]: http://addons-server.readthedocs.org/en/latest/topics/api/accounts.html#super-creation
