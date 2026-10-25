#!/usr/bin/env python3
"""Validate workshop artifact contracts and local documentation links without Azure access."""
import json,re,sys,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    checks=0
    for p in list((ROOT/'apim-artifacts').rglob('*.json'))+list((ROOT/'apic-artifacts').rglob('*.json')):
        json.loads(p.read_text());checks+=1
    for p in (ROOT/'apim-artifacts').rglob('*.xml'):
        ET.fromstring(p.read_text());checks+=1
    api=ROOT/'apim-artifacts/apis/demo-orders'
    spec=json.loads((api/'specification.json').read_text())
    op_ids={operation['operationId'] for path in spec['paths'].values() for method,operation in path.items() if method in ['get','post','put','delete','patch']}
    assert {'get-status','get-echo'} <= op_ids
    assert {p.name for p in (api/'operations').iterdir()} <= op_ids
    release=json.loads((ROOT/'apim-artifacts/namedValues/demo-release/namedValueInformation.json').read_text())
    assert release['properties']['value']=='v1','Public baseline must remain v1'
    qa=(ROOT/'configuration.qa.yaml').read_text();assert 'namePrefix: "qa-"' in qa and 'value: "v2"' in qa
    for p in [ROOT/'filter.dev-strict.yaml',ROOT/'filter.orders-strict.yaml']:
        FILTER_KEYS=['apis', 'backends', 'namedValues', 'products', 'tags', 'versionSets', 'loggers', 'diagnostics', 'groups', 'policyFragments', 'gateways', 'schemas', 'subscriptions', 'policies', 'policyRestrictions', 'documentations', 'workspaces']
        assert set(re.findall(r'^(\w+):',p.read_text(),re.M))==set(FILTER_KEYS)
        checks+=1
    for p in [ROOT/'README.md',*(ROOT/'docs').rglob('*.md')]:
        text=p.read_text()
        for link in re.findall(r'\]\(([^)]+)\)',text):
            if ':' in link or link.startswith('#'):continue
            path=link.split('#')[0]
            assert (p.parent/path).exists(),f'Broken link in {p}: {link}'
            checks+=1
    # Syntax-check the real Bash examples without running Azure commands.
    for p in (ROOT/'docs/labs').glob('*.md'):
        for index, block in enumerate(re.findall(r'```bash\n(.*?)```', p.read_text(), re.S), 1):
            result = subprocess.run(['bash', '-n'], input=block, text=True, capture_output=True)
            assert result.returncode == 0, f'Invalid Bash in {p.name} block {index}: {result.stderr}'
            checks += 1
    # Inspect only publishable text, never config.local.json or runtime logs.
    for folder in ['apim-artifacts','apic-artifacts','examples','docs','tests','validation']:
        for p in (ROOT/folder).rglob('*'):
            if not p.is_file() or p.suffix in ['.pptx','.png','.pyc']:continue
            text=p.read_text()
            assert not re.search(r'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.',text),f'Possible JWT: {p}'
            assert not re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',text),f'Private key: {p}'
            assert not re.search(r'gh[pousr]_[A-Za-z0-9]{30,}',text),f'Possible GitHub credential: {p}'
    print(json.dumps({'passed':True,'artifactAndLinkChecks':checks,'scope':'JSON/XML contracts, baseline, filters, local links, Bash syntax and credential patterns'},indent=2))

if __name__=='__main__':main()
