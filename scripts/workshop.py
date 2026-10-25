#!/usr/bin/env python3
"""Reproducible APIM exercises. Uses only Python's standard library and the pinned CLI."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
FILTER_KEYS = ['apis','backends','namedValues','products','tags','versionSets','loggers',
               'diagnostics','groups','policyFragments','gateways','schemas',
               'subscriptions','policies','policyRestrictions','documentations','workspaces']

def config():
    path = Path(os.environ.get('WORKSHOP_CONFIG', ROOT / 'config.local.json'))
    if not path.exists():
        raise ValueError('Copy config.example.json to config.local.json and enter your Azure resource names.')
    c = json.loads(path.read_text())
    for key in ['subscriptionId','resourceGroup','apim','apic','location']:
        if not c.get(key) or 'YOUR-' in c[key]:
            raise ValueError(f'Configure {key} in {path.name}')
    return c

def strict_filter(path, key, values):
    path.write_text('\n'.join(f'{k}: {json.dumps(values if k == key else [])}' for k in FILTER_KEYS)+'\n')

def validate_delete_plan(plan):
    actions=plan.get('dryRun',{}).get('actions',[])
    if not (len(actions)==1 and actions[0].get('operation')=='DELETE'
            and actions[0].get('type')=='NamedValue'
            and actions[0].get('name')=='workshop-temporary'):
        raise RuntimeError('Refusing cleanup: plan must delete only the workshop-temporary named value')

class Workshop:
    def __init__(self, root=ROOT, settings=None, cli=None):
        self.root = Path(root)
        self.c = settings or config()
        self.cli = Path(cli or os.environ.get('APIOPS_CLI', ROOT/'vendor/apiops-cli/dist/cli/index.js')).resolve()
        self.logs = self.root/'.work/logs'
        self.logs.mkdir(parents=True,exist_ok=True)
        self.results = []

    def command(self, argv, cwd=None, expected=0, label=None):
        start = time.monotonic()
        env = os.environ.copy()
        # Ambient COMMIT_ID must not silently turn a full publish into incremental mode.
        env.pop('COMMIT_ID', None)
        p = subprocess.run([str(x) for x in argv], cwd=cwd or self.root, env=env,
                           text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        label = label or f'command-{len(self.results)+1:02d}'
        if not re.fullmatch(r'[a-zA-Z0-9_.-]+', label):
            raise ValueError('Invalid log label')
        (self.logs/f'{label}.stdout.txt').write_text(p.stdout)
        (self.logs/f'{label}.stderr.txt').write_text(p.stderr)
        result = {'step':label,'exitCode':p.returncode,'expectedExitCode':expected,
                  'passed':p.returncode == expected,'seconds':round(time.monotonic()-start,2)}
        self.results.append(result)
        print(json.dumps(result),flush=True)
        if p.returncode != expected:
            raise RuntimeError(f'{label} failed. Read {self.logs/label}.stdout.txt and .stderr.txt')
        return p.stdout

    def apiops(self, args, label, expected=0, cwd=None):
        if not self.cli.is_file():
            raise ValueError('Run bash scripts/install.sh first or set APIOPS_CLI.')
        out = self.command(['node',self.cli,*args],label=label,expected=expected,cwd=cwd)
        if expected != 0:
            return out
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            return out

    def target(self, apic=False):
        return ['--subscription-id',self.c['subscriptionId'],'--resource-group',self.c['resourceGroup'],
                '--service-name',self.c['apic' if apic else 'apim'],'--format','json']

    def publish(self, env='dev', preview=False, commit=None, filtered=False, label=None):
        args=['publish',*self.target(),'--source','apim-artifacts','--overrides',f'configuration.{env}.yaml']
        if preview: args += ['--dry-run']
        if commit: args += ['--commit-id',commit]
        if filtered: args += ['--filter','filter.orders-strict.yaml']
        return self.apiops(args,label or f'{env}-'+('preview' if preview else 'publish'))

    def smoke(self, env, release, route='status'):
        url=f"https://{self.c['apim']}.azure-api.net/{env}/orders/{route}"
        last={}
        for attempt in range(24):
            try:
                with urllib.request.urlopen(url,timeout=20) as r:
                    data=json.loads(r.read())
                    last={'status':r.status,'environment':r.headers.get('X-Demo-Environment'),
                          'release':r.headers.get('X-Demo-Release')}
                    if last == {'status':200,'environment':env,'release':release}:
                        if route=='echo' and not data.get('url','').endswith('/get'):
                            raise ValueError('Echo did not reach the configured /get backend')
                        result={'step':f'smoke-{env}-{release}-{route}','passed':True,**last,'attempts':attempt+1}
                        self.results.append(result)
                        print(json.dumps(result),flush=True)
                        return result
            except Exception as e:
                last={'error':str(e)}
            if attempt < 23: time.sleep(5)
        raise RuntimeError(f'Smoke assertion failed for {env}/{route}: {last}')

    def extract(self, no_transitive=False, full=False):
        dest='.work/extract-full' if full else '.work/extract-'+('exact' if no_transitive else 'dependencies')
        args=['extract',*self.target(),'--output',dest]
        if not full: args += ['--filter','filter.dev-strict.yaml']
        if no_transitive: args += ['--no-transitive']
        return self.apiops(args,'extract-'+('full' if full else 'exact' if no_transitive else 'dependencies'))

    def scratch(self, label):
        path=self.root/'.work'/f'{label}-{time.time_ns()}'
        path.mkdir(parents=True)
        for name in ['apim-artifacts','configuration.dev.yaml','configuration.qa.yaml']:
            src=self.root/name
            if src.is_dir(): shutil.copytree(src,path/name)
            else: shutil.copy2(src,path/name)
        w=Workshop(path,self.c,self.cli)
        w.results=self.results
        w.command(['git','init','-b','workshop'],label='git-init')
        w.command(['git','config','user.name','APIM Workshop Exercise'],label='git-name')
        w.command(['git','config','user.email','workshop@example.invalid'],label='git-email')
        (path/'.gitignore').write_text('.work/\n')
        return w

    def git_commit(self, message):
        self.command(['git','add','.'],label='git-add')
        self.command(['git','commit','-m',message],label='git-commit')
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.root,text=True).strip()

    def cycle(self):
        w=self.scratch('release')
        release=w.root/'apim-artifacts/namedValues/demo-release/namedValueInformation.json'
        obj=json.loads(release.read_text());obj['properties']['value']='v1';release.write_text(json.dumps(obj,indent=2)+'\n')
        w.git_commit('Baseline release v1')
        w.publish('dev',label='cycle-baseline');w.smoke('dev','v1')
        obj['properties']['value']='v2';release.write_text(json.dumps(obj,indent=2)+'\n')
        sha=w.git_commit('Change release to v2')
        try:
            report=w.publish('dev',preview=True,commit=sha,label='cycle-change-preview')
            assert report['summary']['totalPuts']==1 and report['summary']['totalDeletes']==0
            w.publish('dev',commit=sha,label='cycle-change');w.smoke('dev','v2');w.smoke('qa','v2')
        finally:
            # Restore the baseline even when the v2 verification fails.
            w.command(['git','revert','--no-edit',sha],label='git-revert')
            revert_sha=subprocess.check_output(['git','rev-parse','HEAD'],cwd=w.root,text=True).strip()
            w.publish('dev',commit=revert_sha,label='cycle-rollback');w.smoke('dev','v1')
        # Demonstrate the override-only commit trap without changing Azure.
        (w.root/'configuration.dev.yaml').write_text((w.root/'configuration.dev.yaml').read_text()+'\n# override-only exercise\n')
        override_sha=w.git_commit('Change only override configuration')
        report=w.publish('dev',preview=True,commit=override_sha,label='override-only-preview')
        assert report['summary']['totalPuts']==0

    def guards(self):
        w=self.scratch('guards')
        fixture=w.root/'fixture/namedValues/workshop-temporary/namedValueInformation.json'
        fixture.parent.mkdir(parents=True)
        fixture.write_text(json.dumps({'properties':{'displayName':'workshop-temporary-synthetic','secret':True,'value':'WORKSHOP-NOT-A-CREDENTIAL'}},indent=2)+'\n')
        w.git_commit('Add a disposable synthetic named value')
        args=['publish',*w.target(),'--source','fixture','--overrides','configuration.dev.yaml']
        created=False
        try:
            w.apiops(args,'temporary-publish');created=True
            strict_filter(w.root/'temporary.yaml','namedValues',['dev-workshop-temporary'])
            extract=['extract',*w.target(),'--output','.work/secret-extract','--filter','temporary.yaml']
            w.apiops(extract,'secret-extract')
            saved=w.root/'.work/secret-extract/namedValues/dev-workshop-temporary/namedValueInformation.json'
            assert json.loads(saved.read_text())['properties']['value']=='*** REDACTED ***'
            w.apiops(['publish',*w.target(),'--source','.work/secret-extract','--dry-run'],'redaction-guard',expected=2)
            w.apiops(['publish',*w.target(),'--source','fixture','--filter','temporary.yaml','--delete-unmatched','--dry-run'],'filter-delete-guard',expected=2)
        finally:
            if created:
                fixture.unlink()
                sha=w.git_commit('Remove only the workshop temporary value')
                # Pin one commit and assert its entire delete plan before execution.
                cleanup=[*args,'--commit-id',sha,'--delete-unmatched']
                plan=w.apiops([*cleanup,'--dry-run'],'delete-preview')
                validate_delete_plan(plan)
                w.apiops(cleanup,'delete-one-resource')
                w.apiops([*extract,'--remove-stale'],'remove-stale')
                assert not saved.exists()

    def apic(self):
        target=self.target(apic=True)
        self.apiops(['apic','publish',*target,'--source','apic-artifacts','--dry-run'],'apic-seed-preview')
        self.apiops(['apic','publish',*target,'--source','apic-artifacts'],'apic-seed')
        self.apiops(['apic','extract',*target,'--output','.work/apic-backup'],'apic-backup')
        assert list((self.root/'.work/apic-backup').rglob('specification.*'))
        self.apiops(['apic','publish',*target,'--source','.work/apic-backup','--dry-run'],'apic-replay-preview')
        self.apiops(['apic','publish',*target,'--source','.work/apic-backup'],'apic-replay')
        self.apiops(['apic','extract',*target,'--output','.work/apic-metadata','--workspace','default','--no-specifications'],'apic-metadata-only')
        assert not list((self.root/'.work/apic-metadata').rglob('specification.*'))
        self.apiops(['apic','publish',*target,'--source','.work/apic-metadata','--no-specifications'],'apic-publish-metadata')

    def scaffold(self):
        for provider in ['github-actions','azure-devops']:
            folder=self.root/'.work'/f'scaffold-{provider}-{time.time_ns()}'
            folder.mkdir(parents=True)
            args=['init','--ci',provider,'--environments','dev,qa','--non-interactive']
            self.apiops(args,f'init-{provider}',cwd=folder)
            assert list((folder/'.github/prompts').glob('*.prompt.md'))
            assert (folder/'configuration.dev.yaml').exists()
            # Existing generated files must not be overwritten silently.
            self.apiops(args,f'init-conflict-{provider}',expected=1,cwd=folder)
            self.apiops([*args,'--force'],f'init-force-{provider}',cwd=folder)
            print(f'Generated {provider} files: {folder}',flush=True)

    def doctor(self):
        for cmd in [['node','--version'],['npm','--version'],['git','--version'],['az','version']]:
            self.command(cmd,label='doctor-'+cmd[0])
        self.apiops(['--version'],'cli-version')
        self.command(['az','account','show','--subscription',self.c['subscriptionId'],'--query','id','-o','tsv'],label='azure-account')
        self.command(['az','apim','show','--subscription',self.c['subscriptionId'],'-g',self.c['resourceGroup'],'-n',self.c['apim'],'--query','provisioningState','-o','tsv'],label='apim-ready')

    def validate_live(self):
        self.doctor()
        for env in ['dev','qa']:
            self.publish(env,preview=True);self.publish(env)
        self.smoke('dev','v1');self.smoke('qa','v2');self.smoke('dev','v1','echo')
        self.cycle()
        self.extract(full=True)
        deps=self.extract();exact=self.extract(no_transitive=True)
        assert deps['summary']['totalExtracted'] > exact['summary']['totalExtracted']
        self.publish(filtered=True,preview=True,label='filtered-preview')
        self.publish(filtered=True,label='filtered-publish')
        # Exercise wildcard + exclusion matching on real named values.
        f=self.root/'.work/filter-patterns.yaml'
        strict_filter(f,'namedValues',['dev-*','!dev-demo-release'])
        self.apiops(['extract',*self.target(),'--output','.work/patterns','--filter',str(f)],'wildcard-exclusion')
        names=[p.parent.name for p in (self.root/'.work/patterns/namedValues').glob('*/namedValueInformation.json')]
        assert 'dev-demo-environment' in names and 'dev-demo-release' not in names
        self.guards();self.apic();self.scaffold()
        self.smoke('dev','v1');self.smoke('qa','v2')

    def save_report(self, completed):
        report={'date':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'cliCommit':'129fb326e6878c2bedd45e8ae4ccb8526de688a4',
                'completed':completed,'checks':self.results,
                'scope':'Executed against an existing APIM Consumption instance and API Center Free instance. Resource creation and whole-group deletion are separate.'}
        (self.root/'.work/validation.json').write_text(json.dumps(report,indent=2)+'\n')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['doctor','status','preview','publish','incremental','extract','cycle','guards','apic','scaffold','validate-live'])
    p.add_argument('--env',choices=['dev','qa'],default='dev')
    p.add_argument('--commit')
    p.add_argument('--no-transitive',action='store_true')
    p.add_argument('--full',action='store_true')
    p.add_argument('--filter',action='store_true')
    a=p.parse_args()
    if a.action=='incremental' and not a.commit:p.error('incremental requires --commit SHA')
    w=Workshop();completed=False
    try:
        if a.action=='doctor':w.doctor()
        elif a.action=='status':w.smoke('dev','v1');w.smoke('qa','v2')
        elif a.action in ['preview','publish','incremental']:
            w.publish(a.env,preview=a.action=='preview',commit=a.commit,filtered=a.filter)
        elif a.action=='extract':w.extract(a.no_transitive,a.full)
        else:getattr(w,a.action.replace('-','_'))()
        completed=True
    finally:w.save_report(completed)

if __name__=='__main__':
    try:main()
    except (ValueError,RuntimeError,AssertionError) as e:
        print(f'ERROR: {e}',file=sys.stderr);sys.exit(1)
