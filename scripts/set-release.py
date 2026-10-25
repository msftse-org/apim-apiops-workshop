#!/usr/bin/env python3
import pathlib,json,sys
if len(sys.argv)!=2 or sys.argv[1] not in ['v1','v2']:
 raise SystemExit('Usage: python3 scripts/set-release.py v1|v2')
p=pathlib.Path(__file__).resolve().parents[1]/'apim-artifacts/namedValues/demo-release/namedValueInformation.json'
v=json.loads(p.read_text());v['properties']['value']=sys.argv[1];p.write_text(json.dumps(v,indent=2)+'\n')
