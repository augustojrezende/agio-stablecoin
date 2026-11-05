from pathlib import Path
import os,json,hashlib,shutil,subprocess,datetime,venv
src=Path('/Users/augustojrezende/Projetos/agio-stablecoin');dst=src.with_name('agio-stablecoin_v2')
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def git(*args):return subprocess.check_output(['git',*args],cwd=src,env=env,text=True)
assert git('rev-parse','HEAD').strip()=='543fdea26bc734fbea6d0fa712e5213c0d75d06a'
assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
assert not dst.exists(),'V2 já existe: não sobrescrever'
skip={'.venv','__pycache__','.pytest_cache'}
# Include physical Git objects and every source/data/audit file. No symlinks outside the recreated environment.
links=[str(p) for p in src.rglob('*') if p.is_symlink() and '.venv' not in p.relative_to(src).parts]
assert not links,links
files=[p for p in src.rglob('*') if p.is_file() and not any(x in skip for x in p.relative_to(src).parts)]
h={str(p.relative_to(src)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
shutil.copytree(src,dst,symlinks=False,ignore=lambda d,n:[x for x in n if x in skip])
copyhash={p:hashlib.sha256((dst/p).read_bytes()).hexdigest() for p in h};assert copyhash==h
assert all((src/p).stat().st_ino!=(dst/p).stat().st_ino for p in h)
a=dst/'auditorias/AUD-002';a.mkdir()
(a/'hashes_original_antes.json').write_text(json.dumps(h,indent=2));(a/'hashes_copia_inicial.json').write_text(json.dumps(copyhash,indent=2));(a/'git_original_inicial.txt').write_text(git('status','--short','--untracked-files=all'))
(a/'inventario_original.json').write_text(json.dumps([{'arquivo':str(p.relative_to(src)),'bytes':p.stat().st_size} for p in files],indent=2))
# Preserve complete scientific/code baseline locally for comparisons and regression-before tests.
snapshot=a/'baseline_original';snapshot.mkdir()
for n in ['src','tests','scripts','dados','docs','pyproject.toml','README.md']:
 p=dst/n
 if p.is_dir():shutil.copytree(p,snapshot/n)
 else:shutil.copy2(p,snapshot/n)
# Independent virtual environment created without downloads; physical copies of the installed dependency versions.
base='/opt/homebrew/opt/python@3.14/bin/python3.14'
subprocess.run([base,'-m','venv','--copies',str(dst/'.venv')],check=True,env=env)
old=next((src/'.venv/lib').glob('python*/site-packages'));new=next((dst/'.venv/lib').glob('python*/site-packages'))
shutil.copytree(old,new,dirs_exist_ok=True,symlinks=False,ignore=shutil.ignore_patterns('__pycache__'))
for p in new.glob('*.pth'):
 t=p.read_text();p.write_text(t.replace(str(src),str(dst)))
# Correct installed distribution provenance locally; no install or package updates.
for p in new.glob('agio_stablecoin-*.dist-info/direct_url.json'):
 p.write_text(p.read_text().replace(str(src),str(dst)))
cache=a/'cache';cache.mkdir();(cache/'mpl').mkdir()
meta={'original':str(src),'v2':str(dst),'commit_origem':git('rev-parse','HEAD').strip(),'branch':git('branch','--show-current').strip(),'data':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arquivos_hash':len(h),'hardlinks_compartilhados':0,'symlinks_projeto':links,'ambiente':'venv --copies + cópia física dos pacotes já instalados, .pth apontando exclusivamente V2','autorizacao':'usuário autorizou incluir arquivos não rastreados'}
(a/'preparacao.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));shutil.copy2('/private/tmp/aud002_preparar.py',a/'preparar.py')
print(json.dumps(meta,ensure_ascii=False))
