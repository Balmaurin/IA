"""Generate frontend scaffold for SHEILY-light (React + TS).
Run: python setup_web_scaffold.py
Creates directories/files only if missing, with minimal placeholder content.
"""
from pathlib import Path
import json
import os

ROOT = Path(__file__).resolve().parent
web_dir = ROOT / "web"
src_dir = web_dir / "src"

# ---------- helper -------------
def ensure_file(path: Path, content: str = ""):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print("[CREATE]", path.relative_to(ROOT))

# ---------- package.json, tsconfig, env -------------
ensure_file(web_dir / "package.json", json.dumps({
    "name": "sheily-light-frontend",
    "version": "0.1.0",
    "private": True,
    "scripts": {
        "dev": "vite",
        "build": "vite build",
        "preview": "vite preview"
    },
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "react-router-dom": "^6.23.0",
        "axios": "^1.6.0"
    },
    "devDependencies": {
        "typescript": "^5.4.5",
        "@types/react": "^18.2.50",
        "@types/react-dom": "^18.2.17",
        "vite": "^5.2.0"
    }
}, indent=2))

tsconfig_content = {
    "compilerOptions": {
        "target": "ES6",
        "module": "ESNext",
        "jsx": "react-jsx",
        "strict": True,
        "esModuleInterop": True,
        "skipLibCheck": True,
        "forceConsistentCasingInFileNames": True
    },
    "include": ["src/**/*"]
}
ensure_file(web_dir / "tsconfig.json", json.dumps(tsconfig_content, indent=2))
ensure_file(web_dir / ".env", "VITE_API_URL=http://localhost:8000\n")

# ---------- public -------------
ensure_file(web_dir / "public" / "index.html", """<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>SHEILY-light</title>
  </head>
  <body>
    <div id=\"root\"></div>
    <script type=\"module\" src=\"/src/index.tsx\"></script>
  </body>
</html>""")
ensure_file(web_dir / "public" / "favicon.ico", "")
ensure_file(web_dir / "public" / "robots.txt", "User-agent: *\nDisallow:\n")

# ---------- utility to create component ----------
COMPONENT_TEMPLATE = """import React from 'react';

const {name}: React.FC = () => {
  return <div>{name} works!</div>;
};

export default {name};
"""

def create_component(path: Path, name: str):
    ensure_file(path, COMPONENT_TEMPLATE.replace("{name}", name))

# ---- components hierarchy ----
components = {
    "auth": ["LoginForm", "RegisterForm", "PasswordResetForm"],
    "chat": ["ChatInterface", "MessageBubble", "ChatHistory"],
    "tokens": ["TokenBalance", "TokenTransactions"],
    "backup": ["BackupCreator", "BackupRestorer"],
    "admin": ["AdminDashboard", "UserManager", "SystemMonitor"],
    "common": ["Header", "Footer", "Notification"],
}

for folder, comps in components.items():
    for comp in comps:
        create_component(src_dir / "components" / folder / f"{comp}.tsx", comp)

# ---- pages ----
pages = ["HomePage", "ChatPage", "ProfilePage", "AdminPage", "SettingsPage"]
for page in pages:
    create_component(src_dir / "pages" / f"{page}.tsx", page)

# ---- services ----
ensure_file(src_dir / "services" / "apiClient.ts", "import axios from 'axios';\n\nconst apiClient = axios.create({\n  baseURL: import.meta.env.VITE_API_URL,\n});\n\nexport default apiClient;\n")
ensure_file(src_dir / "services" / "authService.ts", "import api from './apiClient';\nexport const login = (data:any) => api.post('/api/auth/login', data);\nexport const register = (data:any) => api.post('/api/auth/register', data);\n")
ensure_file(src_dir / "services" / "tokenService.ts", "import api from './apiClient';\nexport const getBalance = (user:string) => api.get(`/api/tokens?user=${user}`);\n")

# ---- hooks ----
ensure_file(src_dir / "hooks" / "useAuth.ts", "import { useContext } from 'react';\nimport { AuthContext } from '../contexts/AuthContext';\nexport const useAuth = () => useContext(AuthContext);\n")
ensure_file(src_dir / "hooks" / "useChat.ts", "import { useContext } from 'react';\nimport { ChatContext } from '../contexts/ChatContext';\nexport const useChat = () => useContext(ChatContext);\n")

# ---- contexts ----
ensure_file(src_dir / "contexts" / "AuthContext.tsx", "import React, { createContext, useState } from 'react';\nexport const AuthContext = createContext<any>(null);\nexport const AuthProvider = ({ children }: any) => {\n  const [user, setUser] = useState(null);\n  return <AuthContext.Provider value={{ user, setUser }}>{children}</AuthContext.Provider>;\n};\n")
ensure_file(src_dir / "contexts" / "ChatContext.tsx", "import React, { createContext } from 'react';\nexport const ChatContext = createContext<any>(null);\n")

# ---- utils ----
ensure_file(src_dir / "utils" / "helpers.ts", "export const truncate = (str:string, n=50) => str.length>n ? str.slice(0,n)+'...' : str;\n")
ensure_file(src_dir / "utils" / "constants.ts", "export const APP_NAME = 'SHEILY-light';\n")

# ---- styles placeholders ----
ensure_file(src_dir / "styles" / "theme.css", ":root {\n  --primary: #2f60ff;\n}\n")
ensure_file(src_dir / "styles" / "components" / "chat.css", "")
ensure_file(src_dir / "styles" / "components" / "forms.css", "")
ensure_file(src_dir / "styles" / "layout" / "header.css", "")
ensure_file(src_dir / "styles" / "layout" / "main.css", "")

# ---- App & index ----
ensure_file(src_dir / "App.tsx", "import React from 'react';\nimport { BrowserRouter, Routes, Route } from 'react-router-dom';\nimport HomePage from './pages/HomePage';\nimport ChatPage from './pages/ChatPage';\nconst App: React.FC = () => (\n  <BrowserRouter>\n    <Routes>\n      <Route path='/' element={<HomePage />} />\n      <Route path='/chat' element={<ChatPage />} />\n    </Routes>\n  </BrowserRouter>\n);\nexport default App;\n")
ensure_file(src_dir / "index.tsx", "import React from 'react';\nimport ReactDOM from 'react-dom/client';\nimport App from './App';\nimport './styles/theme.css';\n\nReactDOM.createRoot(document.getElementById('root')!).render(<App />);\n")

print("✅ Web scaffold listo. Ejecuta: cd web && npm install && npm run dev")
