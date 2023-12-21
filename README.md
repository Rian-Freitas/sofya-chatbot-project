# Chatbot Sofya: Guia Oncológico Virtual

![Imagem do WhatsApp de 2023-12-01 à(s) 12 43 57_7c0aa947](https://github.com/Rian-Freitas/sofya-chatbot-project/assets/85463854/00232d05-7265-41be-b7d2-b512996b79c8)

Repositório reservado para o modelo e a interface do nosso projeto de Chatbot guia de oncologia.

### Membros

- Rian Freitas
- Dominique Vargas
- Lindsey Vargas
- Bernardo Vargas

### Objetivos

Com base em guias de oncologia para cuidados, posologia e indicações para pacientes como tumores, no formato PDF, criamos um modelo de _transformer_ da OpenAI capaz de indexar esses documentos em um vetor de armazenamento, associado a uma interface gráfica em que o usuário pode enviar _queries_ ao sistema, que consulta no vetor.

### Bibliotecas utilizadas

- Flask 2.2.5
- Llama Index 0.9.12
- PyPDF 3.17.1
- Accelerate 0.25.0

### Como utilizar

Apenas rode o arquivo `test.py` e espere o tempo de carregamento até o terminal responder com um URL da aplicação Flask. Basta usar `CTRL + Click` na URL ou copiar e colar no navegador de sua preferência.

*Projeto realizado no Field Project, na Escola de Matemática Aplicada da FGV, 2023.*
