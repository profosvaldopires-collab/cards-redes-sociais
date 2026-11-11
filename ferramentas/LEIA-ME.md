# Padrão visual dos cards

- `modelo_cards.py`: gerador de referência (Pillow + fonte Poppins). Cards 1080x1080, fundo #F7F4EC, azul #0634A5, dourado #CC981C, borda azul, rodapé "Prof. Osvaldo Pires | Licitações e Contratos".
- Estrutura de um carrossel "Acórdão em 60s": capa (pergunta + "ARRASTE →"), regra, erro comum, na prática, detalhe, consequência, para guardar (CTA), card final com a foto oficial (`assets/foto-oficial.jpg`).
- Cada post aprovado fica numa pasta `AAAA-MM-DD-tema/` com `01.png` ... `08.png`.
- Link público de cada imagem: `https://raw.githubusercontent.com/profosvaldopires-collab/cards-redes-sociais/main/<pasta>/<arquivo>`.
