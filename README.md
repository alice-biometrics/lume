lume 🔥  [![version](https://img.shields.io/github/release/alice-biometrics/lume/all.svg)](https://github.com/alice-biometrics/lume/releases) [![ci](https://github.com/alice-biometrics/lume/workflows/ci/badge.svg)](https://github.com/alice-biometrics/lume/actions) [![pypi](https://img.shields.io/pypi/dm/lume)](https://pypi.org/project/lume/) [![codecov](https://codecov.io/gh/alice-biometrics/lume/branch/main/graph/badge.svg?token=AS78XD634W)](https://codecov.io/gh/alice-biometrics/lume)
=====

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png?raw=true" width=auto>

A handy Python-based automation tool. 
`lume` helps you sort your commands, allows you to abstract from the development environment and facilitates CI and CD workflows. 

## Installation 💻

``` bash
pip install lume
```

## Getting Started 📈	

**lume** is a simple way to organize your daily software development operations (installation, setup, code compilation, test, etc..)

#### Configuration File

If you want to use lume in your project, just add a `lume.yml` in your root.

```yml
name: lume-sample

install:
  run: echo "Installing..."
  
uninstall:
  run: echo "Uninstalling..."

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
  -h, --help              show this help message and exit
  -v, --version           show lume version number.
  -all, --all-commands    run all commands
  -check CHECK, --check   CHECK
                          check if lume command is available or not
  -clean, --clean         clean
  -build, --build         build
  -test, --test           test
  -install, --install     install
  -uninstall, --uninstall uniinstall

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

To run uninstall:

```console
>> lume -uninstall
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

#### Check if a command is available 

You can check if a command exist use `lume -check <COMMAND-TO-CHECK>`

Example

````console
lume -check test
````

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

Or maybe for compiling a library with different flags depending on the `OS`.

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

Use `all-pre` and `all-post` to define the order of shared operations between OS.

```yml
install:
  run:
    all-pre: echo "Install pre-requirement"
    linux:
       - sudo apt update
       - sudo apt install myprogram
     macos:
       - brew install myprogram
     macos-arm:
       - brew install myprogram-arm
     all-post: echo "Everything was successfully installed"
```


> **Note**
>  When execute a cli lume command, first line will prompt something like `🔥 lume <lume-version> (<your-platform> -- Python <python-version>)`.
>  So, you can check which os-related commands are going to be executed
>  If you get `🔥 lume 0.8.8 (macos-arm -- Python 3.9.6)`, in addition to the common commands, will be executed `brew install myprogram-arm`


#### Use several lume files

Imagine you have multiple steps, and you want to split them in several files. 
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
env:
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

Use `setup` step to manage downloading and unzipping dependencies form external resources (e.g `ftp` servers, `buckets`, etc..)

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

`lume` helps you on environment variables management:
* Set required environment variables
* Define shared envs for all the steps
* Define some envs for a specific step

###### Required envs

Define some required envs. This prevents failure and will raise a clear error (`EnvironmentError`).

```yml
name: lume-sample

required_env:
  MY_REQUIRED_ENV: Neccesary to install private packages # example
  
steps:
  my-step:
    run: echo ${MY_REQUIRED_ENV}
```

###### Shared envs

Define your shared environment variables with `envs`

```yml
name: lume-sample

env:
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
    env:
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
    env_file: examples/env.yml
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
    env: 
       LUME_WAIT_HTTP_200_NUM_MAX_ATTEMPTS: 10
       LUME_WAIT_HTTP_200_WAIT_SECONDS_RETRY: 0.5
    wait_http_200: https://www.google.com
    run: echo "Done"
```

#### `--no-strict` mode

If you use lume with a command (step) that is not available on the `lume.yml`, this will fail and return an exit code 1.

However, if you use `--no-strict` mode, lume will warn you but the execution will be a success returning 0 as exit code.
You can also use the `LUME_NO_STRICT` env var to solve the same issue: `export LUME_NO_STRICT=true`

*Use Case*: This feature could be very useful if you are generalizing a continuous integration workflow. Imagine that you
have projects where you need a setup process and in others you do not. Use `lume -setup --no-strict` to avoid conflicts
in your workflow.

Additionally, the `no-strict` mode could help us to skip `required_env` strict check in some environments.

## Acknowledgements 🙌

`bowie` inspired us! 👨‍🎤 👏👏👏👏👏
Thanks to `bowie` development team in [Gradiant](https://github.com/Gradiant).

## Contact 📬

support@alicebiometrics.com
