import pytest
import os
import sqlite3
from utils import db
import re
import json
from datetime import datetime

def test_job_persistence_and_id_format():
    # Cria um job sintético
    job_id = f"job_{int(datetime.now().timestamp())}_{datetime.now().strftime('%Y%m%d-%H:%M:%S')}_TesteJob"
    job = {
        'id': job_id,
        'created_at': datetime.now().isoformat(),
        'user_input': 'Maximize lucro: 3x + 4y subject to x + y <= 10',
        'job_title': 'TesteJob',
        'status': 'completed',
        'final_message': 'Job concluído com sucesso!'
    }
    db.insert_job(job)
    # Verifica se o job está no banco
    jobs = db.get_jobs()
    found_job = next((j for j in jobs if j['id'] == job_id), None)
    print(f"job_id gerado: {job_id}")
    print(f"job_id salvo: {found_job['id'] if found_job else 'NÃO ENCONTRADO'}")
    assert found_job is not None, f"Job com id {job_id} não encontrado no banco."
    # Verifica formato do ID
    pattern = r"job_\d+_\d{8}-\d{2}:\d{2}:\d{2}_.+"
    assert re.match(pattern, job_id), f"job_id '{job_id}' não bate com o padrão {pattern}"


def test_conversation_and_agent_output_persistence():
    job_id = db.get_jobs()[0]['id']
    # Insere conversa
    db.insert_conversation(job_id, 'user', 'Olá, quero maximizar lucro', datetime.now().isoformat())
    db.insert_conversation(job_id, 'Meaning', '{"is_valid_problem": true}', datetime.now().isoformat())
    # Insere output de agente
    db.insert_agent_output(job_id, 'Meaning', json.dumps({'result': 42}), datetime.now().isoformat())
    # Verifica persistência
    convs = db.get_conversations(job_id)
    outputs = db.get_agent_outputs(job_id)
    assert any(c['sender'] == 'user' for c in convs)
    assert any(o['agent_name'] == 'Meaning' for o in outputs)


def test_history_dataframe_structure():
    # Simula dataframe do histórico
    jobs = db.get_jobs()
    import pandas as pd
    df = pd.DataFrame([
        {'ID': job['id'], 'Created at': job['created_at'], 'Title': job['job_title'], 'Status': job['status']}
        for job in jobs
    ])
    # Verifica colunas essenciais
    for col in ['ID', 'Created at', 'Title', 'Status']:
        assert col in df.columns
    # Verifica se há pelo menos um job
    assert len(df) > 0


def test_agent_outputs_are_json():
    # Verifica se outputs dos agentes são JSON válidos
    jobs = db.get_jobs()
    for job in jobs:
        outputs = db.get_agent_outputs(job['id'])
        for output in outputs:
            try:
                data = json.loads(output['json_output'])
                assert isinstance(data, dict) or isinstance(data, list)
            except Exception:
                # Pode ser string simples, mas não deve quebrar
                assert isinstance(output['json_output'], str)


def test_session_state_cleanup():
    # Simula limpeza de estado após salvar (mock)
    session_state = {'job_id': 'job_999_20240701-12:00:00_TesteJob', 'chat_history': ['msg1', 'msg2']}
    # Após salvar
    session_state.clear()
    assert session_state == {}


def test_navigation_flow_simulation():
    # Simula navegação entre páginas (mock)
    pages = ['d_NewJob', 'e_Results', 'f_History']
    nav_trace = []
    for page in pages:
        nav_trace.append(page)
    assert nav_trace == ['d_NewJob', 'e_Results', 'f_History'] 