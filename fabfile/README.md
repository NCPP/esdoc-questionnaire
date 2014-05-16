### Install steps:

1. Fill in ``./esdoc-questionnaire.conf.TEMPLATE`` and place in a preferred directory remove the ".TEMPLATE".
2. In ``fabile.py`` set the ``CONF_PATH`` variable to the path of the configuration file.
3. Run the following terminal command in the ``fabfile`` directory:

```sh
fab deploy
```

### (OPTIONAL) Launching and using an AWS instance for deployment:

Use the ``fabric`` command ``fab launch_aws:name=<instance_name>`` (where "instance_name" is the name of the instance to create on AWS) before the standard deploy command above:

```sh
fab launch_aws:name=my_instance
```
