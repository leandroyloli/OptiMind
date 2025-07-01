import requests

if __name__ == "__main__":
    url = "https://optimind.streamlit.app/"
    try:
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        if response.status_code == 200:
            print("✅ O site está online!")
        else:
            print("⚠️ O site respondeu, mas não com status 200.")
    except Exception as e:
        print(f"❌ Erro ao acessar o site: {e}") 