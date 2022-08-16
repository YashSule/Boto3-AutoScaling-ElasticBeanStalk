from msilib.schema import Environment
from urllib import response
import boto3


elasticbeanstalk = boto3.client('elasticbeanstalk')
autoscaling = boto3.client("autoscaling")

arnList =[]
allTags =[]
results =[]
finalIds =[]
asgNames = []

aboutEnv = elasticbeanstalk.describe_environments()

for x in aboutEnv["Environments"]:
    arnList.append(x["EnvironmentArn"])

print(arnList)

for x in arnList:
    environment_tag = elasticbeanstalk.list_tags_for_resource(ResourceArn = x)["ResourceTags"]
    allTags.append(environment_tag)
    for y in environment_tag:
        if y["Key"] == "environment" and y["Value"] == "dev":
            results.append(environment_tag)

print('----------------')
print(allTags)
print('----------------')
print(results)

for x in results:
    for y in x:
        if y["Key"] == "elasticbeanstalk:environment-id":
            idaa = y["Value"]
            finalIds.append(idaa)

print('----------------')
print(finalIds)

for x in finalIds:
    env_resources = elasticbeanstalk.describe_environment_resources(
        EnvironmentId = x
    )
    asgNames.append(env_resources["EnvironmentResources"]["AutoScalingGroups"][0]["Name"])

print('----------------')
print(asgNames)


for x in asgNames:
    asgResponse = autoscaling.update_auto_scaling_group(
        AutoScalingGroupName = x,
        MinSize = 0,
        MaxSize = 0
    )
    print(asgResponse)


