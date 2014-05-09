from ConfigParser import SafeConfigParser
import os
import boto.ec2
from boto.ec2.autoscale import LaunchConfiguration
import datetime
import time


class AwsManager(object):

    def __init__(self, conf_path, filtered=True, allow_terminated=False):
        self.conf_path = conf_path
        self.filtered = filtered
        self.allow_terminated = allow_terminated
        self._conn = None
        self._parser = SafeConfigParser()
        self._parser.read(self.conf_path)
        self._cfg = dict(self._parser.items('aws'))

    @property
    def conn(self):
        if self._conn is None:
            self._conn = self._get_aws_connection_()
        return(self._conn)

    def _get_newest_instance_(self):
        instances = self.get_instances()
        launch_times = {i.id: datetime.datetime.strptime(i.launch_time, '%Y-%m-%dT%H:%M:%S.%fZ') for i in instances.values()}
        newest_time = max(launch_times.values())
        newest_instance_id = {i: t for i, t in launch_times.iteritems() if t == newest_time}.keys()[0]
        return(instances[newest_instance_id])

    def get_instances(self):
        reservations = self.conn.get_all_reservations()
        instances = [i for r in reservations for i in r.instances]
        instances = {i.id: i for i in instances}
        if not self.allow_terminated:
            instances = {i.id: i for i in instances.values() if i._state.name != 'terminated'}
        if self.filtered:
            instances = {i.id: i for i in instances.values() if self._filter_(i)}
        return(instances)

    def _filter_(self, instance):
        if instance.key_name == self._cfg['key_name']:
            ret = True
        else:
            ret = False
        return(ret)

    def _get_aws_connection_(self):
        region = 'us-west-2'

        aws_access_key_id = self._cfg['access_key_id']
        aws_secret_access_key = self._cfg['secret_access_key']

        conn = boto.ec2.connect_to_region(region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        if conn is None:
            raise(RuntimeError('Unable to launch instance.'))

        return(conn)

    def launch_new_instance(self, name, wait=True):
        image_id = 'ami-6ac2a85a'
        security_group = 'ocgis'
        instance_type = 't1.micro'
        key_name = self._cfg['key_name']
        self.conn.run_instances(image_id, key_name=key_name, instance_type=instance_type, security_groups=[security_group])
        newest_instance = self._get_newest_instance_()
        self.conn.create_tags([newest_instance.id], {"Name": name})

        if wait:
            status = newest_instance.update()
            while status != 'running':
                time.sleep(1)
                status = newest_instance.update()

        return(newest_instance)