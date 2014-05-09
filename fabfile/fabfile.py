from ConfigParser import SafeConfigParser
import datetime
import time
from fabric.contrib.files import append
from fabric.state import env
from fabric.decorators import task
from fabric.operations import sudo, run, put, local
from fabric.context_managers import cd, prefix, settings
import os


# Path to the configuration file containing secret values.
CONF_PATH = os.path.join(os.path.expanduser('~'), '.config', 'esdoc-questionnaire.conf')
env.parser = SafeConfigParser()
env.parser.read(CONF_PATH)
env.cfg = dict(env.parser.items('fabric'))


env.user = env.cfg['user']
env.hosts = [env.cfg['host']]
env.key_filename = env.cfg['key_filename']


def install_apt_package(name):
    sudo(to_fabric_str(['apt-get', '-y', 'install', name]))


def install_pip_package(name):
    sudo(to_fabric_str(['pip', 'install', name]))


def to_fabric_str(sequence):
    return(' '.join(sequence))


@task(default=True)
def deploy():
    upgrade()
    install_virtual_environment()
    install_pip_packages()
    install_questionnaire(CONF_PATH)
    run_questionnaire_tests()


@task
def launch_aws():
    import aws
    m = aws.AwsManager(conf_path=CONF_PATH)
    instance = m.launch_new_instance(env.cfg['aws_instance_name'])
    env.parser.set('fabric', 'host', instance.public_dns_name)
    env.parser.set('fabric', 'aws_instance_id', instance.id)
    with open(CONF_PATH, 'w') as f:
        env.parser.write(f)


@task
def upgrade():
    sudo('apt-get update')
    sudo('apt-get upgrade -y')


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

    run(to_fabric_str(['mkvirtualenv', env.cfg['venv_name']]))


@task
def install_pip_packages():
    install_apt_package('postgresql-9.3')
    install_apt_package('postgresql-server-dev-9.3')
    install_apt_package('libxml2')
    install_apt_package('libxml2-dev')
    install_apt_package('libxslt1-dev')
    with prefix(to_fabric_str(['workon', env.cfg['venv_name']])):
        packages = [
                    'django',
                    'South',
                    'django-mptt',
                    'ipython',
                    'ipdb',
                    'psycopg2',
                    'lxml',
                    'guppy',
                    'pillow',
                    'django-authopenid',
                    ]
        for package in packages:
            install_pip_package(package)


@task
def install_questionnaire(host_conf_path):
    install_apt_package('git')
    run(to_fabric_str(['mkdir', '-p', env.cfg['git_clone_dir']]))
    run('mkdir ~/.config')

    with settings(sudo_user="postgres"):
        sudo(to_fabric_str(['createuser', '-s', env.cfg['user']]))

    ## create the default database for the root user. required to run psql on the server.
    run('createdb')

    ## create the django project database
    run(to_fabric_str(['createdb', env.parser.get('database', 'name')]))

    ## copy the configuration file to the remote host
    put(local_path=host_conf_path, remote_path='~/.config/esdoc-questionnaire.conf')

    sql = '''"CREATE ROLE {0} LOGIN SUPERUSER ENCRYPTED PASSWORD '{1}';"'''.format(env.parser.get('database', 'user'), env.parser.get('database', 'password', raw=True))
    run(to_fabric_str(['psql', '-c', sql]))

    with cd(env.cfg['git_clone_dir']):
        run(to_fabric_str(['git', 'clone', env.cfg['git_url'], env.cfg['git_repo_name']]))
        with cd(env.cfg['git_repo_name']):
            run(to_fabric_str(['git', 'checkout', env.cfg['git_branch']]))
            with cd('CIM_Questionnaire'):
                with prefix(to_fabric_str(['workon', env.cfg['venv_name']])):
                    run('python manage.py syncdb --noinput')


@task
def run_questionnaire_tests():
    dirs = ['git_clone_dir', 'git_repo_name']
    app_path = os.path.join(*[env.cfg[d] for d in dirs]+['CIM_Questionnaire'])
    with cd(app_path):
        with prefix(to_fabric_str(['workon', env.cfg['venv_name']])):
            run('python manage.py test')
