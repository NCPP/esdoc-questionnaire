from ConfigParser import SafeConfigParser
import datetime
import time
from fabric.contrib.files import append
from fabric.state import env
from fabric.decorators import task
from fabric.operations import sudo, run
from fabric.context_managers import cd, prefix
import os


# Path to the configuration file containing secret values.
CONF_PATH = os.path.join(os.path.expanduser('~'), '.config', 'esdoc-questionnaire.conf')
parser = SafeConfigParser()
parser.read(CONF_PATH)

cfg = dict(parser.items('fabric'))

env.user = cfg['user']
env.hosts = [cfg['host']]
env.key_filename = cfg['key_filename']


def install_apt_package(name):
    sudo(to_fabric_str(['apt-get', '-y', 'install', name]))


def install_pip_package(name):
    sudo(to_fabric_str(['pip', 'install', name]))


def to_fabric_str(sequence):
    return(' '.join(sequence))


@task(default=True)
def deploy():
    # upgrade()
    # install_virtual_environment()
    # install_pip_packages()
    install_questionnaire()



@task
def launch_aws():
    import aws
    m = aws.AwsManager(conf_path=CONF_PATH)
    instance = m.launch_new_instance(cfg['aws_instance_name'])
    parser.set('fabric', 'host', instance.public_dns_name)
    parser.set('fabric', 'aws_instance_id', instance.id)
    with open(CONF_PATH, 'w') as f:
        parser.write(f)

@task
def upgrade():
    sudo('apt-get update')
    sudo('apt-get upgrade -y')

# @task
# def install_apt_packages():
#     cmd = ['apt-get','-y','install','g++','libz-dev','curl','wget','python-dev',
#            'python-pip','libgdal-dev','ipython','python-gdal','git']
#     sudo(' '.join(cmd))
            
@task
def install_virtual_environment():
    install_apt_package('python-dev')
    install_apt_package('python-pip')
    install_pip_package('virtualenv')
    install_pip_package('virtualenvwrapper')

    ## append environment information to profile file
    lines = [
    '',
    '# Set the location where the virtual environments are stored',
    'export WORKON_HOME=~/.virtualenvs',
    '# Use the virtual environment wrapper scripts',
    'source /usr/local/bin/virtualenvwrapper.sh',
    '# Tell pip to only run if there is a virtualenv currently activated',
    'export PIP_REQUIRE_VIRTUALENV=false',
    '# Tell pip to automatically use the currently active virtualenv',
    'export PIP_RESPECT_VIRTUALENV=true',
    '# Tell pip to use virtual environment wrapper storage location',
    'export PIP_VIRTUALENV_BASE=$WORKON_HOME',
            ]
    append('~/.profile', lines)
    run(to_fabric_str(['source', '~/.profile']))

    run(to_fabric_str(['mkvirtualenv', cfg['venv_name']]))


@task
def install_pip_packages():
    install_apt_package('postgresql-9.3')
    install_apt_package('postgresql-server-dev-9.3')
    install_apt_package('libxml2')
    install_apt_package('libxml2-dev')
    install_apt_package('libxslt1-dev')
    with prefix(to_fabric_str(['workon', cfg['venv_name']])):
        packages = [
                    'django',
                    'South',
                    'django-mptt',
                    'ipython',
                    'ipdb',
                    'psycopg2',
                    'lxml']
        for package in packages:
            install_pip_package(package)


@task
def install_questionnaire():
    install_apt_package('git')
    run(to_fabric_str(['mkdir', '-p', cfg['git_clone_dir']]))
    with cd(cfg['git_clone_dir']):
        run(to_fabric_str(['git', 'clone', cfg['git_url'], cfg['git_repo_name']]))
        with cd(cfg['git_repo_name']):
            run(to_fabric_str(['git', 'checkout', cfg['git_branch']]))