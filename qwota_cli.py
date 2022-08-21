import re
from kubernetes import config
from openshift.dynamic import DynamicClient


def cli():
    k8s = config.new_client_from_config(context=current_context()['name'])
    oc = DynamicClient(k8s)
    v1_acrq = oc.resources.get(api_version='v1', kind='AppliedClusterResourceQuota')
    acrq = v1_acrq.get(namespace=current_namespace(), pretty=False)
    for acrq_item in acrq.get('items'):
        if '--terminating' in acrq_item.get('metadata').get('name'):
            continue
        status = acrq_item.get('status').get('total')
        for quota_key in status.get('hard').keys():
            used = status.get('used').get(quota_key)
            hard = status.get('hard').get(quota_key)
            used_int = int_value(used)
            hard_int = int_value(hard)
            if used_int == 0:
                continue

            usage_str = graph(used_int, hard_int)

            print(f'{usage_str}  {quota_key} ({used} of {hard})')


def current_context():
    return config.list_kube_config_contexts()[1]


def current_namespace():
    return current_context()['context']['namespace']


def int_value(value):
    only_digits = int(re.sub('[^\d]', '', value))
    if 'k' in value:
        return only_digits * 1000
    if 'Gi' in value:
        return only_digits * 1000
    if 'Mi' in value:
        return only_digits
    if 'm' in value:
        return only_digits / 1000
    return int(only_digits)


def graph(used, hard):
    usage_p = round((used / hard) * 100)
    usage = '.' * (round(usage_p / 10)*2)
    blanks = ' ' * (20 - len(usage))
    return f'|{usage}{blanks}|'


if __name__ == '__main__':
    cli()
