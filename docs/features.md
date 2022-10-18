## Check if a command is available 

You can check if a command exist use `lume -check <COMMAND-TO-CHECK>`

Example when check existent command (in `lume.yml`):
<div class="termy">
```console
$ lume -check test
lume 🔥 => `test` is an available command ✅ 
```
</div>

Otherwise, if command is not available:
<div class="termy">
```console
$ lume -check not-available-command
lume 🔥 => `not-available-command` is not available command ❌ 
```
</div>


## OS-specific commands

Define your os-specific command adding new fields on `run` commands with specific os keys (`linux`, `macos`, `macos-arm` and `windows`)

Use it when installing dependencies:

```yaml
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

```yaml
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


!!! note

    When execute a cli lume command, first line will prompt something like `🔥 lume <lume-version> (<your-platform> -- Python <python-version>)`.
    So, you can check which os-related commands are going to be executed
    If you get `🔥 lume 0.8.8 (macos-arm -- Python 3.9.6)`, in addition to the common commands, will be executed `brew install myprogram-arm`


## Use several lume files

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

<div class="termy">
```console
$ lume -other:step-1
```
</div>

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

## Several commands per Step

Use the hyphen in order to define several commands per Step:

```yaml
steps:
  clean:
    run:
    - echo "Cleaning dep1"
    - echo "Cleaning dep2"
```

Or just use `|`:

```yaml
steps:
  clean:
    run: |
      echo "Cleaning dep1"
      echo "Cleaning dep2"
```

## Setup Step

Use `setup` step to manage downloading and unzipping dependencies form external resources (e.g `ftp` servers, `buckets`, etc..)

```yaml
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

## Inner Setup and Teardown

Define `setup` commands to execute operations that will be executed before `run` commands. Use `teardown` commands to define command to be executed after `run`.

```yaml
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

## Set environment variables

`lume` helps you on environment variables management:

- Set required environment variables
- Define shared envs for all the steps
- Define some envs for a specific step

### Required envs

Define some required envs. This prevents failure and will raise a clear error (`EnvironmentError`).

```yaml
name: lume-sample

required_env:
  MY_REQUIRED_ENV: Neccesary to install private packages # example
  
steps:
  my-step:
    run: echo ${MY_REQUIRED_ENV}
```

### Shared envs

Define your shared environment variables with `envs`

```yaml
name: lume-sample

env:
   MY_ENV: MY_VALUE
steps:
  my-step:
    run: echo ${MY_ENV}
```

Also, you can use a file to specify you environment variables:

```yaml
name: lume-sample

env_file: path/to/my/env/file

steps:
  my-step:
    run: echo ${MY_ENV}
```

### Step envs

```yaml
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

<div class="termy">
```console
$ lume -my-step
🔥 Step: my-step
🔸 env: set MY_ENV=MY_VALUE
💻 my-step >> echo ${MY_ENV}
    MY_VALUE
```
</div>

Note that if you previously defined an *env*, it will be overwrote during the step.

You can also define variable from external filename (e.g env.yml):

*env.yml:*
```yaml
TEST: SHARED_VALUE
MY_MANAGER: LUME
LUME_CONFIG_FILENAME: filename
```

*lume.yml:*
```yaml
steps:
  envs-file-example:
    env_file: examples/env.yml
    run: echo "${MY_ENV}"
```

## Detach Setup

With `setup_detach` option, you can execute a detached command (e.g a service). Then, after the main `run` command, this proccess will be automatically killed.

This is very useful to test services locally:

```yaml
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

## Wait


Wait few seconds with `wait_seconds`:

```yaml
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

*Example:*
```yaml
steps:
  wait-example-http:
    env: 
       LUME_WAIT_HTTP_200_NUM_MAX_ATTEMPTS: 10
       LUME_WAIT_HTTP_200_WAIT_SECONDS_RETRY: 0.5
    wait_http_200: https://www.google.com
    run: echo "Done"
```

## `--no-strict` mode

If you use lume with a command (step) that is not available on the `lume.yml`, this will fail and return an exit code 1.

However, if you use `--no-strict` mode, lume will warn you but the execution will be a success returning 0 as exit code.
You can also use the `LUME_NO_STRICT` env var to solve the same issue: `export LUME_NO_STRICT=true`

*Use Case*: This feature could be very useful if you are generalizing a continuous integration workflow. Imagine that you
have projects where you need a setup process and in others you do not. Use `lume -setup --no-strict` to avoid conflicts
in your workflow.

Additionally, the `no-strict` mode could help us to skip `required_env` strict check in some environments.