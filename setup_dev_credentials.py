#!/usr/bin/env python3
"""
Script para gerenciar credenciais de desenvolvimento do OptiMind
"""

import secrets
import string
from utils.auth import AuthManager

def generate_secure_password(length=16):
    """Gera uma senha segura aleatória"""
    # Caracteres permitidos
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Garantir pelo menos um de cada tipo
    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]
    
    # Completar com caracteres aleatórios
    all_chars = lowercase + uppercase + digits + symbols
    for _ in range(length - 4):
        password.append(secrets.choice(all_chars))
    
    # Embaralhar a senha
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    
    return ''.join(password_list)

def show_current_credentials():
    """Mostra as credenciais atuais"""
    print("🔐 Credenciais Atuais do OptiMind")
    print("=" * 50)
    
    auth_manager = AuthManager()
    users = auth_manager.list_users()
    
    for username in users:
        user_info = auth_manager.get_user_info(username)
        if user_info:
            print(f"\n👤 Usuário: {username}")
            print(f"   Nome: {user_info['name']}")
            print(f"   Hash: {user_info['password'][:30]}...")
    
    print("\n" + "=" * 50)
    print("⚠️  As senhas não são mostradas por segurança!")
    print("   Consulte o arquivo SECURITY.md para as senhas.")

def generate_new_credentials():
    """Gera novas credenciais seguras"""
    print("🔐 Gerando Novas Credenciais Seguras")
    print("=" * 50)
    
    # Gerar senhas seguras
    admin_password = generate_secure_password(20)
    demo_password = generate_secure_password(18)
    
    print(f"\n👤 Admin:")
    print(f"   Username: admin")
    print(f"   Senha: {admin_password}")
    
    print(f"\n👤 Demo:")
    print(f"   Username: demo")
    print(f"   Senha: {demo_password}")
    
    print("\n" + "=" * 50)
    print("⚠️  IMPORTANTE:")
    print("   1. Salve estas senhas em um local seguro")
    print("   2. Atualize o arquivo SECURITY.md")
    print("   3. NUNCA commite as senhas no Git!")
    
    # Perguntar se quer aplicar as mudanças
    response = input("\n❓ Deseja aplicar estas novas credenciais? (s/N): ")
    if response.lower() in ['s', 'sim', 'y', 'yes']:
        auth_manager = AuthManager()
        
        # Remover usuários existentes
        auth_manager.remove_user("admin")
        auth_manager.remove_user("demo")
        
        # Adicionar novos usuários
        success1, msg1 = auth_manager.add_user("admin", "Administrador", admin_password)
        success2, msg2 = auth_manager.add_user("demo", "Usuário Demo", demo_password)
        
        if success1 and success2:
            print("✅ Credenciais atualizadas com sucesso!")
            print("🔄 Reinicie a aplicação para aplicar as mudanças.")
        else:
            print("❌ Erro ao atualizar credenciais:")
            print(f"   Admin: {msg1}")
            print(f"   Demo: {msg2}")
    else:
        print("❌ Operação cancelada.")

def main():
    """Menu principal"""
    print("🧠 OptiMind - Gerenciador de Credenciais")
    print("=" * 50)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Mostrar credenciais atuais")
        print("2. Gerar novas credenciais")
        print("3. Sair")
        
        choice = input("\nOpção: ").strip()
        
        if choice == "1":
            show_current_credentials()
        elif choice == "2":
            generate_new_credentials()
        elif choice == "3":
            print("👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")

if __name__ == "__main__":
    main() 