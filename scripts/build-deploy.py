#!/usr/bin/env python3
"""Gera a pasta dist/ pronta para o Cloudflare (Workers static assets).
Renomeia arquivos com ?, & e = no nome (herança do clone Shopify) e reescreve as referências.
Uso: python3 scripts/build-deploy.py && cd dist && npx wrangler deploy
"""
import os, shutil, urllib.parse
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); DIST=os.path.join(ROOT,'dist')
shutil.rmtree(DIST,ignore_errors=True)
shutil.copytree(ROOT,DIST,ignore=shutil.ignore_patterns('.bak','.git','.gitignore','.wrangler','dist','scripts','.DS_Store','node_modules','README.md'))
os.chdir(DIST)
open('wrangler.jsonc','w').write('{ "name": "true-wellnes-website", "compatibility_date": "2026-09-15", "observability": { "enabled": true }, "assets": { "directory": "." } }\n')
def safe(n): return n.replace('?','-q-').replace('&','-and-').replace('=','-')
renamed={}
for dp,dn,fn in os.walk('.'):
    for f in fn:
        if any(c in f for c in '?&='): os.rename(os.path.join(dp,f),os.path.join(dp,safe(f))); renamed[f]=safe(f)
variants={}
for old,new in renamed.items():
    for v in (old, old.replace('?','%3F').replace('&','%26'), old.replace('?','%3F').replace('&','&amp;'), old.replace('&','&amp;'), urllib.parse.quote(old), urllib.parse.quote(old,safe='=')): variants[v]=new
keys=sorted(variants,key=len,reverse=True)
for dp,dn,fn in os.walk('.'):
    for f in fn:
        if not f.endswith(('.html','.css','.js','.svg','.json','.xml')): continue
        p=os.path.join(dp,f); t=open(p,encoding='utf-8',errors='surrogateescape').read(); o=t
        for k in keys:
            if k in t: t=t.replace(k,variants[k])
        if t!=o: open(p,'w',encoding='utf-8',errors='surrogateescape').write(t)
print('dist/ pronto:',len(renamed),'arquivos renomeados')
