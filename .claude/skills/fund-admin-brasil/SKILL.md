---
name: fund-admin-brasil
description: Camada de contexto de administração e contabilidade de fundos de investimento no Brasil para as skills de fund admin importadas do marketplace Claude for Financial Services (desenhadas para o mercado americano, US GAAP e estrutura de partnership/LP). Sobrescreve as premissas dos EUA das skills `fund-admin` (gl-recon, nav-tieout, accrual-schedule, roll-forward, variance-commentary) e do `month-end-closer` para que cálculo de cota, marcação a mercado, apropriação de taxas, come-cotas e fechamento produzam resultado correto sob o regime CVM/ANBIMA — e não a versão US GAAP. Consulte SEMPRE que o trabalho envolver fundo, cota, NAV, patrimônio líquido, administração de fundos ou fechamento de fundo brasileiro. Triggers em "fundo", "administração de fundos", "come-cotas", "CVM 175", "NAV", "cota", "marcação a mercado", "FII", "Fiagro", "patrimônio líquido", "taxa de administração", "taxa de performance", "fechamento de fundo", "cotização", "linha d'água", "high-water mark".
---

# Administração e Contabilidade de Fundos — Brasil

Esta é uma **camada de contexto de domínio**, não um workflow. As skills de fund admin importadas (`fund-admin`: `gl-recon`, `nav-tieout`, `accrual-schedule`, `roll-forward`, `variance-commentary`, `break-trace`; e `month-end-closer`) foram escritas para o mercado americano — US GAAP, estrutura de partnership/LP com capital accounts e K-1, fund accounting no modelo americano. Quando o fundo for **brasileiro**, use este documento para sobrescrever essas premissas.

Este overlay pressupõe a fundação **`mercado-brasil`** para o pano de fundo tributário, regulatório e contábil (regime de IR, CVM/B3/ANBIMA, CPC/IFRS, come-cotas geral). Aqui o foco é o **específico de administração de fundos**: estrutura CVM 175, cálculo da cota e do PL, marcação a mercado, apropriação de taxas e o fechamento. Consulte `mercado-brasil` para qualquer ponto de imposto ou macro que não esteja detalhado abaixo.

## Regra mestre: fundo brasileiro não é partnership americana

As skills assumem um veículo americano — cotista como *limited partner*, *capital account* por investidor, alocação de P&L via *waterfall*, *K-1* no fim do ano, US GAAP na contabilidade. **No Brasil isso não existe assim.** O veículo é o **fundo de investimento** regido pela **Resolução CVM 175/2022**, o investidor é **cotista** (detém cotas homogêneas, não um capital account individual), e o resultado é refletido no **valor da cota** — não em alocação de P&L por sócio. Faça três substituições mentais ao usar qualquer skill de fund admin:

1. **Contabilidade** → US GAAP / ASC vira **CPC/IFRS + plano contábil e normas da CVM** (marcação a mercado padrão **ANBIMA**).
2. **Estrutura** → LP/GP, capital accounts, K-1 e *side pockets* viram **cotas / classes / subclasses (CVM 175)**, com apuração de resultado pelo **valor da cota**.
3. **Tributação** → tax code dos EUA vira **regime brasileiro** com o divisor de águas do **come-cotas** (seção 5) — muitas skills não têm análogo a isto.

### Mapa EUA → Brasil

| Conceito na skill (EUA) | Equivalente no Brasil |
|---|---|
| US GAAP / ASC 946 (investment companies) | CPC/IFRS + normas contábeis da CVM |
| Investor capital account / K-1 | Posição em **cotas**; informe de rendimentos |
| Partnership allocation / waterfall | **Valor da cota** (PL / nº de cotas); classes e subclasses |
| Mark-to-market (fair value, ASC 820) | **Marcação a mercado padrão ANBIMA** |
| Management fee / incentive fee + hurdle | **Taxa de administração** + **taxa de performance** com **linha d'água** (high-water mark) |
| NAV per share | **Valor da cota** (cota de abertura vs cota de fechamento) |
| Administrator / custodian / auditor | Papéis segregados da CVM 175 (seção 1) |
| Fund tax withholding (US) | **Come-cotas** + IR na fonte (seção 5) |

---

## 1. Estrutura CVM 175 (arcabouço atual — substituiu a ICVM 555)

- Vigência **escalonada a partir de 2023–2024**. Traz duas mudanças estruturais que quebram o modelo americano das skills:
  - **Classes e subclasses de cotas** dentro de um mesmo fundo: um fundo pode ter várias classes (com carteiras/tributação/público-alvo distintos) e cada classe pode ter subclasses (que diferem em taxas, aportes mínimos, público). O antigo "fundo = uma carteira = uma cota" não vale mais — reconcilie e apure a cota **por classe/subclasse**, não só no nível do fundo.
  - **Responsabilidade limitada do cotista**: por padrão o cotista pode ter responsabilidade limitada ao valor de suas cotas (rompe com a premissa de *unlimited/capital-call* de LP americana).
- **Papéis segregados** (não confundir na conciliação e no roll-forward — cada um tem escrituração/fonte própria):

| Papel | Função |
|---|---|
| **Administrador** | Responsável legal pelo fundo perante a CVM; constituição, escrituração, cálculo da cota (função de fund admin) |
| **Gestor** | Decisões de investimento e ordens (portfolio management) |
| **Custodiante** | Guarda dos ativos, liquidação, registro de titularidade |
| **Distribuidor** | Colocação de cotas junto aos investidores |
| **Auditor independente** | **Auditoria obrigatória** das demonstrações do fundo |

- Demonstrações e plano contábil seguem as **normas da CVM**; **auditoria independente é obrigatória**. Não há 10-K/10-Q — o reporte é o do regime CVM/ANBIMA.

---

## 2. Cálculo da cota e do patrimônio líquido (NAV)

- **Patrimônio líquido (PL)** = ativos a **mercado** − passivos (taxas a pagar, provisões, resgates a liquidar, etc.).
- **Valor da cota** = **PL / número de cotas em circulação**. É o análogo do NAV per share — mas apurado no nível do fundo **e de cada classe/subclasse**.
- **Cota de abertura × cota de fechamento**:
  - **Cota de abertura**: calculada no início do dia (comum em fundos de renda fixa/DI) — aportes e resgates do dia entram pela cota já conhecida.
  - **Cota de fechamento**: calculada após o fechamento do mercado, refletindo a marcação do dia (regra geral para renda variável e multimercado).
  - Ao rodar `nav-tieout`, confirme **qual convenção o fundo usa** antes de comparar cota calculada × cota do administrador — usar a convenção errada gera "break" falso.
- **Cotização** (prazos de conversão e liquidação, D+n de aplicação e resgate) afeta quando aportes/resgates entram no nº de cotas e quando viram caixa. É fonte comum de quebra em conciliação de caixa vs cotas.

---

## 3. Marcação a mercado (MtM)

- Padrão **ANBIMA** de marcação a mercado. Ativos são avaliados a **valor de mercado**, não "na curva".
- **Renda fixa em fundos é marcada a mercado** (não a curva), salvo exceções previstas na regulação/manual (ex.: certos casos de carteira que carrega até o vencimento com público e condições específicas). Ao portar uma skill que assume *held-to-maturity/amortized cost* como default, **inverta**: em fundo o default é MtM.
- A marcação alimenta diretamente o PL e, portanto, o valor da cota do dia. Divergência de fonte de preço (administrador × gestor × custodiante) é causa clássica de variação inexplicada — trate na `variance-commentary` e no `break-trace`.

---

## 4. Apropriação de taxas

- **Taxa de administração**: percentual **ao ano sobre o PL**, **apropriada (provisionada) diariamente** — reduz o PL e a cota todo dia, de forma pro rata (base 252 dias úteis ou 360, conforme o regulamento). No `accrual-schedule`, o accrual da adm é **diário e linear sobre o PL**, não um lançamento mensal fixo.
- **Taxa de performance**: geralmente cobrada sobre o que exceder um **benchmark** — **CDI**, **IPCA+**, **Ibovespa**, etc. — com **conceito de linha d'água (high-water mark)**:
  - Só há cobrança quando a cota supera o benchmark **e** o ponto máximo já cobrado anteriormente (a "linha d'água"). Perdas precisam ser recuperadas antes de nova cobrança.
  - Período de apuração e cobrança segue o **regulamento do fundo** — tipicamente **semestral** (confirmar no regulamento).
  - No accrual, a performance é **provisionada** conforme o desempenho relativo ao benchmark evolui e **revertida** se a cota recuar abaixo da linha d'água. Não trate como fee fixo.
- Ambas reduzem o PL antes do cálculo da cota de fechamento — a ordem importa na conciliação.

---

## 5. Tributação e come-cotas (o divisor de águas)

Consulte `mercado-brasil` §1.3 para a tabela regressiva completa. O ponto crítico de fund admin é o **come-cotas**:

- **Come-cotas** = antecipação **semestral** de IR em **fundos abertos**, no **último dia útil de MAIO e de NOVEMBRO**, à alíquota de **15%** (fundos de **longo prazo**) ou **20%** (curto prazo), **retida em cotas** (reduz o nº de cotas do investidor, não o valor da cota). No resgate, cobra-se apenas a diferença até a alíquota da tabela regressiva.
- **Fundos de ações**: tributação de **15% apenas no resgate**, **sem come-cotas**.
- **Fundos fechados**: a **Lei 14.754/2023** passou a submetê-los à **tributação periódica (come-cotas) a partir de 2024**, com a tributação do **estoque** como **evento de transição**. (Antes, fundo fechado só tributava no resgate/amortização — premissa que muitas referências antigas ainda repetem; sinalize se a data do trabalho for pré-2024.)

### Quem tem e quem não tem come-cotas

| Tipo de fundo | Come-cotas? | Observação |
|---|---|---|
| Fundo aberto de RF / multimercado (longo prazo) | **Sim** | 15%, maio e novembro |
| Fundo aberto de curto prazo | **Sim** | 20% |
| Fundo **fechado** | **Sim (desde 2024)** | Lei 14.754/2023; estoque tributado na transição |
| Fundo de **ações** | **Não** | 15% só no resgate |
| **ETF** de ações | **Não** | — |
| **FII / Fiagro** | **Não** | Ver seção 6 |
| **Previdência (PGBL/VGBL)** | **Não** | Regime próprio (regressivo/progressivo) |
| Fundos **incentivados/isentos** (ex.: debêntures Lei 12.431) | **Não** | Isentos |

---

## 6. FII / Fiagro

- **Rendimentos distribuídos: isentos de IR para PF** se cumpridos os requisitos: fundo **listado** em bolsa/balcão, **≥ 100 cotistas** (Lei 14.754/2023) e cotista detém **< 10%** das cotas / dos rendimentos.
- **Ganho de capital na venda de cotas: 20%** (sem a isenção de R$ 20 mil das ações à vista).
- **Não têm come-cotas.** Na administração, o fluxo relevante é a **distribuição de rendimentos** (mensal, em geral), não a marcação de resultado tributável periódico.

---

## 7. Fechamento mensal — contexto brasileiro para as skills

Ao rodar `gl-recon`, `nav-tieout`, `accrual-schedule`, `roll-forward`, `variance-commentary` e o `month-end-closer` em um fundo brasileiro:

- **`accrual-schedule`** → accruals que importam: **taxa de administração diária** sobre o PL; **taxa de performance** provisionada contra benchmark com **linha d'água** (provisiona e reverte); provisão de auditoria/custódia; e, no fim de **maio/novembro**, a **provisão de come-cotas**. Não use o calendário de accruals americano (management/incentive fee no modelo LP).
- **`roll-forward`** → PL inicial + aportes − resgates + resultado (MtM + rendimentos − despesas − taxas) − come-cotas (nos meses aplicáveis) = PL final. Concilie **em cotas e em reais**, e **por classe/subclasse** — a cotização (D+n) explica descasamentos entre "cotas emitidas/resgatadas" e "caixa movimentado".
- **`gl-recon` / `nav-tieout`** → concilie o razão contábil (plano CVM) e a cota calculada contra a **fonte do administrador** e a **posição do custodiante**. Confirme a **convenção de cota (abertura × fechamento)** e a **fonte de preço (ANBIMA)** antes de abrir break.
- **`variance-commentary` / `break-trace`** → causas típicas de variação: diferença de **marcação a mercado** entre fontes, timing de **cotização**, **come-cotas** no mês de maio/novembro, e reversão de **provisão de performance**. Comente em **BRL** e, quando houver benchmark, contra **CDI/IPCA/Ibovespa** (não S&P 500).
- Retorno e desempenho do cliente: **líquidos e contra o CDI**, em reais — convenção do material brasileiro (ver `mercado-brasil` §4).

---

## Nota importante
Este documento é uma referência de trabalho para orientar as skills, **não é aconselhamento jurídico, contábil ou tributário**. A legislação e a regulação brasileira de fundos mudam com frequência (resoluções e anexos da CVM 175, atos ANBIMA, medidas provisórias, Reforma Tributária). Antes de entregar material ao cliente, **confirme a regra vigente** — em especial alíquotas e datas de come-cotas, requisitos de isenção de FII/Fiagro, o cronograma de vigência da CVM 175 e o tratamento de fundos fechados sob a Lei 14.754/2023. Na dúvida sobre um ponto específico, sinalize a incerteza em vez de afirmar.
