# Projeto Lightless - PHYSICAL COMPUTING IOT

## Grupo:
Octávio Hernandez Chiste Cordeiro – RM 97894 |
Rafael Perussi Caczan – RM 93092 |
Sabrina Flores – RM 550781

## Descrição do Problema

Durante apagões, ambientes críticos perdem funcionalidades essenciais de comunicação e segurança. A ausência de iluminação e a indisponibilidade de sistemas conectados tornam difícil a comunicação de pedidos de ajuda ou alerta, especialmente por pessoas com deficiência visual ou mobilidade reduzida.

## Visão Geral da Solução

Link para vídeo demonstrativo: https://www.youtube.com/watch?v=1FUd2L_E3yg&feature=youtu.be

*Lightless* é uma aplicação em Python que utiliza a biblioteca MediaPipe para detectar gestos simples em tempo real via webcam. A aplicação roda localmente, sem necessidade de internet ou hardware adicional, o que a torna ideal para ambientes sob queda de energia, desde que com suporte de nobreak ou bateria.

### Gestos Suportados:

- **Palma da mão levantada** → "Sinal de atenção"
- **Punho fechado** → "Alerta urgente"
- **Dois braços erguidos** → "Emergência detectada"

A detecção é feita via webcam, mesmo em baixa luminosidade, e os eventos são registrados visualmente em tela com logs persistentes.

## Instruções de Execução

### Pré-requisitos

- Python 3.8 ou superior  
- pip  
- Webcam funcional  
- Sistema operacional compatível (Windows ou Linux)

### Instalação

```bash
pip install opencv-python mediapipe

