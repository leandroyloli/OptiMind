#!/usr/bin/env python3
"""
Teste automatizado para todos os problemas do arquivo problem_list.toml
Envia cada problema ao Meaning Agent e valida a resposta JSON
"""

import sys
import os
import json
import tomllib
from pathlib import Path

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.meaning_agent import MeaningAgent
from schemas.validator import validate_problem_output

def load_problems():
    """Carrega todos os problemas do arquivo TOML"""
    with open('prompts/problem_list.toml', 'rb') as f:
        data = tomllib.load(f)
    return data['problem']

def test_meaning_agent_on_all_problems():
    """Testa o Meaning Agent com todos os problemas"""
    print("🚀 Iniciando teste automatizado do Meaning Agent com todos os problemas...")
    print("=" * 80)
    
    # Carrega os problemas
    problems = load_problems()
    print(f"📚 Total de problemas carregados: {len(problems)}")
    
    # Inicializa o Meaning Agent
    agent = MeaningAgent()
    
    # Contadores para estatísticas
    total_tests = len(problems)
    successful_tests = 0
    failed_tests = 0
    failed_problems = []
    
    print(f"\n🔍 Testando cada problema individualmente...")
    print("-" * 80)
    
    for i, problem in enumerate(problems, 1):
        title = problem['title']
        description = problem['description']
        
        print(f"\n📝 Teste {i}/{total_tests}: {title}")
        print(f"   Descrição: {description[:100]}...")
        
        try:
            # Limpa o histórico de chat antes de cada teste para evitar contaminação
            agent.clear_chat_history()
            
            # Envia o problema ao Meaning Agent
            response = agent.process_problem(description)
            
            # Valida a resposta
            if isinstance(response, dict) and 'result' in response:
                problem_data = response['result']
                is_valid, validation_errors = validate_problem_output(problem_data)
            else:
                is_valid = False
                validation_errors = ["Resposta não contém dados válidos do problema"]
            
            if is_valid:
                print(f"   ✅ SUCESSO: Resposta válida")
                if isinstance(problem_data, dict):
                    print(f"   📊 Tipo: {problem_data.get('problem_type', 'N/A')}")
                    print(f"   🎯 Objetivo: {problem_data.get('objective', 'N/A')}")
                else:
                    print(f"   📊 Resposta: {type(problem_data).__name__}")
                successful_tests += 1
            else:
                print(f"   ❌ FALHA: Resposta inválida")
                print(f"   🔍 Erros de validação:")
                for error in validation_errors:
                    print(f"      - {error}")
                failed_tests += 1
                failed_problems.append({
                    'title': title,
                    'errors': validation_errors,
                    'response': response
                })
                
        except Exception as e:
            print(f"   💥 ERRO: Exceção durante o processamento")
            print(f"      Erro: {str(e)}")
            failed_tests += 1
            failed_problems.append({
                'title': title,
                'errors': [f"Exceção: {str(e)}"],
                'response': None
            })
    
    # Relatório final
    print("\n" + "=" * 80)
    print("📊 RELATÓRIO FINAL")
    print("=" * 80)
    print(f"✅ Testes bem-sucedidos: {successful_tests}/{total_tests} ({successful_tests/total_tests*100:.1f}%)")
    print(f"❌ Testes falharam: {failed_tests}/{total_tests} ({failed_tests/total_tests*100:.1f}%)")
    
    if failed_problems:
        print(f"\n🔍 PROBLEMAS QUE FALHARAM:")
        print("-" * 40)
        for problem in failed_problems:
            print(f"\n📝 {problem['title']}")
            for error in problem['errors']:
                print(f"   ❌ {error}")
    
    # Retorna True se todos os testes passaram
    return failed_tests == 0

def test_specific_problem(problem_title):
    """Testa um problema específico por título"""
    print(f"🎯 Testando problema específico: {problem_title}")
    
    problems = load_problems()
    agent = MeaningAgent()
    
    # Encontra o problema
    problem = None
    for p in problems:
        if p['title'] == problem_title:
            problem = p
            break
    
    if not problem:
        print(f"❌ Problema '{problem_title}' não encontrado!")
        return False
    
    print(f"📝 Descrição: {problem['description'][:200]}...")
    
    try:
        # Limpa o histórico de chat antes do teste
        agent.clear_chat_history()
        
        response = agent.process_problem(problem['description'])
        if isinstance(response, dict) and 'result' in response:
            problem_data = response['result']
            is_valid, validation_errors = validate_problem_output(problem_data)
        else:
            is_valid = False
            validation_errors = ["Resposta não contém dados válidos do problema"]
        
        if is_valid:
            print(f"✅ SUCESSO: Resposta válida")
            print(f"📊 Resposta completa:")
            print(json.dumps(problem_data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ FALHA: Resposta inválida")
            for error in validation_errors:
                print(f"   ❌ {error}")
            print(f"📊 Resposta recebida:")
            if isinstance(problem_data, dict):
                print(json.dumps(problem_data, indent=2, ensure_ascii=False))
            else:
                print(problem_data)
            return False
            
    except Exception as e:
        print(f"💥 ERRO: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Testa o Meaning Agent com problemas")
    parser.add_argument("--all", action="store_true", help="Testa todos os problemas")
    parser.add_argument("--problem", type=str, help="Testa um problema específico por título")
    
    args = parser.parse_args()
    
    if args.problem:
        success = test_specific_problem(args.problem)
        sys.exit(0 if success else 1)
    elif args.all:
        success = test_meaning_agent_on_all_problems()
        sys.exit(0 if success else 1)
    else:
        # Padrão: testa todos os problemas
        success = test_meaning_agent_on_all_problems()
        sys.exit(0 if success else 1) 