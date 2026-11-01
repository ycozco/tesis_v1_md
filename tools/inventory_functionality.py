"""Inventory active FastAPI routes, SPA paths and historical Flask routes without invoking mutations."""
import ast
import json
import os
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'data/runtime-api'))
sys.path.insert(1,str(ROOT/'sistema-web-agro/backend'))
os.environ['DATABASE_URL']='sqlite+pysqlite:///:memory:'
from app_fastapi.main import app


def main():
    routes=[]
    for path,operations in app.openapi()['paths'].items():
        for method,operation in operations.items():
            if method not in ('get','post','put','patch','delete'):continue
            routes.append({'path':path,'methods':[method.upper()],
                           'requires_bearer_auth':bool(operation.get('security')),
                           'runtime_registered':True, 'execution_tested':path.startswith('/api/research/')
                           or path in ['/api/auth/login','/api/auth/logout','/api/dashboard/stats','/health','/api/migration/status']})
    legacy=[]
    for file in sorted((ROOT/'sistema-web-agro/backend/routes').glob('*.py')):
        tree=ast.parse(file.read_text(encoding='utf8'))
        for node in ast.walk(tree):
            if not isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):continue
            for decorator in node.decorator_list:
                if isinstance(decorator,ast.Call) and isinstance(decorator.func,ast.Attribute) and decorator.func.attr=='route':
                    path=ast.literal_eval(decorator.args[0])
                    methods=next((ast.literal_eval(k.value) for k in decorator.keywords if k.arg=='methods'),['GET'])
                    legacy.append({'path':path,'methods':methods,'function':node.name,
                        'file':str(file.relative_to(ROOT)).replace('\\','/'),'status':'legacy_source_inventory_not_execution_verified'})
    spa=re.findall(r'<Route\s+path="([^"]+)"', (ROOT/'sistema-web-agro/frontend/src/App.jsx').read_text(encoding='utf8'))
    report={'date':'2026-11-01','fastapi':routes,'legacy_flask':legacy,'spa_paths':spa,
            'research_views':['series','pronosticos','senales','reportes','fuentes','proceso','ia'],
            'warning':'Registration or static inventory does not prove a workflow works. Historical Flask mutations were not invoked.'}
    out=ROOT/'sistema-web-agro/docs/ui-ia-auditoria-2026-11-01/inventario-funcional.json'
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps({'fastapi_routes':len(routes),'legacy_flask_routes':len(legacy),'spa_paths':len(spa),'research_views':7}))


if __name__=='__main__':main()
