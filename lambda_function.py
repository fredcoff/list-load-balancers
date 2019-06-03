import json
import boto3

client = boto3.client('elbv2')

"""
- LoadbalancerARN
- ListenerARN
- TargetARN
- Identify all Listeners for each loadBalancer
- Identify all Targets for each loadBalancer.
"""

def get_listeners(lb_arn):
    listeners = []
    
    response = client.describe_listeners(LoadBalancerArn=lb_arn, PageSize=400)
    while True:
        for listener in response['Listeners']:
            listeners.append(listener['ListenerArn'])
        
        next_marker = response['NextMarker'] if 'NextMarker' in response else None
        if not next_marker:
            break
        
        response = client.describe_listeners(LoadBalancerArn=lb_arn, Marker=next_marker, PageSize=400)
    
    return listeners

def get_target_groups(lb_arn):
    target_groups = []
    
    response = client.describe_target_groups(LoadBalancerArn=lb_arn, PageSize=400)
    while True:
        for target_group in response['TargetGroups']:
            target_groups.append(target_group['TargetGroupArn'])
        
        next_marker = response['NextMarker'] if 'NextMarker' in response else None
        if not next_marker:
            break
        
        response = client.describe_target_groups(LoadBalancerArn=lb_arn, Marker=next_marker, PageSize=400)
    
    return target_groups

def get_load_balancers():
    load_balancers = []
    
    response = client.describe_load_balancers(PageSize=400)
    while True:
        obj = {}
        
        for desc in response['LoadBalancers']:
            obj['LoadBalancerArn'] = desc['LoadBalancerArn']
            
            obj['Listeners'] = get_listeners(obj['LoadBalancerArn'])
            
            obj['TargetGroups'] = get_target_groups(obj['LoadBalancerArn'])
            
            load_balancers.append(obj)

        next_marker = response['NextMarker'] if 'NextMarker' in response else None
        if not next_marker:
            break
            
        response = client.describe_load_balancers(Marker=next_marker, PageSize=400)
    
    return load_balancers
    
        
def lambda_handler(event, context):
    
    return {
        'statusCode': 200,
        'body': json.dumps(get_load_balancers())
    }
