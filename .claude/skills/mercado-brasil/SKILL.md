---
name: mercado-brasil
description: Camada de contexto do mercado e da legislação brasileira para as skills de finanças importadas do marketplace Claude for Financial Services (desenhadas para o mercado americano). Encode uma vez o arcabouço tributário, regulatório, contábil e sucessório do Brasil para que qualquer skill de wealth management, fund admin, KYC/compliance, equity research ou modelagem produza resultado correto para o Brasil — e não a versão US GAAP/SEC padrão. Consulte SEMPRE que o trabalho envolver cliente, ativo, fundo, empresa ou carteira brasileira, ou quando a jurisdição não estiver explícita e o contexto for Brasil. Triggers em "Brasil", "legislação brasileira", "tributação de investimentos", "IR", "come-cotas", "CVM", "B3", "PLD", "COAF", "ITCMD", "previdência", "renda variável", "renda fixa", "offshore", "Lei 14.754", ou qualquer análise financeira em BRL.
---

# Mercado e Legislação — Brasil

Esta é uma **camada de contexto**, não um workflow. As skills importadas (`wealth-management`, `fund-admin`, `equity-research`, `operations`/`kyc`, `financial-analysis`, `private-equity`, etc.) foram escritas para o mercado americano — US GAAP, SEC, wash sale rule, tabela de imposto federal dos EUA, Monte Carlo em ETFs. Quando o trabalho for **brasileiro**, use este documento para sobrescrever essas premissas.

## Regra mestre: estabeleça a jurisdição primeiro

Antes de qualquer análise, defina se o cliente/ativo/fundo é **Brasil**, **exterior (offshore)** ou **misto**. Os três regimes se comportam de forma diferente e a maioria dos erros vem de aplicar a regra do país errado. Na dúvida, e sem sinal de que é EUA, assuma **Brasil** e confirme.

Ao usar uma skill importada com um caso brasileiro, faça três substituições mentais:
1. **Imposto** → troque o tax code dos EUA pelo regime brasileiro (seção 1).
2. **Regulatório/documentos** → troque SEC/FINRA por CVM/B3/Bacen/COAF (seção 2).
3. **Benchmark/moeda** → troque S&P 500 / Treasury por CDI, IPCA, Selic e NTN-B, em BRL (seção 4).

---

## 1. Tributação de investimentos — pessoa física

### 1.1 Renda variável (ações, ETF de ações, BDR, opções, termo, futuros)
- **Swing trade: 15%** sobre o ganho líquido; **day trade: 20%**.
- Apuração **mensal**, por modalidade; recolhimento via **DARF** até o último dia útil do mês seguinte (código 6015). O imposto **não** é retido na fonte (só o "dedo-duro" de 0,005% / 1% no day trade).
- **Compensação de prejuízo apenas dentro da mesma modalidade** (comum não compensa day trade e vice-versa). Prejuízo **não expira**, mas precisa ser declarado no IRPF todo ano para permanecer utilizável.
- **Isenção de R$ 20.000/mês**: vendas de **ações à vista** até R$ 20 mil no mês são isentas. Não vale para ETF, day trade, opções nem exterior. Ganho dentro da isenção **não** consome prejuízo acumulado (o prejuízo seria desperdiçado).

### 1.2 FII / Fiagro
- **Ganho de capital na venda de cotas: 20%** (sem a isenção de R$ 20 mil).
- **Rendimentos distribuídos: isentos** para PF **se** o fundo é listado, tem **≥ 100 cotistas** (Lei 14.754/2023) e o cotista detém **< 10%** das cotas. É bucket fechado — prejuízo de FII só compensa ganho de FII.

### 1.3 Renda fixa e fundos abertos
- **Tabela regressiva, retida na fonte**: 22,5% (≤180d), 20% (181–360d), 17,5% (361–720d), **15% (>720d)**.
- **Come-cotas**: fundos abertos têm antecipação semestral (último dia útil de **maio e novembro**) — 15% (longo prazo) ou 20% (curto prazo). A Lei 14.754/2023 estendeu regras de tributação periódica também a **fundos fechados**.
- **Isentos de IR para PF**: poupança, LCI, LCA, CRI, CRA, debêntures incentivadas (Lei 12.431). Trate-os como isentos ao calcular retorno líquido.

### 1.4 Exterior / offshore (Lei 14.754/2023)
- Aplicações financeiras no exterior e lucros de **controladas (offshore)**: **15%** na apuração **anual** do IRPF (ficha "Bens e Direitos" / aplicações financeiras no exterior).
- Prejuízo no exterior compensa ganho no exterior na mesma apuração anual. Regime de **transparência** opcional para a controlada; **trust** tem tratamento próprio.
- **Sem wash sale**: o Brasil não tem a regra dos 30 dias dos EUA (ver seção 5).

### 1.5 Previdência (PGBL / VGBL)
- **PGBL**: dedutível até **12%** da renda bruta tributável (quem faz declaração completa); no resgate tributa **o valor total**.
- **VGBL**: sem dedução; no resgate tributa **apenas o rendimento**.
- Escolha da tabela: **regressiva** (chega a **10%** após 10 anos — bom para longo prazo) ou **progressiva** (segue a tabela do IR — melhor se o resgate será em faixa baixa).

---

## 2. Regulatório e institucional

| Sigla | Papel | Equivalente US (mental) |
|---|---|---|
| **CVM** | Regulador do mercado de capitais | SEC |
| **B3** | Bolsa (ações, futuros, renda fixa) | NYSE/Nasdaq/CME |
| **Bacen** | Banco Central (câmbio, bancos, Selic) | Fed |
| **ANBIMA** | Autorregulação (fundos, distribuição, certificações) | FINRA (parcial) |
| **COAF/UIF** | Inteligência financeira / PLD-FT | FinCEN |

- **Fundos**: **Resolução CVM 175** (arcabouço atual, substituiu a ICVM 555) — classes e subclasses, responsabilidade limitada do cotista, cotização.
- **Suitability**: Resolução CVM 30 — perfil do investidor obrigatório antes de recomendar.
- **Assessor de investimentos** (ex-agente autônomo): Resolução CVM 178. **Consultor de valores mobiliários**: Resolução CVM 19 (atividade independente, remunerada pelo cliente — relevante para o modelo de family office).

### 2.1 PLD-FT / KYC (crítico para as skills `operations` e `kyc-screener`)
As skills de KYC importadas assumem OFAC/SDN, PEP dos EUA e o Bank Secrecy Act. No Brasil substitua por:
- **Lei 9.613/1998** (lavagem de dinheiro) + **Lei 13.260/2016** (financiamento ao terrorismo).
- **Resolução CVM 50** (PLD-FT no mercado de capitais): cadastro, "conheça seu cliente", monitoramento e **comunicação ao COAF**.
- **PEP**: pessoa exposta politicamente conforme definição da CVM/COAF (não a lista dos EUA). Sanções: observar listas da **ONU/CSNU** e a **Lei 14.286/2021** (câmbio), além de OFAC quando houver exposição a USD.
- Documentos: **CPF/CNPJ**, comprovante de residência, e para PJ o **quadro societário até o beneficiário final (UBO)**.

---

## 3. Contabilidade e reporte de empresas (para `equity-research`, `fund-admin`, modelagem)
- Normas: **CPC**, convergentes com **IFRS** — não US GAAP. Cuidado com diferenças (ex.: leasing, reconhecimento de receita, impairment).
- Companhias abertas reportam à CVM: **ITR** (trimestral) e **DFP** (anual), mais **Formulário de Referência**. Não há 10-K/10-Q; ao usar skills que buscam "SEC filings", redirecione para **RI da empresa / CVM / B3**.
- Demonstrações em **BRL**. IR/CSLL da PJ: lucro real/presumido; JCP (juros sobre capital próprio) é peculiaridade brasileira relevante em valuation e em dividendos.

---

## 4. Benchmark, moeda e macro (para relatórios e performance)
- **Benchmark de retorno**: CDI (pós-fixado), **IPCA** (inflação, para NTN-B e metas reais), **Ibovespa** (renda variável local). Não use S&P 500 como default para carteira brasileira.
- **Taxa livre de risco**: **Selic / Tesouro (NTN-B, LTN, NTN-F)** — não o Treasury dos EUA.
- **Performance sempre líquida e contra o CDI** no material de cliente (é a convenção do consolidado mensal). Retorno em **reais** e, quando houver ativo em dólar, separar efeito câmbio do efeito ativo.
- **Câmbio**: USD/BRL; **IOF** sobre operações de câmbio (alíquota variável — verificar a vigente).

---

## 5. Diferenças que mais causam erro (checklist rápido)
- **Wash sale**: existe nos EUA (30 dias), **não existe no Brasil**. Nunca imponha janela de 30 dias a um caso brasileiro. Único cuidado: vender e recomprar o **mesmo ativo, no mesmo dia, na mesma corretora** é caracterizado como **day trade** (bucket de 20%) — recomprar na sessão seguinte.
- **Compensação de prejuízo**: nos EUA é ampla com limite anual de US$ 3.000 contra renda ordinária; no Brasil é **só dentro da modalidade**, sem esse limite e **sem prazo de expiração** (desde que declarado anualmente).
- **Sucessão**: nos EUA é estate tax federal + step-up. No Brasil é **ITCMD estadual** (alíquotas por estado, tendência de progressividade com a EC 132/2023 da Reforma Tributária), **sem step-up**; ferramentas típicas são **holding familiar**, doação em vida com usufruto e previdência (VGBL geralmente fora do inventário).
- **Contas**: EUA distingue taxable / IRA / 401(k) / Roth. No Brasil o eixo é **conta comum × previdência (PGBL/VGBL) × offshore**, cada um com regime próprio (seções 1.1–1.5).

---

## Nota importante
Este documento é uma referência de trabalho para orientar as skills, **não é aconselhamento jurídico ou tributário**. A legislação brasileira muda com frequência (medidas provisórias, resoluções CVM, Reforma Tributária). Antes de entregar material ao cliente, **confirme a regra vigente** — em especial alíquotas de IOF/ITCMD, requisitos de isenção de FII e o estado atual de MPs em tramitação (ex.: a MP 1.303/2025, que previa expiração de prejuízo em 5 anos, **caducou sem virar lei** e não é regra vigente). Na dúvida sobre um ponto específico, sinalize a incerteza em vez de afirmar.
