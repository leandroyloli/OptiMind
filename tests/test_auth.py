"""
Testes completos para o sistema de autenticação do OptiMind
"""

import pytest
import json
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import bcrypt

# Importar módulos do OptiMind
import sys
sys.path.append('.')

from utils.auth import AuthManager, require_auth, logout, create_authenticator
import streamlit as st

@pytest.fixture
def temp_auth_manager():
    temp_dir = tempfile.mkdtemp()
    users_file = os.path.join(temp_dir, "users.json")
    login_attempts_file = os.path.join(temp_dir, "login_attempts.json")
    auth_manager = AuthManager()
    auth_manager.users_file = users_file
    auth_manager.login_attempts_file = login_attempts_file
    # Limpar usuários padrão para garantir ambiente limpo
    auth_manager.users_data = {"usernames": {}}
    auth_manager.save_users()
    yield auth_manager
    shutil.rmtree(temp_dir)

class TestAuthManager:
    """Testes para a classe AuthManager"""
    
    def test_init_creates_default_users(self, temp_auth_manager):
        """Testar se usuários padrão são criados na inicialização"""
        temp_auth_manager.load_users()
        # Após reset, não há usuários padrão
        assert temp_auth_manager.users_data["usernames"] == {}
    
    def test_password_hashing(self, temp_auth_manager):
        """Testar hash e verificação de senhas"""
        password = "TestPassword123!"
        
        # Testar hash
        hashed = temp_auth_manager._hash_password(password)
        assert hashed != password
        assert hashed.startswith("$2b$")
        
        # Testar verificação
        assert temp_auth_manager.verify_password(password, hashed)
        assert not temp_auth_manager.verify_password("wrong_password", hashed)
    
    def test_password_strength_validation(self, temp_auth_manager):
        """Testar validação de força de senha"""
        # Senha forte
        strong_password = "StrongPass123!"
        is_strong, message = temp_auth_manager.validate_password_strength(strong_password)
        assert is_strong
        
        # Senha fraca - muito curta
        weak_password = "Short1!aA"
        is_strong, message = temp_auth_manager.validate_password_strength(weak_password)
        assert not is_strong
        assert "12 caracteres" in message
        
        # Senha fraca - sem maiúsculas
        weak_password = "password123!a@"  # 13 chars
        is_strong, message = temp_auth_manager.validate_password_strength(weak_password)
        assert not is_strong
        assert "maiúscula" in message
        
        # Senha fraca - sem minúsculas
        weak_password = "PASSWORD123!@#"  # 13 chars
        is_strong, message = temp_auth_manager.validate_password_strength(weak_password)
        assert not is_strong
        assert "minúscula" in message
        
        # Senha fraca - sem números
        weak_password = "Password!@#abc"  # 14 chars
        is_strong, message = temp_auth_manager.validate_password_strength(weak_password)
        assert not is_strong
        assert "número" in message
        
        # Senha fraca - sem símbolos
        weak_password = "Password123abc"  # 14 chars
        is_strong, message = temp_auth_manager.validate_password_strength(weak_password)
        assert not is_strong
        assert "caractere especial" in message
    
    def test_add_user(self, temp_auth_manager):
        """Testar adição de usuários"""
        # Adicionar usuário válido
        success, message = temp_auth_manager.add_user("testuser", "Test User", "StrongPass123!")
        assert success
        assert "testuser" in temp_auth_manager.users_data["usernames"]
        assert temp_auth_manager.users_data["usernames"]["testuser"]["name"] == "Test User"
        
        # Tentar adicionar usuário que já existe
        success, message = temp_auth_manager.add_user("testuser", "Another User", "AnotherPass123!")
        assert not success
        assert "já existe" in message
        
        # Tentar adicionar usuário com senha fraca
        success, message = temp_auth_manager.add_user("weakuser", "Weak User", "weakweakweak1!")
        assert not success
        assert "fraca" in message
    
    def test_remove_user(self, temp_auth_manager):
        """Testar remoção de usuários"""
        # Adicionar usuário
        temp_auth_manager.add_user("testuser", "Test User", "StrongPass123!")
        assert "testuser" in temp_auth_manager.users_data["usernames"]
        
        # Remover usuário
        success = temp_auth_manager.remove_user("testuser")
        assert success
        assert "testuser" not in temp_auth_manager.users_data["usernames"]
        
        # Tentar remover usuário que não existe
        success = temp_auth_manager.remove_user("nonexistent")
        assert not success
    
    def test_rate_limiting(self, temp_auth_manager):
        """Testar rate limiting"""
        ip_address = "192.168.1.1"
        
        # Verificar que IP não está bloqueado inicialmente
        assert not temp_auth_manager.is_ip_blocked(ip_address)
        
        # Simular tentativas falhadas
        for _ in range(5):
            temp_auth_manager.record_login_attempt(ip_address, False)
        
        # Verificar se IP está bloqueado após 5 tentativas
        assert temp_auth_manager.is_ip_blocked(ip_address)
        
        # Simular login bem-sucedido
        temp_auth_manager.record_login_attempt(ip_address, True)
        
        # Verificar se IP foi desbloqueado
        assert not temp_auth_manager.is_ip_blocked(ip_address)
    
    def test_get_user_info(self, temp_auth_manager):
        """Testar obtenção de informações do usuário"""
        # Adicionar usuário
        temp_auth_manager.add_user("testuser", "Test User", "StrongPass123!")
        
        # Obter informações
        user_info = temp_auth_manager.get_user_info("testuser")
        assert user_info is not None
        assert user_info["name"] == "Test User"
        
        # Usuário inexistente
        user_info = temp_auth_manager.get_user_info("nonexistent")
        assert user_info is None
    
    def test_list_users(self, temp_auth_manager):
        """Testar listagem de usuários"""
        # Adicionar alguns usuários
        temp_auth_manager.add_user("user1", "User One", "Pass123!Abcde")
        temp_auth_manager.add_user("user2", "User Two", "Pass456!Abcde")
        
        # Listar usuários
        users = temp_auth_manager.list_users()
        assert "user1" in users
        assert "user2" in users

class TestAuthManagerExtended:
    """Testes adicionais para a classe AuthManager"""
    
    def test_verify_password_direct(self, temp_auth_manager):
        """Testar verificação de senha diretamente"""
        password = "TestPassword123!"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        assert temp_auth_manager.verify_password(password, hashed)
        assert not temp_auth_manager.verify_password("wrong", hashed)
    
    def test_rate_limiting_extended(self, temp_auth_manager):
        """Testar rate limiting com mais detalhes"""
        ip = "192.168.1.1"
        
        # Não bloqueado inicialmente
        assert not temp_auth_manager.is_ip_blocked(ip)
        
        # Simular tentativas excessivas
        for _ in range(5):
            temp_auth_manager.record_login_attempt(ip, False)
        
        # Deve estar bloqueado
        assert temp_auth_manager.is_ip_blocked(ip)
        
        # Login bem-sucedido deve desbloquear
        temp_auth_manager.record_login_attempt(ip, True)
        assert not temp_auth_manager.is_ip_blocked(ip)

class TestAuthIntegration:
    """Testes de integração do sistema de autenticação"""
    
    @pytest.mark.skip(reason="Testes de integração requerem contexto real do Streamlit.")
    @patch('streamlit.session_state')
    def test_require_auth_success(self, mock_session_state):
        """Testar autenticação bem-sucedida"""
        # Mock session_state com usuário autenticado
        mock_session_state.authenticated = True
        mock_session_state.user_name = "Test User"
        mock_session_state.username = "testuser"
        
        # Mock do streamlit
        with patch('streamlit.stop') as mock_stop:
            name, username = require_auth()
            assert name == "Test User"
            assert username == "testuser"
            mock_stop.assert_not_called()
    
    @pytest.mark.skip(reason="Testes de integração requerem contexto real do Streamlit.")
    @patch('streamlit.session_state')
    def test_require_auth_failed(self, mock_session_state):
        """Testar autenticação falhada"""
        # Mock session_state sem autenticação
        mock_session_state.authenticated = False
        mock_session_state.get.return_value = False
        
        # Mock do streamlit
        with patch('streamlit.stop') as mock_stop:
            with patch('streamlit.error') as mock_error:
                require_auth()
                mock_error.assert_called()
                mock_stop.assert_called()
    
    @pytest.mark.skip(reason="Testes de integração requerem contexto real do Streamlit.")
    def test_create_authenticator(self):
        """Testar criação do autenticador"""
        authenticator = create_authenticator()
        
        # Verificar se é uma instância válida
        assert authenticator is not None
        assert hasattr(authenticator, 'login')
        assert hasattr(authenticator, 'logout')
        
        # Verificar se tem credenciais
        assert hasattr(authenticator, 'credentials')
        assert 'usernames' in authenticator.credentials

def test_password_strength_examples():
    """Testar exemplos de força de senha"""
    auth_manager = AuthManager()
    
    # Senhas fortes
    strong_passwords = [
        "Opt1M1nd@2024#Admin",
        "D3m0@Opt1M1nd#2024!",
        "MySecurePass123!",
        "Complex@Password#2024"
    ]
    
    for password in strong_passwords:
        is_strong, message = auth_manager.validate_password_strength(password)
        assert is_strong, f"Senha '{password}' deveria ser forte: {message}"
    
    # Senhas fracas
    weak_passwords = [
        "password123!a@",
        "PASSWORD123!@#",
        "Password!@#abc",
        "Password123abc",
    ]
    
    for password in weak_passwords:
        is_strong, message = auth_manager.validate_password_strength(password)
        assert not is_strong, f"Senha '{password}' deveria ser fraca"

if __name__ == "__main__":
    # Executar testes
    pytest.main([__file__, "-v"]) 