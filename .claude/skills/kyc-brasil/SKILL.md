---
name: kyc-brasil
description: Camada de domínio de KYC e PLD-FT (prevenção à lavagem de dinheiro e ao financiamento do terrorismo) para o Brasil, sobrepondo as premissas americanas das skills importadas do marketplace Claude for Financial Services — em especial `operations` (kyc-doc-parse, kyc-rules) e o agente `kyc-screener`, que assumem OFAC/SDN, PEP dos EUA e Bank Secrecy Act. Traduz o processo de onboarding, cadastro, identificação de beneficiário final, classificação de risco, monitoramento e comunicação para o arcabouço brasileiro (COAF, CVM 50, Lei 9.613). Consulte SEMPRE que o trabalho envolver KYC, PLD, PLDFT, COAF, lavagem de dinheiro, beneficiário final, UBO, PEP, cadastro de cliente, suitability, onboarding, screening de sanções, due diligence ou classificação de risco de cliente no Brasil. Triggers em "KYC", "PLD", "PLD-FT", "PLDFT", "COAF", "lavagem de dinheiro", "financiamento ao terrorismo", "beneficiário final", "UBO", "PEP", "pessoa exposta politicamente", "cadastro", "suitability", "onboarding", "sanções", "due diligence", "conheça seu cliente".
---

# KYC e PLD-FT — Brasil

Este é um **overlay de domínio**. Ele aprofunda o tema de KYC/PLD-FT sobre a fundação `mercado-brasil` (leia-a antes: ela traz o pano de fundo regulatório — CVM, Bacen, COAF, B3 — e o mapa institucional geral). Aqui o foco é o que é **específico de KYC/PLD-FT** e sobrescreve as premissas americanas das skills `operations`/`kyc` e do agente `kyc-screener`, que foram escritas para OFAC/SDN, PEP dos EUA e Bank Secrecy Act.

Regra mestre: quando uma skill de KYC pedir "OFAC screening", "SDN list", "FinCEN SAR" ou "PEP list", **não** rode a versão americana em cliente brasileiro. Faça as substituições da tabela abaixo e siga o processo brasileiro.

## Mapa de equivalência EUA → Brasil

| Conceito na skill importada (US) | Equivalente funcional no Brasil |
|---|---|
| **OFAC / SDN list** (sanções) | Listas do **Conselho de Segurança da ONU (CSNU)**; indisponibilidade imediata de ativos pela **Lei 13.810/2019**. OFAC só quando houver exposição a USD/EUA. |
| **FinCEN** (unidade de inteligência financeira) | **COAF** — Unidade de Inteligência Financeira, vinculado ao **Banco Central** desde a **Lei 13.974/2020**. |
| **Bank Secrecy Act (BSA)** | **Lei 9.613/1998** (lavagem) + **Resolução CVM 50/2021** (PLD-FT no mercado de capitais). |
| **PATRIOT Act / terrorism financing** | **Lei 13.260/2016** (financiamento ao terrorismo); ativos virtuais/cripto: **Lei 14.478/2022**. |
| **US PEP list** | **Definição de PEP do COAF/CVM** (não é lista importada — é enquadramento por critério; ver seção PEP). |
| **SAR (Suspicious Activity Report)** | **Comunicação ao COAF** (operação suspeita e operação em espécie acima de limites). |
| **CIP / customer identification** | **Cadastro** + **"conheça seu cliente" (KYC)** conforme CVM 50. |
| **Beneficial ownership (FinCEN BOI)** | **Beneficiário final (UBO)** — **IN RFB 2.119/2022** (declaração no CNPJ). |

---

## 1. Base legal (o que citar)

- **Lei 9.613/1998** — crime de lavagem de dinheiro; obrigações de identificação, registro e comunicação.
- **Lei 13.260/2016** — financiamento ao terrorismo.
- **Lei 14.478/2022** — prestadores de serviço de ativos virtuais (cripto) sujeitos a PLD-FT.
- **Lei 13.810/2019** — cumprimento de sanções da ONU e indisponibilidade **imediata** de ativos.
- **Lei 13.974/2020** — COAF vinculado ao Banco Central.
- **Resolução CVM 50/2021** — PLD-FT no mercado de capitais: cadastro e atualização, "conheça seu cliente", **abordagem baseada em risco (ABR)**, monitoramento de operações e comunicação ao COAF.
- **IN RFB 2.119/2022** — cadastro CNPJ e declaração de **beneficiário final**.
- **Resolução CVM 30/2021** — suitability (perfil do investidor).

> A CVM 50 é a norma central para instituições do mercado de capitais. Instituições reguladas pelo Bacen (bancos, corretoras de câmbio) seguem norma equivalente do Banco Central — se a jurisdição regulatória do cliente não estiver clara, sinalize e confirme qual regulador se aplica.

---

## 2. Cadastro — campos mínimos

### Pessoa Física (PF)
- **CPF** (identificador fiscal — equivale ao SSN/TIN, mas é o eixo do cadastro).
- **Documento de identidade** com foto: RG ou CNH.
- **Comprovante de residência** atualizado.
- **Informações de renda e patrimônio** (compatibilidade financeira).
- **Origem dos recursos** (source of funds/wealth).
- Enquadramento **PEP** (sim/não) e enquadramento de risco.

### Pessoa Jurídica (PJ)
- **CNPJ**.
- **Contrato/estatuto social** e alterações vigentes.
- **Quadro de sócios e administradores**, percorrido **até o beneficiário final (pessoa natural)**.
- **Procurações** e poderes de representação; identificação dos representantes/procuradores (com CPF).
- **Demonstrações financeiras** e informações de faturamento/patrimônio.
- Enquadramento de risco e verificação de PEP entre sócios/representantes/UBO.

O cadastro deve ser **atualizado periodicamente** (a periodicidade varia conforme o risco — mais frequente para alto risco). Cadastro desatualizado é falha de PLD-FT, não apenas de higiene de dados.

---

## 3. Beneficiário final (UBO)

Objetivo: chegar à **pessoa natural** que, em última instância, controla ou se beneficia da PJ — não parar no primeiro sócio pessoa jurídica.

- Percorrer o **quadro societário em cascata**: se sócio da PJ-cliente é outra PJ, abrir essa PJ, e assim por diante até a pessoa física.
- Referência: **IN RFB 2.119/2022** (declaração de beneficiário final no cadastro CNPJ). O limiar usual de participação para caracterizar beneficiário final é da ordem de **25%**, direto ou indireto, além de quem exerce controle por outros meios — **confirme o percentual e as exceções vigentes na IN**, pois há hipóteses de dispensa (ex.: companhias abertas, entes públicos).
- Estruturas **offshore, trust e fundos no exterior** exigem esforço reforçado para identificar o UBO e devem elevar a classificação de risco (ver seção 4).
- Impossibilidade de identificar o beneficiário final é, por si, um **gatilho de atenção** — avaliar recusa de relacionamento ou EDD intensiva.

---

## 4. Classificação de risco e gatilhos de EDD

A CVM 50 adota **abordagem baseada em risco (ABR)**: classificar cada cliente e calibrar a diligência ao risco.

| Nível | Perfil típico | Diligência |
|---|---|---|
| **Baixo** | PF residente, renda/patrimônio compatíveis, sem bandeiras | Cadastro padrão (CDD) |
| **Médio** | Complexidade moderada, exposição parcial a fatores de risco | CDD reforçado, monitoramento mais atento |
| **Alto** | PEP, não residente, offshore/trust, cash-intensive, ativos virtuais, sócio/UBO opaco | **Due diligence reforçada (EDD)** |

**Gatilhos de EDD (due diligence reforçada):**
- **PEP** (e familiares / estreitos colaboradores) — ver seção 5.
- **Não residentes** e clientes com forte exposição ao exterior.
- **Estruturas offshore, trusts, fundos exclusivos e cadeias societárias opacas.**
- Setores/atividades de maior risco (uso intensivo de espécie, ativos virtuais, doações).
- Incompatibilidade entre movimentação e renda/patrimônio declarados.

EDD implica, no mínimo: aprofundar **origem dos recursos e do patrimônio**, obter **aprovação de nível hierárquico superior** para iniciar/manter o relacionamento e **monitoramento intensificado**.

---

## 5. PEP — Pessoa Exposta Politicamente

**Não é a lista dos EUA.** No Brasil é um **enquadramento por critério**, conforme definição do COAF/CVM:

- Agentes públicos que desempenham ou desempenharam **cargos, empregos ou funções públicas relevantes** (no Brasil ou no exterior), e dirigentes de organizações internacionais.
- O enquadramento persiste por **5 anos** após a pessoa deixar o cargo relevante.
- Estende-se a **familiares** (parentesco próximo) e a **estreitos colaboradores**.

Consequências: cliente PEP é **alto risco por definição** → **EDD**, apuração reforçada de origem de recursos e **aprovação de nível hierárquico superior** antes de iniciar/manter o relacionamento, além de monitoramento contínuo.

---

## 6. Sanções e screening

- Rastrear contra as **listas do CSNU (ONU)**. Havendo correspondência, aplicar a **Lei 13.810/2019**: **indisponibilidade imediata** de ativos e comunicação às autoridades — sem espera por ordem judicial prévia.
- **OFAC/SDN**: consultar **apenas** quando houver exposição a USD, contrapartes/ativos nos EUA, ou exigência de correspondente bancário americano. Não é o rastreio primário para um cliente puramente doméstico.
- Fazer screening no **onboarding** e de forma **contínua** (relistagens acontecem); rastrear cliente, sócios, representantes e **UBO**.

---

## 7. Monitoramento e comunicação ao COAF

- **Monitorar operações** de forma contínua, buscando incompatibilidade com o perfil, fracionamento (structuring), atipicidade e sinais das situações de alerta da CVM 50.
- **Comunicar ao COAF**:
  - **Operações suspeitas** (independente de valor) — equivalente ao SAR.
  - **Operações em espécie acima dos limites** definidos na norma. **Confirme o valor-limite vigente** na regulação aplicável antes de afirmar um número — os limites são atualizados periodicamente.
  - **Comunicação negativa** anual quando não houver operações a reportar, quando exigida.
- A comunicação ao COAF é **sigilosa**: não informar o cliente ("no tipping-off").
- Manter **registros** de cadastro, operações e comunicações pelo prazo regulatório.

---

## 8. Suitability (adjacente ao KYC)

- **Resolução CVM 30/2021**: definir o **perfil do investidor** (conservador/moderado/agressivo, capacidade de assumir risco e horizonte) **antes de recomendar** produtos.
- Suitability responde "o produto é adequado?"; KYC/PLD-FT responde "quem é o cliente e o dinheiro é lícito?". São processos distintos que convivem no onboarding — não os confunda ao aplicar uma skill importada.

---

## 9. Checklist prático de onboarding

**PF**
- [ ] CPF coletado e validado
- [ ] Documento de identidade com foto (RG/CNH)
- [ ] Comprovante de residência atualizado
- [ ] Renda e patrimônio declarados e compatíveis
- [ ] Origem dos recursos apurada
- [ ] Verificação PEP (titular, familiares, colaboradores próximos)
- [ ] Screening de sanções (ONU; OFAC se exposição a USD)
- [ ] Classificação de risco atribuída (baixo/médio/alto)
- [ ] EDD + aprovação hierárquica superior, se alto risco/PEP
- [ ] Perfil de suitability (CVM 30) definido

**PJ**
- [ ] CNPJ e situação cadastral
- [ ] Contrato/estatuto social vigente
- [ ] Quadro societário percorrido até o **UBO (pessoa natural)**
- [ ] Beneficiário final identificado e documentado (IN RFB 2.119)
- [ ] Procurações e representantes identificados (com CPF)
- [ ] Demonstrações financeiras / faturamento
- [ ] Verificação PEP entre sócios, representantes e UBO
- [ ] Screening de sanções da PJ e das pessoas relevantes
- [ ] Classificação de risco (offshore/trust/opacidade → alto)
- [ ] EDD + aprovação hierárquica superior, se aplicável
- [ ] Rotina de atualização cadastral definida

---

## Nota importante
Este documento é uma referência de trabalho para orientar as skills, **não é aconselhamento jurídico ou de compliance**. A regulação brasileira de PLD-FT muda com frequência (resoluções e ofícios da CVM e do Bacen, atos do COAF, instruções da RFB, atualização de listas de sanções). Antes de aplicar uma regra a um caso real, **confirme a norma e os limites vigentes** — em especial o valor-limite de comunicação de operações em espécie, o percentual e as dispensas de beneficiário final da IN RFB 2.119, e qual regulador (CVM ou Bacen) rege o cliente. Na dúvida sobre um ponto específico, **sinalize a incerteza** em vez de afirmar.
