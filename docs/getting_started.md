**lume** is a simple way to organize your daily software development operations (installation, setup, code compilation, test, etc..)

## Configuration File

If you want to use lume in your project, just add a `lume.yml` in your root.

```yaml
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

```yaml
settings:
  show_exit_code: True
```

Use `help` to know `lume` available commands. `lume` is dynamic, so the steps we are defining will be shown here automatically.

<div class="termy">

```console
$ lume --help
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
</div>

!!! note 
    In case you want to change the name of the lume configuration file or just store in another folder, please use `LUME_CONFIG_FILENAME` environment variable.
    
    <div class="termy">

    ```console
    $ export LUME_CONFIG_FILENAME=examples/lume-sample.yml
    $ lume --help
    ```
    </div>

## Run Defined Steps

To run install:

<div class="termy">
```console
$ lume -install
```
</div>

To run uninstall:

<div class="termy">
```console
$ lume -uninstall
```
</div>

To run all the steps:

<div class="termy">
```console
$ lume -all
```
</div>

Of course, you can run every step individually:

<div class="termy">
```console
$ lume -clean
```
</div>

Or several steps:

<div class="termy">
```console
$ lume -build -test
```
</div>

Here is an example of the log output that would have lume using several commands defined previously on [Configuration File](#configuration-file):

<div class="termy">
```console
$ lume -install -all
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
</div>
