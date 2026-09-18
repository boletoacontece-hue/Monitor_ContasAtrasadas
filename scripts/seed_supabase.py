# -*- coding: utf-8 -*-
"""
Carga inicial (seed) do painel no Supabase.
Lê data/dados.json (gerado por prep.py) e faz UPSERT em:
  - ctapag_lancamentos  (por 'nr')
  - ctapag_conferencia  (por 'imovel')

Uso:
  export SUPABASE_URL="https://SEU-PROJETO.supabase.co"
  export SUPABASE_SERVICE_KEY="<service_role key>"   # NÃO use a anon aqui
  python scripts/seed_supabase.py

Rode primeiro o supabase/schema.sql no SQL Editor.
A service_role ignora RLS — mantenha essa chave em segredo (só no seu ambiente).
"""
import os, json, sys, urllib.request

URL = os.environ.get('SUPABASE_URL', '').rstrip('/')
KEY = os.environ.get('SUPABASE_SERVICE_KEY', '')
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(DIR, 'data', 'dados.json')
BATCH = 500

LANC_COLS = ['nr','origem','comp','venc','vi','dias','faixa','forn','fav','taxa','imovel','nome','prop','ocup','cc',
             'forma','parc','pr','compl','valor','cstatus','cadm','cdata','cmeio','cboleto','ctipo','cvalor','cquem',
             'cmotivo','cpego','cpago','cdtpgto']

def upsert(table, rows, on_conflict):
    if not rows:
        print(f'  {table}: nada a enviar'); return
    endpoint = f'{URL}/rest/v1/{table}?on_conflict={on_conflict}'
    sent = 0
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i+BATCH]
        body = json.dumps(chunk, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(endpoint, data=body, method='POST', headers={
            'apikey': KEY, 'Authorization': f'Bearer {KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'resolution=merge-duplicates,return=minimal',
        })
        with urllib.request.urlopen(req) as resp:
            if resp.status not in (200, 201, 204):
                raise SystemExit(f'Erro {resp.status} em {table}: {resp.read().decode()}')
        sent += len(chunk)
        print(f'  {table}: {sent}/{len(rows)}')

def main():
    if not URL or not KEY:
        print('Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no ambiente. (dry-run abaixo)')
    payload = json.load(open(DADOS, encoding='utf-8'))
    regs = payload['registros']
    conf = payload.get('conferencia', {})

    lanc = []
    for r in regs:
        o = {k: r.get(k) for k in LANC_COLS}
        if o.get('vi') == '':
            o['vi'] = None
        lanc.append(o)

    confrows = []
    for imv, c in conf.items():
        row = {'imovel': imv}
        row.update({k: c.get(k, '') for k in ['status','adm','data','meio','boleto','tipo','valor','quempaga','motivo','pego','pago','dtpgto']})
        confrows.append(row)

    print(f'Lançamentos: {len(lanc)} | Conferências: {len(confrows)}')
    if not URL or not KEY:
        print('DRY-RUN: nada enviado (faltam credenciais).'); return

    print('Enviando conferência…');  upsert('ctapag_conferencia', confrows, 'imovel')
    print('Enviando lançamentos…');  upsert('ctapag_lancamentos', lanc, 'nr')
    print('OK — carga concluída.')

if __name__ == '__main__':
    main()
