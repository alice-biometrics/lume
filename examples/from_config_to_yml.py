import yaml

from lume.config import Config, InstallConfig, SetupConfig, DependencyConfig, StepConfig

s_config = Config(
    name="name",
    install=InstallConfig(run=["pip install meiga"]),
    setup=SetupConfig(
        {
            "dep1": DependencyConfig(
                type="file",
                url="url",
                auth_required=True,
                credentials_env="env",
                unzip=True,
            )
        }
    ),
    steps={
        "build": StepConfig(run=["python setup_teardown.py"]),
        "test": StepConfig(run=["pytest"]),
    },
)
print(s_config.to_dict())

with open("lume_internal.yml", "w") as file:
    file.write(yaml.dump(s_config.to_dict()))
