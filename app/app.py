from flask import Flask
from flask import request, render_template, redirect
import os
import boto3
import random
import time

class Config(object):
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_ECS_CLUSTER = 'cloud-desktop-demo'
    AWS_TASK_FAMILY = 'novnc-desktop'
    AWS_REGION = 'us-east-1'

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    resp = {}
    if request.method == 'POST':
        resp = start_new_task()
        time.sleep(2)
        return redirect('/')

    tasks = get_current_tasks()
    return render_template('index.html', tasks=tasks, resp=resp)

def start_new_task():
    client = boto3.client('ecs', region_name=app.config['AWS_REGION'])
    return client.run_task(
        cluster=app.config['AWS_ECS_CLUSTER'],
        taskDefinition=app.config['AWS_TASK_FAMILY'],
        count=1
    )

def get_current_tasks():
    tasks = []
    
    client = boto3.client('ecs', region_name=app.config['AWS_REGION'])
    response = client.list_tasks(
        cluster=app.config['AWS_ECS_CLUSTER'],
        family=app.config['AWS_TASK_FAMILY'],
        desiredStatus='RUNNING'
    )
    arns = response['taskArns']

    if not arns:
        return tasks

    response = client.describe_tasks(cluster=app.config['AWS_ECS_CLUSTER'], tasks=arns)

    for task in response['tasks']:
        try:
            tasks.append({
                'containerInstanceArn': task['containerInstanceArn'],
                'port': task['containers'][0]['networkBindings'][0]['hostPort'],
                'name': task['containers'][0]['name']
            })
        except:
            pass

    for task in tasks:
        task['ip'] = get_container_ip(task['containerInstanceArn'])

    return tasks

def get_container_ip(containerInstanceArn):
    client = boto3.client('ecs', region_name=app.config['AWS_REGION'])
    response = client.describe_container_instances(cluster=app.config['AWS_ECS_CLUSTER'],
        containerInstances=[containerInstanceArn])
    ec2InstanceId = response['containerInstances'][0]['ec2InstanceId']
    ec2_client = boto3.client('ec2', region_name=app.config['AWS_REGION'])
    response = ec2_client.describe_instances(InstanceIds=[ec2InstanceId])
    return response['Reservations'][0]['Instances'][0]['PublicIpAddress']

if __name__ == '__main__':
    app.run()