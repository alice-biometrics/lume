lume :fire:  [![version](https://img.shields.io/github/release/alice-biometrics/lume/all.svg)](https://github.com/alice-biometrics/lume/releases) [![ci](https://github.com/alice-biometrics/lume/workflows/ci/badge.svg)](https://github.com/alice-biometrics/lume/actions) [![pypi](https://img.shields.io/pypi/dm/lume)](https://pypi.org/project/lume/)
=====

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png" width=auto>

A handy Python-based automation tool. 
`lume` helps you sort your commands, allows you to abstract from the development environment and facilitates CI and CD workflows. 

## Installation :computer:

~~~
pip install lume
~~~

## Getting Started :chart_with_upwards_trend:	

**lume** is a simple way to organize your daily software development operations (installation, setup, code compilation, test, etc..)

#### Configuration File

If you want to use lume in your project, just add a `lume.yml` in your root.

```yml
name: lume-sample

install:
  run: echo "Installing..."

steps:
  clean:
    run: echo "Cleaning folder1"
  build:
    run: echo "Building..."
  test:
    run: echo "Testing..."
```

If you want lume to print the program exit code, just type `show_exit_code: True` in `settings` in the `lume.yml`

```yml

settings:
  show_exit_code: True
```

Use `help` to know `lume` available commands. `lume` is dynamic, so the steps we are defining will be shown here automatically.

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

In case you want to change the name of the lume configuration file or just store in another folder, please use `LUME_CONFIG_FILENAME` environment variable.

```console
>> export LUME_CONFIG_FILENAME=examples/lume-sample.yml; lume -h
```

#### Run Defined Steps

To run install:

```console
>> lume -install
```

To run all the steps:

```console
>> lume -all
```

Of course, you can run every step individually:

```console
>> lume -clean
```

Or several steps:

```console
>> lume -build -test
```

Here is an example of the log output that would have lume using several commands definded previously on [Configuration File](#configuration-file):

```console
>> lume -install -all
🔥 Step: install
💻 install >> echo "Installing..."
 Installing...
 🔥 Step: clean
💻 clean >> echo "Cleaning..."
 Cleaning...
🔥 Step: build
💻 build >> echo "Building..."
 Building...
🔥 Step: test
💻 test >> echo "Testing (Unit)..."
 Testing (Unit)...
💻 test >> echo "Testing (Integration)..."
 Testing (Integration)...
🔥 Step: error
💻 error [cwd=examples] >> echo "This is an error" >>/dev/stderr
🧐 This is an error
```

## Features

#### OS-specific commands

Define your os-specific command adding new fields on `run` commands with specific os keys (`linux`, `macos`, `macos-arm` and `windows`)

Use it when installing dependencies:

```yml
install:
  run:
    linux:
       - sudo apt update
       - sudo apt install myprogram
     macos:
       - brew install myprogram
     macos-arm:
       - brew install myprogram
     all:
      - echo "Installed :fire:"
```

Or maybe for compiling a library with differents flags depending on the `OS`.

```yaml
steps:
  build:
    setup:
      linux: echo "Linux Setup..."
      macos: echo "MacOS Setup..."
      windows: echo "Windows Setup..."
    teardown:
      linux: echo "Linux Teardown..."
      macos: echo "MacOS Teardown..."
      windows: echo "Windows Teardown..."
    run:
      linux: echo "Building with Linux Compiler..."
      macos: echo "Building with MacOS Compiler..."
      windows: echo "Building with Windows Compiler..."
      all: echo "Checking Compiled Library..."
```

#### Use several lume file

Imagine you have multiple steps and you want to split them in several files. 
You can do it using the `other_steps` option. Just add the following code to your root `lume.yml`

```yaml
steps:
  build:
    run: echo "Building..."

other_steps:
  other: examples/other-steps.yml
```

Being `other-steps.yml` something like the following:

```yaml
steps:
  step-1:
    run: echo "Other Step 1..."
  step-2:
    run: echo "Other Step 1..."
```

To call use the name (in this case `other`) plus the step name (e.g `step-1`)

```bash
$ lume -other:step-1
```

You can setup some additional and specific env vars for these steps:

```yaml
envs:
  MY_OTHER_ENV: MY_VALUE

steps:
  step-1:
    run: echo "Other Step 1..."
  step-2:
    run: echo "Other Step 1..."
```

#### Several commands per Step

Use the hyphen in order to define several commands per Step:

```yml
steps:
  clean:
    run:
    - echo "Cleaning dep1"
    - echo "Cleaning dep2"
```

Or just use `|`:

```yml
steps:
  clean:
    run: |
      echo "Cleaning dep1"
      echo "Cleaning dep2"
```

#### Setup Step

Use `setup` step to manage to download and unzip dependencies form external resources (e.g `ftp` servers, `buckets`, etc..)

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

##### Setup and Teardown

Define `setup` commands to execute operations that will be executed before `run` commands. Use `teardown` comands to define command to be executed after `run`.

```yml
name: lume-sample

show_exit_code: True

install:
  run: echo "Installing..."

steps:
  my-step:
    setup: echo "Setup"
    run: echo "Run"
    teardown: echo "Teardown"
```

#### Set environment variables

`lume` allows the definition of shared envs or specific envs for every step.

###### Shared envs

Define your shared environment variables with `envs`

```yml
name: lume-sample

envs:
   MY_ENV: MY_VALUE
steps:
  my-step:
    run: echo ${MY_ENV}
```

Also, you can use a file to specify you environment variables:

```yml
name: lume-sample

env_file: path/to/my/env/file

steps:
  my-step:
    run: echo ${MY_ENV}
```

###### Step envs

```yml
name: lume-sample

install:
  run: echo "Installing..."

steps:
  my-step:
    envs:
      MY_ENV: MY_VALUE
    run: echo ${MY_ENV}
```

The output for this step will be something like the following:

```console
>> lume -my-step
🔥 Step: my-step
🔸 env: set MY_ENV=MY_VALUE
💻 my-step >> echo ${MY_ENV}
    MY_VALUE
```

Note that if you previously defined an *env*, it will be overwrote during the step.

You can also define variable from external filename (e.g [examples/env.yml](examples/env.yml) )

```yml
steps:
  envs-file-example:
    envs_file: examples/env.yml
    run: echo "${MY_ENV}"
```



#### Detach Setup

With `setup_detach` option, you can execute a detached command (e.g a service). Then, after the main `run` command, this proccess will be automatically killed.

This is very useful to test services locally:

```yml
name: lume-sample

show_exit_code: True

install:
  run: echo "Installing..."

steps:
  my-step:
    setup_detach:
      log_filename: taskmanager.log
      run: python -m taskmanager # service
    run: pytest
```

#### Wait


Wait few seconds with `wait_seconds`:

```yml
steps:
  wait-example-seconds:
    wait_seconds: 2
    run: echo "Done"
```

Wait for a 200 calling a HTTP url:

```yml
steps:
  wait-example-http:
    wait_http_200: https://www.google.com
    run: echo "Done"
```

You can configure the following parameters via env:

* `LUME_WAIT_HTTP_200_NUM_MAX_ATTEMPTS`
* `LUME_WAIT_HTTP_200_WAIT_SECONDS_RETRY`

e.g


```yml
steps:
  wait-example-http:
    envs: 
       LUME_WAIT_HTTP_200_NUM_MAX_ATTEMPTS: 10
       LUME_WAIT_HTTP_200_WAIT_SECONDS_RETRY: 0.5
    wait_http_200: https://www.google.com
    run: echo "Done"
```

## Acknowledgements :raised_hands:

`bowie` inspired us! 👨‍🎤 :clap:

Thanks to `bowie` development team in [Gradiant](https://github.com/Gradiant).


## Contact :mailbox_with_mail:

support@alicebiometrics.com
