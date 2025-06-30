"""
Módulo de Autenticação para OptiMind
Gerencia usuários, senhas e validação de credenciais
"""

import streamlit as st
import streamlit_authenticator as stauth
import bcrypt
from typing import Dict, List, Tuple, Optional
import json
import os
import time
from datetime import datetime, timedelta
import re

class AuthManager:
    """Gerencia autenticação de usuários"""
    
    def __init__(self):
        self.users_file = "users.json"
        self.login_attempts_file = "login_attempts.json"
        self.max_attempts = 5  # Máximo de tentativas por IP
        self.lockout_duration = 300  # 5 minutos de bloqueio
        self.load_users()
        self.load_login_attempts()
    
    def load_users(self):
        """Carrega usuários do arquivo JSON"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users_data = json.load(f)
        else:
            # Usuários padrão para desenvolvimento com senhas SEGURAS
            self.users_data = {
                "usernames": {
                    "admin": {
                        "name": "Administrador",
                        "password": self._hash_password("Opt1M1nd@2024#Admin")
                    },
                    "demo": {
                        "name": "Usuário Demo",
                        "password": self._hash_password("D3m0@Opt1M1nd#2024!")
                    }
                }
            }
            self.save_users()
    
    def load_login_attempts(self):
        """Carrega tentativas de login para rate limiting"""
        if os.path.exists(self.login_attempts_file):
            with open(self.login_attempts_file, 'r') as f:
                self.login_attempts = json.load(f)
        else:
            self.login_attempts = {}
    
    def save_login_attempts(self):
        """Salva tentativas de login"""
        with open(self.login_attempts_file, 'w') as f:
            json.dump(self.login_attempts, f, indent=2)
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Verifica se um IP está bloqueado por tentativas excessivas"""
        if ip_address not in self.login_attempts:
            return False
        
        attempts = self.login_attempts[ip_address]
        if len(attempts) >= self.max_attempts:
            # Verificar se o bloqueio ainda está ativo
            last_attempt = max(attempts)
            if time.time() - last_attempt < self.lockout_duration:
                return True
            else:
                # Resetar tentativas após o período de bloqueio
                self.login_attempts[ip_address] = []
                self.save_login_attempts()
        
        return False
    
    def record_login_attempt(self, ip_address: str, success: bool):
        """Registra uma tentativa de login"""
        if ip_address not in self.login_attempts:
            self.login_attempts[ip_address] = []
        
        current_time = time.time()
        
        if success:
            # Resetar tentativas em caso de sucesso
            self.login_attempts[ip_address] = []
        else:
            # Adicionar tentativa falhada
            self.login_attempts[ip_address].append(current_time)
            # Manter apenas as últimas tentativas
            self.login_attempts[ip_address] = self.login_attempts[ip_address][-self.max_attempts:]
        
        self.save_login_attempts()
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Valida a força da senha"""
        if len(password) < 12:
            return False, "Senha deve ter pelo menos 12 caracteres"
        
        if not re.search(r"[A-Z]", password):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        
        if not re.search(r"[a-z]", password):
            return False, "Senha deve conter pelo menos uma letra minúscula"
        
        if not re.search(r"\d", password):
            return False, "Senha deve conter pelo menos um número"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Senha deve conter pelo menos um caractere especial"
        
        return True, "Senha forte"
    
    def save_users(self):
        """Salva usuários no arquivo JSON"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users_data, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash de senha usando bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def add_user(self, username: str, name: str, password: str) -> Tuple[bool, str]:
        """Adiciona novo usuário com validação de senha"""
        if username in self.users_data["usernames"]:
            return False, "Usuário já existe"
        
        # Validar força da senha
        is_strong, message = self.validate_password_strength(password)
        if not is_strong:
            return False, f"Senha fraca: {message}"
        
        self.users_data["usernames"][username] = {
            "name": name,
            "password": self._hash_password(password)
        }
        self.save_users()
        return True, "Usuário criado com sucesso"
    
    def remove_user(self, username: str) -> bool:
        """Remove usuário"""
        if username in self.users_data["usernames"]:
            del self.users_data["usernames"][username]
            self.save_users()
            return True
        return False
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Retorna informações do usuário"""
        return self.users_data["usernames"].get(username)
    
    def list_users(self) -> List[str]:
        """Lista todos os usuários"""
        return list(self.users_data["usernames"].keys())

def get_client_ip():
    """Obtém o IP do cliente (simplificado para desenvolvimento)"""
    # Em produção, isso seria obtido do request
    return "127.0.0.1"

def create_authenticator() -> stauth.Authenticate:
    """Cria instância do autenticador Streamlit"""
    # Carregar usuários do arquivo JSON ou usar padrão
    auth_manager = AuthManager()
    
    # Converter para formato do streamlit-authenticator
    credentials = {
        'usernames': {}
    }
    
    for username, user_data in auth_manager.users_data["usernames"].items():
        credentials['usernames'][username] = {
            'name': user_data['name'],
            'password': user_data['password']
        }
    
    return stauth.Authenticate(
        credentials=credentials,
        cookie_name="optimind_cookie",
        cookie_key="abcdef",  # até v0.4.2 usa-se `cookie_key`
        location="main",
        cookie_expiry_days=30
    )

def check_auth_status() -> Tuple[Optional[str], Optional[str], bool]:
    """
    Verifica status de autenticação usando session_state
    Returns: (name, username, authentication_status)
    """
    authenticator = create_authenticator()
    
    # Renderizar o formulário de login
    authenticator.login(
        location="main",
        fields={"Form name": "OptiMind Login"}
    )
    
    # Verificar status na session_state
    auth_status = st.session_state.get("authentication_status")
    name = st.session_state.get("name")
    username = st.session_state.get("username")
    
    return name, username, auth_status

def logout():
    """Realiza logout do usuário"""
    authenticator = create_authenticator()
    authenticator.logout("Logout", location="main")

def require_auth():
    """
    Decorator para requerer autenticação
    Se não autenticado, para a execução
    """
    name, username, auth_status = check_auth_status()
    
    if auth_status == False:
        st.error("❌ Usuário/senha incorretos")
        st.stop()
    elif auth_status == None:
        st.warning("⚠️ Por favor, insira suas credenciais")
        st.stop()
    elif auth_status == True:
        # Login bem-sucedido
        return name, username
    
    # Se chegou aqui, ainda não autenticado
    st.stop() 