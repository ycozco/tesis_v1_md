"""Strictly development-only inputs and bounded parallel experimental fits."""
import json
import math
from datetime import date, timedelta
from pathlib import Path

DEVELOPMENT_END = date(2026, 4, 20)

def available(path, product, destination, target):
    payload = json.loads(Path(path).read_text(encoding='utf-8'))
    column = 3 if target == 'unit_fob' else 4
    return {date.fromisoformat(r[2]): float(r[column]) for r in payload['weekly_rows']
                if r[0] == product and r[1] == destination
                and r[column] is not None and math.isfinite(float(r[column]))}

def history_at(observed, last):
    history=[]; cursor=last
    while cursor in observed and len(history)<156:
        history.append({'timestamp':cursor.isoformat(),'target':observed[cursor]})
        cursor-=timedelta(days=7)
    return list(reversed(history))

def eligibility(path, product, destination, target, horizon, validation_end=None):
    if horizon not in (1,2,4): raise ValueError('El bloque de validación debe ser de 1, 2 o 4 semanas.')
    all_rows=available(path,product,destination,target)
    observed={d:v for d,v in all_rows.items() if d<=DEVELOPMENT_END}
    required=max(24,4*horizon)+horizon
    dates=sorted(observed)
    eligible=[d.isoformat() for d in dates if len(history_at(observed,d))>=required]
    requested=date.fromisoformat(validation_end) if validation_end else (max(observed) if observed else None)
    if requested and requested>DEVELOPMENT_END: raise ValueError('El bloque final está reservado: el desarrollo termina el 20/04/2026.')
    history=history_at(observed,requested) if requested else []
    ready=len(history)>=required
    return {'ready':ready,'required_weeks':required,'consecutive_weeks':len(history),'development_end':DEVELOPMENT_END.isoformat(),
            'last_observed':max(all_rows).isoformat() if all_rows else None,'last_development':dates[-1].isoformat() if dates else None,
            'validation_end':requested.isoformat() if requested else None,'eligible_validation_ends':eligible,
            'reason':None if ready else f'Se necesitan al menos {required} semanas consecutivas de desarrollo; hay {len(history)}. No se imputan huecos.'}

def prepare(path, product, destination, target, horizon, validation_end=None):
    if horizon not in (1,2,4): raise ValueError('El bloque de validación debe ser de 1, 2 o 4 semanas.')
    # The thesis final block remains reserved, including when selecting another date.
    info=eligibility(path,product,destination,target,horizon,validation_end)
    observed={d:v for d,v in available(path,product,destination,target).items() if d<=DEVELOPMENT_END}
    if not observed: raise ValueError('No hay datos de desarrollo para esta serie.')
    history=history_at(observed,date.fromisoformat(info['validation_end']))
    if not info['ready']: raise ValueError(info['reason'])
    return history[:-horizon], history[-horizon:]
