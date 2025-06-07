# Sistema de Deteção de Quedas com YOLO

## 📋 Descrição

Este projeto implementa um sistema de deteção de quedas em tempo real utilizando o modelo YOLO (You Only Look Once). O sistema monitoriza vídeo em tempo real ou ficheiros de vídeo pré-gravados, deteta quedas de pessoas e envia notificações por e-mail quando uma pessoa permanece caída por um período prolongado.

## 🌟 Funcionalidades

- Deteção em tempo real de quedas de pessoas
- Monitorização por câmera ou vídeos pré-gravados
- Envio automático de notificações por e-mail com imagem da deteção
- Temporizador para confirmar que a pessoa permanece caída

## 🛠️ Requisitos

- Python 3
- OpenCV
- Ultralytics YOLO
- Acesso à câmera (para monitorização em tempo real)
- Conta de e-mail para envio de notificações

## ⚙️ Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/AOP-YOLO.git
   cd AOP-YOLO
   ```

2. Crie um ambiente virtual Python (recomendado):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No macOS/Linux
   # OU
   .venv\Scripts\activate  # No Windows
   ```

3. Instale as dependências:
   ```bash
   pip install ultralytics opencv-python
   ```

4. Certifique-se de que o modelo YOLO está disponível na pasta `models/`:
   - O ficheiro do modelo deve estar em `models/fallDetection.pt`

## 🚀 Como Utilizar

### Executar com câmera em tempo real:

```bash
python finalteste.py
```

Por predefinição, o sistema utiliza a câmera do dispositivo (source=0). Para alterar a fonte de vídeo, modifique o parâmetro `source` no método `run_camera`.

### Executar com um vídeo pré-gravado:

Retire o comentário da linha `fall_system.run_video("video3.mp4")` e comente a linha `fall_system.run_camera(0)` no final do ficheiro `finalteste.py`:

```python
# fall_system.run_camera(0)
fall_system.run_video("video3.mp4")
```

## ⚠️ Configuração das Notificações por E-mail

Por predefinição, o sistema está configurado para enviar e-mails utilizando uma conta Gmail. Para personalizar:

1. Edite as seguintes variáveis na classe `FallDetectionSystem`:
   - `smtp_server` e `smtp_port`: Servidor e porta SMTP
   - `sender_email` e `sender_password`: Credenciais do remetente
   - `recipient_email`: E-mail do destinatário das notificações

## 🕹️ Controlos

- Pressione `q` para sair da aplicação a qualquer momento

## 📊 Parâmetros Configuráveis

- `fall_threshold`: Tempo em segundos que a pessoa deve permanecer caída para gerar um alerta (predefinição: 10 segundos)
- Sensibilidade de deteção: Ajuste o valor de confiança (`conf > 0.5`) no método `process_frame`

## 📝 Notas

- O sistema guarda automaticamente uma imagem (`queda_detetada.jpg`) quando uma queda é detetada
- As notificações por e-mail incluem a imagem capturada e informações sobre o evento