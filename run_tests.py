#!/usr/bin/env python3
"""
Script para executar testes do sistema de autenticação do OptiMind
"""

import subprocess
import sys
import os

def run_tests():
    """Executar todos os testes automatizados do projeto (pasta tests)"""
    print("🧪 Executando todos os testes do OptiMind...")
    print("=" * 60)
    try:
        import pytest
    except ImportError:
        print("❌ pytest não está instalado. Instalando...")
        import subprocess, sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
    import subprocess, sys
    result = subprocess.run([
        sys.executable, "-m", "pytest", "tests", "-v", "--tb=short"
    ], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️  Warnings/Errors:")
        print(result.stderr)
    if result.returncode == 0:
        print("✅ Todos os testes passaram!")
        return True
    else:
        print("❌ Alguns testes falharam!")
        return False

def run_specific_test(test_name):
    """Executar um teste específico"""
    print(f"🧪 Executando teste específico: {test_name}")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            f"tests/test_auth.py::{test_name}", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Warnings/Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")
        return False

def show_test_summary():
    """Mostrar resumo dos testes disponíveis"""
    print("📋 Testes disponíveis:")
    print("=" * 60)
    
    tests = [
        "TestAuthManager.test_init_creates_default_users",
        "TestAuthManager.test_password_hashing", 
        "TestAuthManager.test_password_strength_validation",
        "TestAuthManager.test_add_user",
        "TestAuthManager.test_remove_user",
        "TestAuthManager.test_rate_limiting",
        "TestAuthManager.test_get_user_info",
        "TestAuthManager.test_list_users",
        "TestAuthManagerExtended.test_verify_password_direct",
        "TestAuthManagerExtended.test_rate_limiting_extended",
        "TestAuthIntegration.test_require_auth_success",
        "TestAuthIntegration.test_require_auth_failed",
        "TestAuthIntegration.test_create_authenticator",
        "test_password_strength_examples"
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"{i:2d}. {test}")
    
    print()
    print("Para executar um teste específico:")
    print("python run_tests.py --test <nome_do_teste>")
    print()
    print("Para executar todos os testes:")
    print("python run_tests.py")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("🧪 Testes do Sistema de Autenticação - OptiMind")
            print("=" * 60)
            print()
            print("Uso:")
            print("  python run_tests.py              # Executar todos os testes")
            print("  python run_tests.py --test <nome> # Executar teste específico")
            print("  python run_tests.py --list        # Listar testes disponíveis")
            print("  python run_tests.py --help        # Mostrar esta ajuda")
            print()
            show_test_summary()
        elif sys.argv[1] == "--list" or sys.argv[1] == "-l":
            show_test_summary()
        elif sys.argv[1] == "--test" and len(sys.argv) > 2:
            test_name = sys.argv[2]
            success = run_specific_test(test_name)
            sys.exit(0 if success else 1)
        else:
            print("❌ Argumento inválido. Use --help para ver as opções.")
            sys.exit(1)
    else:
        # Executar todos os testes
        success = run_tests()
        sys.exit(0 if success else 1) 