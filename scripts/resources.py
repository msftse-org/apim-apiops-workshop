#!/usr/bin/env python3
"""Create the two low-cost workshop resources, inspect them, or explicitly delete the group."""
import argparse,json,subprocess
from workshop import config

def az(*args, allow_missing=False):
    p=subprocess.run(['az',*args],text=True,capture_output=True)
    if p.returncode:
        if allow_missing and ('ResourceNotFound' in p.stderr or 'ResourceGroupNotFound' in p.stderr):return None
        raise RuntimeError(p.stderr)
    return json.loads(p.stdout) if p.stdout.strip() else None

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['plan','provision','list','cleanup'])
    p.add_argument('--delete-resource-group',help='Must exactly match the configured group for cleanup')
    a=p.parse_args();c=config()
    sub=c['subscriptionId'];rg=c['resourceGroup']
    if a.action=='plan':
        print(json.dumps({'resourceGroup':rg,'location':c['location'],'APIM':{'name':c['apim'],'sku':'Consumption'},'API Center':{'name':c['apic'],'sku':'Free'}},indent=2));return
    if a.action=='list':
        print(json.dumps(az('resource','list','--subscription',sub,'-g',rg,'--query','[].{name:name,type:type}','-o','json'),indent=2));return
    if a.action=='cleanup':
        if a.delete_resource_group != rg:p.error('cleanup requires --delete-resource-group with the exact configured group name')
        group=az('group','show','--subscription',sub,'-n',rg,'-o','json')
        if group.get('tags',{}).get('purpose') not in ['apim-apiops-workshop','apiops-demo']:
            raise ValueError('Refusing deletion: resource group does not have the workshop purpose tag')
        az('group','delete','--subscription',sub,'-n',rg,'--yes','-o','none');return
    exists=az('group','exists','--subscription',sub,'-n',rg,'-o','json')
    if not exists:az('group','create','--subscription',sub,'-n',rg,'-l',c['location'],'--tags','purpose=apim-apiops-workshop','-o','json')
    current=az('apim','show','--subscription',sub,'-g',rg,'-n',c['apim'],'-o','json',allow_missing=True)
    if current is None:
        if not c.get('publisherEmail'):raise ValueError('Set publisherEmail in config.local.json')
        current=az('apim','create','--subscription',sub,'-g',rg,'-n',c['apim'],'-l',c['location'],
                   '--sku-name','Consumption','--sku-capacity','0','--publisher-name','APIM Workshop',
                   '--publisher-email',c['publisherEmail'],'--tags','purpose=apim-apiops-workshop','-o','json')
    uri=f"https://management.azure.com/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.ApiCenter/services/{c['apic']}?api-version=2024-03-01"
    center=az('rest','--method','get','--url',uri,allow_missing=True)
    if center is None:
        center=az('rest','--method','put','--url',uri,'--body',json.dumps({'location':c['location'],'sku':{'name':'Free'},'properties':{},'tags':{'purpose':'apim-apiops-workshop'}}))
    print(json.dumps({'apim':current.get('provisioningState',current.get('properties',{}).get('provisioningState')),'apiCenter':center.get('properties',{}).get('provisioningState'),'existingResourcesReused':True},indent=2))

if __name__=='__main__':main()
