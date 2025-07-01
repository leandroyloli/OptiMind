import os
import pytest

try:
    import openai
    import streamlit as st
except ImportError:
    openai = None
    st = None

@pytest.mark.skipif(openai is None or st is None, reason="openai ou streamlit não instalado")
def test_openai_api_key_and_connection():
    api_key = None
    model = None
    # Tenta ler dos secrets do Streamlit
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    # Fallback: tenta variável de ambiente
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    assert api_key, "Chave OpenAI não encontrada nos secrets nem nas variáveis de ambiente."
    assert api_key.startswith("sk-"), "Formato da chave OpenAI inválido."
    openai.api_key = api_key
    # Tenta ler o modelo
    try:
        model = st.secrets["OPENAI_MODEL"]
    except Exception:
        pass
    if not model:
        model = os.environ.get("OPENAI_MODEL")
    # Testa uma chamada simples (listar modelos)
    try:
        models = openai.models.list()
        assert hasattr(models, 'data'), "Resposta inesperada da API OpenAI."
    except Exception as e:
        pytest.fail(f"Erro ao conectar na API OpenAI: {e}") 