lume :fire:  [![version](https://img.shields.io/github/release/alice-biometrics/lume/all.svg)](https://github.com/alice-biometrics/lume/releases) [![ci](https://github.com/alice-biometrics/lume/workflows/ci/badge.svg)](https://github.com/alice-biometrics/lume/actions) [![pypi](https://img.shields.io/pypi/dm/lume)](https://pypi.org/project/lume/)
=====

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

A Python-based handy automation tool. Lume helps you with your daily dev operations and ease the CI & CD process. 

## Table of Contents
- [Installation :computer:](#installation-computer)
- [Getting Started :chart_with_upwards_trend:](#getting-started-chart_with_upwards_trend)
  * [Configuration File](#configuration-file)
  * [Run Defined Steps](#run-defined-steps)
  * [Advanced Configurations](#advanced-configurations)
- [Acknowledgements :raised_hands:](#acknowledgements-raised_hands)
- [Contact :mailbox_with_mail:](#contact-mailbox_with_mail)

## Installation :computer:

~~~
pip install lume
~~~

## Getting Started :chart_with_upwards_trend:	

**lume** is a simple way to organize installation, setup, code compilation, test, etc..

#### Configuration File

If you want to use lume in your project, just add a `lume.yml` in your root.

```yml
name: lume-sample

install:
  run:
  - echo "Installing..."

steps:
  clean:
    run:
    - echo "Cleaning..."
  build:
    run:
    - echo "Building..."
  test:
    run:
    - echo "Testing..."
```

Add `show_exit_code: True` in settings if you want lume to print the program exit code.

```yml

settings:
  show_exit_code: True
```

You can use `help` to know what lume is able to do for you:

```console
>> lume -h
usage: lume 🔥 [-h] [-v] [-all] [-clean] [-build] [-test] [-install]

Lume helps you with your daily dev operations and ease the CI & CD process.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show lume version number.
  -all, --all-commands  run all commands
  -clean, --clean       clean
  -build, --build       build
  -test, --test         test
  -install, --install   install

```

If you want to save your lume file in another folder or change the name, you can do it with the Environment Variable `LUME_CONFIG_FILENAME`.

```console
>> export LUME_CONFIG_FILENAME=examples/lume-sample.yml; lume -h
```

#### Run Defined Steps

Lume automatically parses your `lume.yml` file allowing you to call it.

To run install:

```console
>> lume -install
🔥 Step: install
👩‍💻 install >> echo "Installing..."
 Installing...
```

To run all the steps:

```console
>> lume -all
🔥 Step: clean
👩‍💻 clean >> echo "Cleaning..."
 Cleaning...
🔥 Step: build
👩‍💻 build >> echo "Building..."
 Building...
🔥 Step: test
👩‍💻 test >> echo "Testing (Unit)..."
 Testing (Unit)...
👩‍💻 test >> echo "Testing (Integration)..."
 Testing (Integration)...
🔥 Step: error
👩‍💻 error [cwd=examples] >> echo "This is an error" >>/dev/stderr
🧐 This is an error

```

Of course, you can run every step individually:

```console
>> lume -clean
🔥 Step: clean
👩‍💻 clean >> echo "Cleaning..."
 Cleaning...
```

Or several steps:

```console
>> lume -build -test
🔥 Step: build
👩‍💻 build >> echo "Building..."
 Building...
🔥 Step: test
👩‍💻 test >> echo "Testing (Unit)..."
 Testing (Unit)...
👩‍💻 test >> echo "Testing (Integration)..."

```

#### Advanced Configurations

Lume allows you to define several commands per Step:

```yml
steps:
  clean:
    run:
    - echo "Cleaning dep1"
    - echo "Cleaning dep2"
```
Additionally, lume implements a special step to manage dependencies such us resources.

```yml
steps:
  
  setup:
    output: deps
    deps:
      images:
        type: file
        url: https://path/images.zip
        name: images
        auth_required: true
        credentials_env: ENVVAR_CREDENTIALS
        unzip: true
      resources:
        type: bucket
        url: gs://alice-biometrics/resources.zip
        name: resources
        auth_required: true
        credentials_env: GOOGLE_APPLICATION_CREDENTIALS
        unzip: true
  build:
    run:
    - echo "Creating dir"
    - echo "Building..."
  lint:
    run:
    - echo "Checking code..."
  doc:
    cwd: examples
    run:
    - echo $(pwd)
    - echo "Doc is nice"
  loop:
    cwd: examples
    run:
    -  for((i=1;i<=20000;i+=1)); do echo "Welcome $i times"; done
```

## Acknowledgements :raised_hands:

`bowie` inspired us! 👨‍🎤 :clap:

Thanks to `bowie` development team in [Gradiant](https://github.com/Gradiant).


## Contact :mailbox_with_mail:

support@alicebiometrics.com
