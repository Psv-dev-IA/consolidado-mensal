# Consolidado e report mensal

Skill para Claude que produz o material mensal que um consultor de investimentos envia para os
clientes dele. Você anexa os relatórios das instituições e recebe de volta um arquivo com a sua
marca, em HTML e em PDF.

O material tem duas partes:

1. **O consolidado.** Quanto a carteira rendeu no período, em reais e em porcentagem, e como isso
   se compara ao CDI.
2. **O report.** A leitura do que aconteceu no mercado naquele intervalo, escrita para quem não é
   do mercado financeiro.

Fora do arquivo, no chat, vem um **bloco de sinalizações** com as ressalvas encontradas. Ele é só
do consultor e nunca vai junto para o cliente.

Lê relatório de qualquer instituição, brasileira ou estrangeira, um ou vários de uma vez. Carteira
em moeda estrangeira sai nas duas moedas, com a conversão pela PTAX do Banco Central e um quadro
separando o que foi rendimento do ativo e o que foi câmbio.

---

## Como instalar, três caminhos

Escolha um. O primeiro é o mais confortável para quem vai usar todo mês.

### 1. Projeto no Claude, recomendado

1. Crie um Projeto no Claude.
2. Suba os arquivos deste repositório para os arquivos do projeto.
3. Cole o conteúdo de [`docs/instrucoes-do-projeto.md`](docs/instrucoes-do-projeto.md) nas
   instruções do projeto, junto com a sua identidade visual.
4. Todo mês, abra uma conversa no projeto, anexe os relatórios e escreva
   **Consolidado e report de [mês]**.

### 2. Skill instalada

Baixe `consolidado-mensal.zip` e instale como skill na sua conta. A partir daí ela é acionada
sozinha quando você anexar relatório e pedir o consolidado do mês.

### 3. Prompt avulso, sem instalar nada

Abra uma conversa nova, cole o conteúdo de
[`docs/prompt-consolidado-mensal.md`](docs/prompt-consolidado-mensal.md), anexe os relatórios e
mande. Funciona em qualquer conversa, sem projeto e sem skill instalada.

---

## O que tem em cada arquivo

| Arquivo | Para que serve |
|---|---|
| `SKILL.md` | O orquestrador. Abertura com o consultor, sequência de trabalho, regras gerais e a conferência final |
| `references/leitura-e-calculo.md` | Como ler cada layout de relatório, o que conta como aporte, cálculo de rentabilidade, consolidação de várias instituições, carteira internacional |
| `references/report-mercado.md` | Como escrever a Parte 2, regra de peso entre Brasil e Exterior, números obrigatórios, fontes preferenciais |
| `references/identidade-visual.md` | Paleta, logo, fontes, o que a marca pode e não pode mudar |
| `assets/template-material.html` | O HTML do material, com as variáveis de cor no `:root` |
| `assets/identidade-modelo.md` | Ficha de identidade para o consultor preencher uma vez |
| `scripts/extrair_cores.py` | Lê a paleta direto da logo e devolve as cinco variáveis CSS |
| `docs/como-usar.md` | Uma página para entregar ao consultor |
| `docs/prompt-consolidado-mensal.md` | Versão em prompt avulso |
| `docs/instrucoes-do-projeto.md` | Bloco para colar nas instruções de um Projeto no Claude |

---

## Cores, sem precisar saber hexadecimal

O consultor anexa a logo e a paleta sai dela:

```bash
python scripts/extrair_cores.py caminho/para/logo.png
```

```json
{
  "paleta": {
    "--cor-principal": "#1A395B",
    "--cor-secundaria": "#EEF1F3",
    "--cor-texto": "#050C14",
    "--cor-negativo": "#B3261E",
    "--cor-linha": "#CCD3DA"
  }
}
```

Basta colar o bloco `paleta` no `:root` do template. Aceita png, jpg e svg. Precisa de Pillow.

Se o consultor tiver manual de marca em PDF, é melhor ainda: anexa o manual e recebe de volta um
`identidade-[marca].md` pronto, com a logo recortada e os hex lidos da página de paleta.

---

## O que ela não faz, de propósito

- **Não recomenda carteira.** Nada de sugerir compra, venda, aumento, redução ou realocação
- **Não faz projeção.** O material é sobre o que já aconteceu
- **Não abre a carteira ativo a ativo.** O consolidado responde quanto rendeu, não o que rendeu
- **Não inventa número.** Dado que não existe no relatório sai como "não consta no relatório",
  com o registro nas sinalizações

---

## Aviso

Material informativo. O resultado depende dos relatórios anexados e da disponibilidade das fontes
de mercado no momento da geração. Confira os números antes de enviar ao cliente.
