---
name: equity-research-brasil
description: Camada de contexto para equity research e análise de ações brasileiras, sobrescrevendo as premissas americanas (SEC, 10-K/10-Q, consenso I/B/E/S, bolsas dos EUA) das skills do plugin `equity-research` — earnings-analysis, earnings-preview, initiating-coverage, model-update, sector-overview, thesis-tracker, morning-note, idea-generation, catalyst-calendar — e do agente `earnings-reviewer`. Consulte SEMPRE que a análise envolver empresa listada na B3, cobertura, tese ou resultado trimestral de companhia brasileira. Triggers em "equity research", "análise de ações", "cobertura", "initiating coverage", "B3", "Ibovespa", "ITR", "DFP", "formulário de referência", "fato relevante", "JCP", "juros sobre capital próprio", "múltiplos", "resultado trimestral", "balanço", "teleconferência de resultados", "consenso", "P/L", "EV/EBITDA", "P/VPA", "dividend yield", "payout".
---

# Equity Research — Brasil

Esta é uma **camada de contexto de domínio**, não um workflow. Ela se apoia na fundação **`mercado-brasil`** (tributação, regulatório, contábil, macro) e a especializa para **análise de ações**. As skills do plugin `equity-research` e o agente `earnings-reviewer` foram escritos para o mercado americano — SEC, 10-K/10-Q, earnings call trimestral no padrão US, consenso I/B/E/S, bolsas NYSE/Nasdaq, US GAAP. Quando o alvo for uma **companhia listada na B3**, use este documento para sobrescrever essas premissas.

Leia a fundação `mercado-brasil` primeiro (seções 3 e 4, contabilidade e benchmark). Este overlay assume aquele contexto e não o repete.

## Regra mestre: reescreva as três premissas americanas

Toda skill de research importada carrega três premissas dos EUA que quebram no Brasil. Substitua-as antes de rodar qualquer análise:
1. **Divulgações** → SEC filings (10-K/10-Q/8-K) **não existem**. Use ITR/DFP/FRE via CVM, RI e B3 (seção 1).
2. **Consenso** → I/B/E/S padronizado **não é a norma local**. Use consenso de casas locais / Bloomberg / Refinitiv / Bigdata.com (seção 3).
3. **Remuneração ao acionista** → nos EUA é dividendo + buyback. No Brasil é **dividendo + JCP**, com tratamento fiscal oposto entre eles (seção 5). Isso é o erro mais comum e mais material em valuation.

---

## 1. Mapa EUA → Brasil (divulgações e eventos)

| Conceito US (nas skills) | Equivalente Brasil | Onde buscar |
|---|---|---|
| 10-K (anual) | **DFP** — Demonstrações Financeiras Padronizadas | CVM (Empresas.NET), RI da empresa |
| 10-Q (trimestral) | **ITR** — Informações Trimestrais (1T, 2T, 3T; o 4T sai dentro da DFP) | CVM, RI |
| Registrant / business description | **Formulário de Referência (FRE)** — fatores de risco, capital, governança, remuneração, partes relacionadas | CVM, RI |
| 8-K (material event) | **Fato relevante** e **comunicado ao mercado** | CVM, RI, B3 |
| Proxy statement / DEF 14A | Edital de convocação, **proposta da administração (AGO/AGE)** | CVM, RI |
| SEC (regulador de divulgação) | **CVM** (sistema Empresas.NET) | cvm.gov.br |
| Earnings call | **Teleconferência / webcast de resultados** (release + apresentação + call, geralmente em PT e EN) | RI |
| Ticker + exchange | Ticker B3 (ex.: PETR4, VALE3, ITUB4); ADRs negociam na NYSE (ex.: VALE, ITUB) | B3, NYSE (ADR) |
| GAAP | **CPC / IFRS** (ver `mercado-brasil` §3) | — |

**Regra prática:** onde uma skill diz "pull the latest 10-K/10-Q" ou "SEC filings", redirecione para **RI da empresa → CVM → B3**, nessa ordem de conveniência. O release trimestral (fato/press release do RI) costuma trazer o número gerencial antes do ITR auditado; cite qual você usou.

O 4T merece atenção: **não há ITR do 4º trimestre** — o número "4T" que o mercado usa é derivado (DFP anual menos os três ITRs) e vem no release de resultados anual. Não procure um "ITR do 4T" na CVM.

---

## 2. Onde buscar dados (equity research Brasil)

- **Divulgações primárias**: CVM (Empresas.NET / dados abertos), site de **RI** da companhia, e **B3** (cotações, composição de índices, calendário corporativo, proventos).
- **Consenso e estimativas**: **Bloomberg**, **Refinitiv/LSEG**, **Bigdata.com**, e relatórios de **casas locais** (research de bancos e corretoras). Não assuma cobertura I/B/E/S ampla — muitas small caps têm 1–3 casas cobrindo, ou nenhuma. Sinalize baixa cobertura.
- **Macro**: Bacen (Selic/COPOM, Focus), IBGE (IPCA, PIB), FGV (IGP-M), Tesouro. Ver `mercado-brasil` §4.
- **Proventos e datas**: agenda de eventos corporativos da B3 e do RI (data-com, data-ex, pagamento de dividendos/JCP).

---

## 3. Consenso e estimativas

O consenso brasileiro é **menos padronizado** que o americano:
- Cobertura mais rala, sobretudo fora do Ibovespa; o "consenso" pode ser média de poucas casas — reporte o **número de estimativas** (n) junto com a média.
- Definições de lucro variam (com/sem JCP no payout, lucro recorrente vs. reportado, ajustes não-recorrentes distintos entre casas). Ao comparar "beat/miss", **fixe a mesma base** de comparação.
- Prefira **lucro recorrente / ex-itens não-recorrentes** para a leitura de tendência, mas ancore o headline no reportado.

---

## 4. Peculiaridades do resultado trimestral brasileiro

Ao rodar `earnings-analysis`, `earnings-preview` e `model-update` para uma empresa brasileira, cheque:
- **Sazonalidade / safra**: forte em agro, açúcar/etanol, varejo (4T e Black Friday/Natal), turismo, energia (hidrologia/PLD). Compare **ano contra ano (YoY)**, não sequencial (QoQ), quando a sazonalidade domina.
- **Inflação e indexação**: muitas receitas são contratos indexados a **IPCA / IGP-M** (concessões, aluguéis, saneamento, energia). Reajustes anuais movem margem — separe efeito **preço/reajuste** de **volume**.
- **Câmbio e hedge**: exportadoras (Vale, Suzano, frigoríficos, petróleo) e empresas com dívida/insumo em USD. Distinga **efeito operacional do câmbio** de **variação cambial não-caixa sobre dívida** (que infla/deflaciona o lucro líquido sem caixa). Verifique política de **hedge** e sua marcação.
- **Juros altos**: a Selic pesa no **resultado financeiro** de empresas alavancadas — a leitura do lucro líquido pode ser dominada por despesa financeira, não pela operação. Foque **EBITDA e geração de caixa** para a operação.
- **JCP**: ver seção 5 — entra no resultado como despesa dedutível (afeta a linha fiscal) e é forma de remuneração ao acionista.
- **Não-recorrentes**: impairment, créditos tributários (ex.: exclusão do ICMS da base de PIS/COFINS — "tese do século"), reversões de provisão. Isole-os.

---

## 5. Dividendos vs. JCP (tratar SEPARADAMENTE)

O erro mais material do research importado é tratar remuneração ao acionista como nos EUA. No Brasil há **dois instrumentos distintos**:

| | Dividendo | JCP (Juros sobre Capital Próprio) |
|---|---|---|
| Base legal | Lei das S.A. | **Lei 9.249/1995** |
| Efeito na empresa | pago do lucro após IR | **dedutível** de IRPJ/CSLL → **escudo fiscal** (reduz imposto da empresa) |
| Tributação do acionista PF | **isento** de IR (regime vigente — **monitorar Reforma Tributária**) | **15% retido na fonte** |
| Limite | dividendo mínimo obrigatório conforme estatuto | limitado pela TJLP/TLP sobre o PL e por % do lucro/reservas |

Implicações para valuation e cobertura:
- **Dividend yield**: some dividendo + JCP para o yield **bruto**, mas calcule também o **yield líquido** ao acionista PF (JCP sofre 15%). Deixe claro qual está reportando.
- **Payout**: empresas otimizam pagando JCP até o limite (economia fiscal ~34% na empresa) e o excedente em dividendo. Um payout "alto" via JCP tem custo fiscal menor para a empresa.
- **Modelagem**: o JCP reduz a alíquota efetiva da empresa — não modele a carga cheia de ~34% (IRPJ 15% + adicional 10% + CSLL 9%; ver `mercado-brasil`) ignorando o escudo do JCP.
- **Bancos e seguradoras** são usuários intensivos de JCP — essencial acertar aqui.

---

## 6. Múltiplos e comps na B3

- **Múltiplos usuais**: **P/L**, **EV/EBITDA**, **P/VPA** (essencial para **bancos** e seguradoras, onde EV/EBITDA não faz sentido — use também **ROE**, P/L e P/VPA), **dividend yield**, EV/EBIT. Para bancos, foque **ROE, ROAE, índice de Basileia, inadimplência, NII, custo de crédito**.
- **Peers vêm da B3**, por setor e liquidez, não de peers globais automáticos. Cuidado ao comparar um banco brasileiro com money-center dos EUA — estruturas de capital, spread e regulação diferem.
- **Carga tributária de bancos/seguradoras é maior**: a CSLL de instituições financeiras é **majorada** frente aos 9% gerais (esteve em 15–20% em diferentes períodos), elevando a alíquota efetiva acima dos ~34% do lucro real geral. Não aplique os ~34% cheios a banco sem **confirmar a alíquota vigente** de CSLL do setor financeiro.
- **Ajustes**: normalize lucro por não-recorrentes e por **JCP** antes de comparar P/L entre pares (uma paga JCP, outra não). Ajuste EBITDA pela política de leasing (IFRS 16) se houver divergência entre empresas.
- **Liquidez**: muitas ações fora do Ibovespa têm baixo volume — sinalize risco de liquidez e desconto de iliquidez; múltiplo de comp pode estar distorcido por poucos negócios.

---

## 7. Governança e classes de ação

A skill `initiating-coverage` deve descrever a estrutura de governança no padrão B3:
- **Segmentos de listagem** (do mais ao menos exigente): **Novo Mercado** (só ON, tag along 100%, free float mínimo), **Nível 2**, **Nível 1**, **tradicional**. O segmento afeta direitos do minoritário e costuma justificar prêmio/desconto de governança.
- **Classes de ação**: **ON (ordinária, com voto)** e **PN (preferencial, sem voto ou voto restrito, geralmente prioridade em dividendo)**. Empresas fora do Novo Mercado costumam ter ON + PN (ex.: PETR3/PETR4, ITUB3/ITUB4). O ticker ".3" = ON, ".4" = PN; units (".11") empacotam ON+PN.
- **Tag along**: percentual do preço garantido ao minoritário em troca de controle — 100% no Novo Mercado, menor ou inexistente para PN fora dele. É item de tese, não detalhe.
- **Controle**: muitos casos de **controlador definido** (família, Estado, holding) — avalie risco de conflito de interesse, partes relacionadas (no FRE) e o histórico de tratamento do minoritário.

---

## 8. Setores regulados (contexto para sector-overview e teses)

Grande parte do índice é de setores regulados, com receita/tarifa indexada e regulador próprio:

| Setor | Regulador | Notas para a tese |
|---|---|---|
| Bancos | **Bacen** | Basileia, provisão de crédito, spread; use P/VPA e ROE |
| Energia elétrica | **ANEEL** | receita regulada, ciclos tarifários, RAB, indexação a IPCA/IGP-M, risco hidrológico |
| Saneamento | (estadual + marco do saneamento) | contratos de longo prazo, metas de universalização, reajuste por índice |
| Telecom | **Anatel** | capex intensivo, concessão/autorização |
| Petróleo e gás | **ANP** | preço de paridade de importação, royalties, ciclo de commodity |
| Saúde / planos | **ANS** | sinistralidade, reajuste regulado dos planos |

Para esses setores, o driver da tese é frequentemente **regulatório** (revisão tarifária, renovação de concessão, marco legal) e **indexação inflacionária**, não só demanda.

---

## 9. Calendário de catalisadores (catalyst-calendar / morning-note)

Ao montar agenda de catalisadores, inclua os eventos brasileiros — não o calendário do Fed/BLS:
- **Datas de resultado** (agenda B3/RI) e teleconferências.
- **COPOM** (decisão de Selic, ~8 reuniões/ano) — driver macro central para bancos, alavancadas e desconto de fluxo.
- **IPCA** (IBGE, mensal) e **IGP-M** (FGV) — indexadores de receita e âncora de juro real.
- **Boletim Focus** (Bacen, semanal) — revisões de expectativa.
- **Eventos corporativos**: data-com/data-ex de dividendos e JCP, AGO/AGE, revisões tarifárias (ANEEL), leilões (energia, transmissão, óleo), safra (agro).
- **Rebalanceamento de índices** (Ibovespa quadrimestral: jan/mai/set) — entradas/saídas movem fluxo passivo.
- Macro externo relevante para commodities e câmbio (Fed, dados da China para Vale/siderurgia).

---

## 10. Índices e benchmark de tese

- **Ibovespa** — principal; benchmark padrão de ação brasileira (não S&P 500).
- **IBrX-100** — 100 ações mais líquidas (ponderação por valor de mercado free float).
- **SMLL** — small caps.
- **IDIV** — carteira de dividendos (útil para tese de renda).
- Ao avaliar performance relativa de uma ação ou setor, use o índice **local** apropriado; ao comparar com par global (ex.: Vale vs. BHP), explicite câmbio e diferenças regulatórias/fiscais.

---

## Nota importante
Este documento é uma referência de trabalho para orientar as skills de equity research, **não é aconselhamento de investimento, jurídico ou tributário, nem recomendação de compra ou venda**. A legislação e a regulação brasileiras mudam com frequência (resoluções CVM/B3, Reforma Tributária, marcos setoriais). Em especial, **a isenção de IR sobre dividendos na pessoa física e a tributação do JCP podem ser alteradas pela Reforma Tributária — trate como ponto a monitorar** e confirme a regra vigente antes de usar em valuation ou material de cliente. Requisitos de listagem, alíquotas e regras setoriais devem ser verificados na fonte primária (CVM, B3, RI, reguladores). Na dúvida sobre um ponto específico, sinalize a incerteza em vez de afirmar.
