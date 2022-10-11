
Performs continuos integrations steps using Python package `lume`. 

This workflow will run the following steps:

* lint
* check-requirements
* static-analysis
* test-unit
* test-integration
* test-acceptance

*Example:*

```yaml
  ci:
    uses: alice-biometrics/actions/.github/workflows/lume-ci.yml@main
    with:
      language: python
```

## Inputs

| Name                   | Requirement | Default | Description                                                                                                                              |
|------------------------| ----------- |------|------------------------------------------------------------------------------------------------------------------------------------------|
| `language`             | _required_  |      | Select the language (Use python or node)                                                                                                 |
| `lume_version`         | _optional_  | latest | Select the lume version if required. Check the [release history](https://pypi.org/project/lume/#history)                                 |
| `lume_config_filename` | _optional_  | lume.yml | In case you want to change the name of the lume configuration file or just store in another folder                                       |
| `pre_commands`         | _optional_  |  | Set additional lume commands to be executed at the begining of the required ones. Use commas if you need to execute several commands     |
| `post_setup_commands`  | _optional_  |  | Set additional lume commands to be executed after the setup and before required ones. Use commas if you need to execute several commands |
| `post_commands`        | _optional_  |  | Set additional lume commands to be executed at the end of the required ones. Use commas if you need to execute several commands          |


## Secrets

| Name                   | Requirement | Description                                                                            |
| ---------------------- |-------------| -------------------------------------------------------------------------------------- |
| `github_access_token`  | _optional_  | Only required if you need the token to be passed to requirements or dependency manager | 
| `gke_project`  | _optional_  | ID of the Google Cloud Platform project. If provided, this will configure `gcloud` to use this project ID by default for commands. |
| `gke_key`   | _optional_  | The service account key which will be used for authentication credentials. This key should be [created](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) and stored as a [secret](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets). It can be encoded as a [Base64](https://en.wikipedia.org/wiki/Base64) string or as JSON. |


## Lume Config File (Required in your repository)

To make it work, it is necessary to have a lume file in the root with at least the following commands (Python example):

```yaml
name: Testing

install:
  run: pip install --upgrade --upgrade-strategy eager -r requirements/dev-requirements.txt -r requirements/requirements.txt

steps:
  clean:
    run: echo "clean"
  lint:
    run:
      - black --check .
      - flake8 tests
  check-requirements:
    run: safety check -r requirements/requirements.txt
  test-unit:
    run: echo "test-unit"
  test-integration:
    run: echo "test-integration"
  test-acceptance:
    run: echo "test-acceptance"
```

If you want to change or fix a lume version and also execute additional lume commands, you can do it with the following code:
```yaml
  ci:
    uses: alice-biometrics/actions/.github/workflows/lume-ci.yml@main
    with:
      language: python
      lume_version: 0.5.2
      pre_commands: pre-command # should be available on lume.yml otherwise those won't be executed
      post_setup_commands: build # should be available on lume.yml otherwise those won't be executed
      post_commands: my-additional-command-1,my-additional-command-2 # should be available on lume.yml otherwise those won't be executed
```

## Workflow Code

Check current code in [lume-ci.yml](https://github.com/alice-biometrics/actions/blob/main/.github/workflows/lume-ci.yml):

```yaml
name: Lume CI

on:
  workflow_call:
    inputs:
      language:
        required: true
        type: string
        default: python
        description: Select the language (Use python or node)
      python_version:
        required: false
        type: string
        default: 3.9
      runs_on:
        required: false
        type: string
        default: ubuntu-latest
      lume_version:
        required: false
        type: string
        default: latest
      lume_config_filename:
        required: false
        type: string
        default: lume.yml
      pre_commands:
        required: false
        type: string
        default: ""
      post_setup_commands:
        required: false
        type: string
        default: ""
      post_commands:
        required: false
        type: string
        default: ""
      use_cache:
        required: false
        type: boolean
        default: true
      working_directory:
        required: false
        type: string
        default: .
    secrets:
      gke_project:
        required: false
      gke_key:
        required: false
      github_access_token:
        required: false

env:
  LUME_CONFIG_FILENAME: ${{ inputs.lume_config_filename}}
  GITHUB_ACCESS_TOKEN: ${{ secrets.github_access_token}}
  GKE_PROJECT: ${{ secrets.gke_project}}
  GKE_KEY: ${{ secrets.gke_key}}

jobs:
  lume-ci:
    name: Lume CI
    runs-on: ${{ inputs.runs_on }}
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v3

      - name: Authenticate to Google Cloud
        if: env.GKE_PROJECT && env.GKE_KEY
        uses: google-github-actions/auth@v0
        with:
          credentials_json: ${{ secrets.gke_key }}

      - name: Set up Cloud SDK
        if: env.GKE_PROJECT && env.GKE_KEY
        uses: google-github-actions/setup-gcloud@v0

      - name: Setup Python (without cache)
        if: ${{ inputs.language == 'python' && inputs.use_cache == false }}
        uses: actions/setup-python@v3
        with:
          python-version: ${{ inputs.python_version }}

      - name: Setup Python (with cache)
        if: ${{ inputs.language == 'python' && inputs.use_cache == true }}
        uses: actions/setup-python@v3
        with:
          python-version: ${{ inputs.python_version }}
          cache: pip
          cache-dependency-path: '**/*requirements.txt'

      - name: Setup Node
        uses: actions/setup-node@v3
        if: ${{ inputs.language == 'node' }}
        with:
          node-version: 12
          registry-url: https://npm.pkg.github.com
          always-auth: true
          cache: 'yarn'

      - name: Lume
        working-directory: ${{inputs.working_directory}}
        run: |
          version=${{ inputs.lume_version}}
          if [ "$version" = "latest" ]; then
              pip install -U lume
          else
              pip install -U lume==$version
          fi
      - name: Pre Commands
        if: ${{ inputs.pre_commands != '' }}
        working-directory: ${{inputs.working_directory}}
        run: |
          IFS=","
          read -r -a pre_commands <<< "${{ inputs.pre_commands}}"
          if [[ ${#pre_commands[@]} > 1 ]]; then
            for command in ${pre_commands[@]}; do lume -$command; done
          elif  [[ ${#pre_commands[@]} = 1 ]]; then
            echo "lume -$pre_commands" | bash -
          fi
      - name: Install
        working-directory: ${{inputs.working_directory}}
        run: lume -install

      - name: Setup (If required)
        working-directory: ${{inputs.working_directory}}
        run: lume -setup --no-strict

      - name: Post Setup Commands
        working-directory: ${{inputs.working_directory}}
        if: ${{ inputs.post_setup_commands != '' }}
        run: |
          IFS="," 
          read -r -a post_setup_commands <<< "${{ inputs.post_setup_commands}}"
          if [[ ${#post_setup_commands[@]} > 1 ]]; then
            for command in ${post_setup_commands[@]}; do lume -$command; done
          elif  [[ ${#post_setup_commands[@]} = 1 ]]; then
            echo "lume -$post_setup_commands" | bash -
          fi
      - name: Check Requirements
        working-directory: ${{inputs.working_directory}}
        run: lume -check-requirements

      - name: Static Analysis
        working-directory: ${{inputs.working_directory}}
        run: lume -static-analysis

      - name: Lint
        working-directory: ${{inputs.working_directory}}
        run: lume -lint

      - name: Unit Tests
        working-directory: ${{inputs.working_directory}}
        run: lume -test-unit

      - name: Integration Tests
        working-directory: ${{inputs.working_directory}}
        run: lume -test-integration

      - name: Acceptance Tests
        working-directory: ${{inputs.working_directory}}
        run: lume -test-acceptance

      - name: Post Commands
        working-directory: ${{inputs.working_directory}}
        if: ${{ inputs.post_commands != '' }}
        run: |
          IFS="," 
          read -r -a post_commands <<< "${{ inputs.post_commands}}"
          if [[ ${#post_commands[@]} > 1 ]]; then
            for command in ${post_commands[@]}; do lume -$command; done
          elif  [[ ${#post_commands[@]} = 1 ]]; then
            echo "lume -$post_commands" | bash -
          fi
```