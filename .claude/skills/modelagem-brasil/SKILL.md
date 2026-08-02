---
name: modelagem-brasil
description: Camada de contexto para MODELAGEM FINANCEIRA E VALUATION no Brasil, sobrescrevendo as premissas americanas das skills de modelagem importadas do marketplace Claude for Financial Services (financial-analysis, model-builder, pitch-agent) — dcf-model, lbo-model, comps-analysis e 3-statement-model, que assumem Treasury dos EUA como risk-free, tax rate federal americano (~21%) e mercado de dívida dos EUA. Encode a construção do WACC no Brasil, custo de capital próprio e de dívida locais, consistência moeda×taxa×inflação, imposto IRPJ+CSLL (~34%), JCP, terminal value em ambiente de juros altos e comps na B3. Consulte SEMPRE que a modelagem envolver empresa, ativo ou fluxo de caixa em BRL. Triggers em "DCF", "valuation", "WACC", "LBO", "comps", "modelo", "fluxo de caixa descontado", "taxa de desconto", "risco-país", "custo de capital", "custo de equity", "terminal value", "perpetuidade", "câmbio", "USD/BRL", "IR/CSLL", "IRPJ", "JCP", "juros sobre capital próprio", "beta", "ERP", "debênture", "Selic", "NTN-B", "múltiplos", "EV/EBITDA".
---

# Modelagem Financeira e Valuation — Brasil

Esta é uma **camada de domínio** que se apoia na fundação `mercado-brasil` (tributação, regulatório, contábil, benchmarks). Consulte `mercado-brasil` primeiro para o arcabouço geral; use **este** documento para o que é específico de **modelagem e valuation**. As skills de modelagem importadas (`financial-analysis`/`model-builder`/`pitch-agent`: **dcf-model**, **lbo-model**, **comps-analysis**, **3-statement-model**) foram calibradas para os EUA — Treasury como risk-free, tax rate federal ~21%, mercado de dívida high-yield/leveraged loan americano, perpetuidade com inflação de ~2%. Quando o alvo for **Brasil**, sobrescreva essas premissas com o que segue.

## Regra mestre: consistência moeda × taxa × inflação

O erro nº 1 em valuation de emergente é **descontar fluxo em BRL por WACC calibrado em USD** (ou vice-versa). Antes de montar o modelo, fixe a **moeda do fluxo** e case tudo a ela:

| Fluxo projetado em | Deve ser descontado por | Risk-free base | Inflação embutida |
|---|---|---|---|
| **BRL nominal** | WACC nominal em BRL | Selic / LTN / NTN-F | IPCA de longo prazo |
| **BRL real** | WACC real em BRL | NTN-B (juro real, IPCA+) | zero (tudo em termos reais) |
| **USD nominal** | WACC em USD (CAPM US + risco-país) | Treasury | CPI dos EUA |

Regra derivada para o **terminal value**: `g` nominal em BRL tem de ser coerente com a inflação de longo prazo embutida (IPCA), não com os ~2% dos EUA. Fluxo real usa `g` real. Nunca misture.

## Mapa de substituições EUA → Brasil

| Premissa da skill (padrão EUA) | Substituir por (Brasil) |
|---|---|
| Risk-free = 10Y Treasury | **NTN-B** (real) ou **LTN/NTN-F / Selic** (nominal) — títulos públicos brasileiros |
| Tax rate ~21% federal | **~34%** no lucro real (IRPJ 15% + adicional 10% + CSLL 9%) |
| Custo de dívida = spread s/ Treasury / SOFR | Spread sobre **CDI/Selic**; **debêntures** como principal instrumento corporativo |
| Perpetuidade g ~2% (CPI US) | `g` coerente com **IPCA** de longo prazo |
| ERP dos EUA (~4,5–5,5%) | ERP local ou ERP US **+ prêmio de risco-país** (EMBI+/CDS) |
| SEC filings (10-K/10-Q) | **ITR/DFP + Formulário de Referência** (CVM/RI); demonstrações em CPC/IFRS |
| Sem escudo de JCP | Modelar **JCP** como alternativa a dividendos (escudo fiscal) |

---

## 1. Construção do WACC no Brasil

`WACC = Ke · E/(D+E) + Kd · (1−t) · D/(D+E)`, com **t ≈ 34%** (lucro real). Duas abordagens aceitas para o custo de equity `Ke` — escolha uma e seja **consistente** com a moeda do fluxo:

**Abordagem A — CAPM local (fluxo em BRL nominal).**
`Ke = rf_BR + β · ERP_BR`
- `rf_BR`: yield da **NTN-F/LTN** de prazo longo (nominal) ou Selic. Para fluxo **real**, use **NTN-B** e trabalhe tudo em termos reais.
- `β`: beta do setor; para poucos comparáveis locais, use beta desalavancado de peers globais e **realavanque** pela estrutura de capital e `t` locais.
- `ERP_BR`: prêmio de risco de mercado do Brasil (tipicamente maior que o dos EUA).

**Abordagem B — CAPM em USD + risco-país (Damodaran, mercados emergentes).**
`Ke_USD = rf_US + β · ERP_maduro + λ · CRP` e depois converte para BRL pelo **diferencial de inflação**:
`Ke_BRL = (1 + Ke_USD) · (1 + IPCA_esperado)/(1 + CPI_US_esperado) − 1`
- `CRP` (country risk premium): normalmente o **EMBI+ Brasil** ou o **CDS soberano** (spread sobre o Treasury), às vezes ajustado pela razão vol(equity)/vol(bond).
- `λ`: exposição da empresa ao risco-país (1,0 como default; menor para exportadora dolarizada).

Ambas devem convergir se calibradas de forma coerente. **Sinalize** qual foi usada e não troque de abordagem no meio do modelo.

### Custo da dívida (Kd)
- Empresa brasileira capta a **CDI + spread** (ou Selic + spread), com taxas nominais **bem mais altas** que nos EUA. Não use spread sobre Treasury.
- Mercado de dívida corporativa: predominância de **debêntures** (incl. incentivadas da Lei 12.431, isentas para PF — o que barateia o funding do emissor), CRIs/CRAs, notas comerciais. Menos profundo e mais curto que o mercado US.
- Escudo fiscal da dívida = `Kd · t`, com `t ≈ 34%` — mais valioso em BRL justamente pela alíquota alta.

### Câmbio (ativo dolarizado)
Para receitas/custos em USD dentro de empresa BRL, **projete USD/BRL explicitamente** e de forma coerente com o diferencial de juros/inflação (paridade): `USD/BRL_{t+1} = USD/BRL_t · (1+juro_BRL)/(1+juro_USD)` (ou via diferencial de inflação). Não congele o câmbio spot ao longo da projeção.

---

## 2. Impostos e JCP na modelagem

- **Alíquota efetiva ~34%** no **lucro real**: IRPJ 15% + adicional 10% (sobre lucro acima de R$ 20 mil/mês) + CSLL 9%. Use ~34% como default de `t` em WACC e no NOPAT — não 21%.
- **Lucro presumido**: base de cálculo é uma margem presumida da receita, não o lucro contábil — muda toda a modelagem de imposto (empresas menores/serviços). Confirme o regime antes de projetar a linha de imposto.
- **JCP (juros sobre capital próprio)** — peculiaridade brasileira: distribuição a acionistas **dedutível** da base de IRPJ/CSLL (limitada por TJLP × patrimônio líquido e por trava de lucro). Modelar JCP em vez de/além de dividendos **reduz o IR efetivo** da empresa e cria valor. Sofre retenção de IRRF na PF (15%). Em valuation, refletir o escudo de JCP no fluxo (menor imposto pago) ou como ajuste explícito.

---

## 3. DCF adaptado (skill dcf-model)

1. **Fixe a moeda** (§ regra mestre) e projete FCFF/FCFE coerente com ela.
2. **NOPAT** = EBIT · (1 − 0,34); adicione de volta D&A, subtraia capex e variação de capital de giro (working capital é sensível a inflação alta — projetar em % de receita nominal).
3. **Desconte** pelo WACC na **mesma moeda/inflação** do fluxo.
4. **Terminal value** — cautela redobrada em ambiente de juros/inflação altos:
   - Gordon: `TV = FCF_{n}·(1+g)/(WACC − g)`. Em BRL nominal, `g` deve refletir **IPCA de longo prazo** + crescimento real modesto, e ficar **bem abaixo** do WACC nominal (que é alto) — spread (WACC − g) pequeno infla demais o TV.
   - Alternativa: **múltiplo de saída** (EV/EBITDA) calibrado por comps da B3, muitas vezes mais defensável que perpetuidade quando a Selic está elevada.
   - Faça o TV **não** dominar 85%+ do EV; se dominar, revise premissas.
5. **Sensibilidade**: tabela WACC × g (e WACC × múltiplo de saída). Exemplo ilustrativo de faixas (confirmar com dados vigentes): WACC nominal BRL na casa de dois dígitos altos; `g` nominal na faixa da inflação-alvo + 1–2 p.p.

---

## 4. LBO adaptado (skill lbo-model)

O modelo padrão assume leveraged loan/high-yield dos EUA com dívida barata e abundante. No Brasil:
- **Alavancagem típica menor**: custo de dívida em **CDI+** e mercado de aquisição menos profundo reduzem o Debt/EBITDA sustentável frente aos deals US.
- **Financiamento** frequentemente via **debêntures** (às vezes com FIDC/CRA), não term loan B / bonds US. Amortização e covenants em BRL.
- **Retorno via financial leverage** é estruturalmente menor que nos EUA (a dívida "come" mais caixa); mais peso recai sobre **crescimento operacional e múltiplo de saída** para gerar IRR/MOIC.
- Imposto ~34% afeta o escudo da dívida (a favor) e o caixa livre para amortizar (contra). Modele DSCR com o custo de dívida real (CDI+spread).
- Sensibilidade de IRR/MOIC deve incluir cenário de **Selic/CDI** (custo de dívida), não só múltiplo de entrada/saída.

---

## 5. Comps na B3 (skill comps-analysis)

- **Universo**: peers listados na **B3, em BRL**. Não misture múltiplos de empresa US sem ajustar câmbio, risco-país e estrutura de capital.
- **Múltiplos**: **EV/EBITDA** e **P/L (P/E)** como padrão; **P/VPA (P/B)** para bancos e seguradoras; EV/Receita para crescimento pré-lucro. FIIs por P/VP e dividend yield.
- **Ajustes obrigatórios**:
  - **JCP**: normalizar payout/lucro — JCP vira despesa financeira na contabilidade mas é remuneração ao acionista; ajustar para comparar P/L de forma consistente.
  - **Normas contábeis**: CPC/IFRS (não US GAAP) — atenção a leasing (IFRS 16), impairment, reconhecimento de receita ao comparar EBITDA.
  - **Estrutura de capital** e liquidez: free-float baixo e liquidez menor pedem prêmio/desconto; desalavancar múltiplos quando comparar D/E diferentes.
  - **Impostos**: alíquota ~34% já embutida no lucro reportado — cuidado ao comparar com peers estrangeiros de alíquota menor.

---

## Nota importante
Este documento é uma referência de trabalho para orientar as skills de modelagem, **não é aconselhamento de investimento, jurídico ou tributário**. Parâmetros de mercado (Selic, CDI, IPCA esperado, EMBI+/CDS, ERP, câmbio USD/BRL) e regras tributárias mudam com frequência — as faixas citadas aqui são **ilustrativas** e devem ser substituídas pelos números vigentes na data da análise. Antes de entregar um valuation, **confirme os inputs correntes** (curva de juros, risco-país, alíquota e regime tributário do alvo, limites de JCP) e **sinalize a incerteza** de qualquer premissa em vez de afirmá-la como fato.
