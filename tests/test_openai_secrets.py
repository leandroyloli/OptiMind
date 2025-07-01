import os
import pytest
import openai
import streamlit as st
import time

try:
    import openai
    import streamlit as st
except ImportError:
    openai = None
    st = None

@pytest.mark.skipif(openai is None or st is None, reason="openai ou streamlit não instalado")
def test_openai_api_key_and_connection():
    # Tenta ler a chave e o modelo do mesmo jeito do AdminTools
    api_key = st.secrets["OPENAI"]["OPENAI_API_KEY"]
    model = st.secrets["OPENAI"].get("OPENAI_MODEL", None)
    assert api_key, "OPENAI_API_KEY not found in secrets."
    openai.api_key = api_key
    try:
        start = time.time()
        models = openai.models.list()
        elapsed = time.time() - start
        assert hasattr(models, 'data'), "Resposta inesperada da API OpenAI."
        print(f"Connection successful! {len(models.data)} models available. (time: {elapsed:.2f}s)")
    except Exception as e:
        pytest.fail(f"Erro ao conectar na API OpenAI: {e}") 