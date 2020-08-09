import boto3
import botocore.exceptions
import json
import string
import random

# Script to opt-out of AI Sharing with AWS. 
# https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_ai-opt-out.html

# Defines the boto3 client for Organizations
client = boto3.client('organizations')

# Gets the root of the organization, need for 
def list_roots():
    response = client.list_roots()
    return response['Roots'][0]['Id']

# Enables the policy type to allow setting a policy for AI opt-out.
def enable_policy_type():
    rootid=list_roots()
    try:
        response = client.enable_policy_type(
            RootId=rootid,
            PolicyType='AISERVICES_OPT_OUT_POLICY'
        )
    except botocore.exceptions.ClientError as error:
        print('Policy type have already been enabled')
        return error
    else:
        print('Successfully enabled the policy type.')
        return response


# Defines the policy with default scope to opt-out from sharing information on all services
ai_services_policy = {
    "services": {
        "default": {
            "opt_out_policy": {
                "@@assign": "optOut"
            }
        }
    }
}
ai_services_policy = json.dumps(ai_services_policy)




# Creates the AI Opt-Out policy
def create_policy():
    try:
        uid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        response = client.create_policy(
            Content=ai_services_policy,
            Description='Organization Policy to opt-out of AI sharing',
            Name='ai-opt-out-'+uid,
            Type='AISERVICES_OPT_OUT_POLICY'
        )
    except botocore.exceptions.ClientError as error:
        print('A policy with duplicate name already exists..')
        return error
    else:
        print('Policy has been created.. needs to be attached before it takes effect.')
        print(response)
        return response ['Policy']['PolicySummary']['Id']

# Attaches the policy that has been created
def attach_policy():
    policyId = create_policy()
    targetId = list_roots()
    try:
        response = client.attach_policy(
            PolicyId=policyId,
            TargetId=targetId
        )
    except botocore.exceptions.ClientError as error:
        print('The policy has already been attached or no policyId was returned.. skipping.')
        raise  error
    else:
        print('AI Opt-Out policy has been successfully attached to the organizations root.')
        print(response)
        return response
        


if __name__ == '__main__':
    list_roots
    enable_policy_type()
    attach_policy()
