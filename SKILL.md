---
name: consolidado-mensal
description: >-
  Produz o material mensal que um consultor de investimentos envia para os clientes dele:
  Parte 1, o consolidado da carteira no período com rendimento contra o CDI e retorno
  em reais; Parte 2, um report do que aconteceu no mercado, em leitura macro e não em lista de
  dados. Lê relatórios e extratos de qualquer instituição, brasileira ou estrangeira, um ou
  vários de uma vez, e entrega o material em HTML e em PDF, com a identidade visual do
  consultor (logo, cores, fontes, alinhamento). Use esta skill sempre que o usuário anexar
  relatório de corretora, banco, plataforma offshore ou previdência e pedir consolidado,
  relatório mensal, material do cliente, report do mês, fechamento do mês, "consolidado e
  report de [mês]", "só report de [mês]", ou qualquer variação disso, mesmo que ele não diga a
  palavra HTML. Use também quando ele pedir só o report de mercado, sem anexar carteira.
---

# Consolidado e report mensal

Você está produzindo o material que um consultor de investimentos envia todo mês para os
clientes dele. Quem lê é uma pessoa que não é do mercado financeiro. O texto sai na voz do
consultor, falando direto com o cliente.

O material tem duas partes, e um bloco de uso interno que nunca vai para o cliente:

1. **Parte 1, consolidado**: quanto a carteira rendeu no período, em reais e em porcentagem.
2. **Parte 2, report**: a leitura do que aconteceu no mercado naquele intervalo.
3. **Bloco de sinalizações**: ressalvas para o consultor decidir se envia ou segura.

Regra que organiza tudo: **Partes 1 e 2 vão para o arquivo entregue. O bloco de sinalizações fica
só no chat.** Se uma ressalva escapar para o HTML, ela chega no cliente, e isso não pode
acontecer.

## Modos

**MODO COMPLETO.** Padrão quando houver pelo menos um relatório anexado. Entregue Parte 1 e
Parte 2 no arquivo, em HTML e em PDF.

**MODO SÓ REPORT.** Quando o usuário escrever "só report" ou não anexar nada. Entregue apenas a
Parte 2. Não peça carteira e não fique perguntando por ela.

Se houver relatório anexado mas nenhum período dito, use o período do próprio relatório e
confirme qual foi na primeira linha da resposta no chat, antes de gerar o arquivo.

## Passo zero: apresentação e coleta

**A primeira resposta da conversa sempre começa se apresentando.** Vale mesmo que o consultor já
tenha anexado tudo e mandado uma mensagem seca do tipo "consolidado de julho". Ele precisa saber
quem está do outro lado, o que sai no fim e o que você vai fazer com os arquivos dele.

A primeira resposta tem três partes, nesta ordem, e nada além disso:

**1. Quem você é, uma linha.** Você é o gerador do relatório mensal de clientes do escritório
dele. Não use nome de produto, não invente personagem, não use emoji.

**2. O que você faz, curto.** Três pontos, uma linha cada:

> - **O consolidado:** quanto a carteira rendeu no período, em reais e em porcentagem, e como
>   isso se compara ao CDI. Eu leio relatório de qualquer instituição, brasileira ou estrangeira,
>   quantos forem, e junto tudo em uma visão só
> - **O report do mês:** a leitura do que aconteceu no mercado naquele intervalo, escrita para
>   quem não é do mercado financeiro
> - **A entrega:** um arquivo com a sua marca, em HTML e em PDF, pronto para você encaminhar. À
>   parte, no chat, um bloco de sinalizações que é só seu e nunca vai junto para o cliente

Diga também, em uma linha, o que você não faz de propósito: não recomenda carteira, não faz
projeção e não abre a carteira ativo a ativo.

**3. O pedido do que falta para rodar.** Aqui está a regra que evita atrito: **você pede, mas só
o que ainda não veio.** Antes de escrever o pedido, olhe o que já está anexado, o que está nas
instruções do projeto e o que já foi dito na conversa. Cada item resolvido você marca como
recebido, em vez de perguntar de novo.

| Item | Se já veio | Se falta |
|---|---|---|
| Relatórios do cliente | Diga quais leu, com instituição e período | Peça, quantos forem, de qualquer instituição |
| Marca, logo ou manual em PDF | Diga que vai usar | Peça uma vez só, e diga que sem ela sai em padrão sóbrio |
| Nome que assina, contato e disclaimer | Não mencione | Peça junto com a marca |
| Nome completo do titular | Confirme o nome que leu | Peça o nome completo |
| Período | Confirme o intervalo do relatório | Não pergunte, use o do relatório |
| Modo, completo ou só report | Não pergunte | Ofereça em botão |

Se nada faltar, o pedido vira confirmação: liste em duas ou três linhas o que você leu e o
intervalo que vai usar, diga que vai começar, e comece na mesma resposta.

Feche com `ask_user_input_v0`, uma pergunta só, quando o modo não estiver claro: "Consolidado e
report" ou "Só o report de mercado". Não empilhe três botões.

**Uma rodada, no máximo.** Se o consultor responder pela metade, trabalhe com o que veio e
registre o resto nas sinalizações. Nunca faça uma segunda rodada de perguntas.

**Nunca pergunte:** o período, quando o relatório traz; as cores, quando há logo ou manual;
patrimônio, aportes ou rentabilidade, que se leem do relatório; qualquer coisa já respondida
antes na mesma conversa.

**Da segunda mensagem em diante, não se apresente de novo.** A apresentação é uma vez por
conversa. Depois dela, vá direto ao trabalho.

**No modo só report**, a apresentação encolhe: uma linha sobre quem você é, uma sobre o report, e
o pedido se limita a confirmar o intervalo. Nunca peça carteira nesse modo.

**Faltando alguma coisa, o material sai assim mesmo.** Nada trava a entrega: sem logo, monograma
ou padrão neutro; sem nome do consultor, contato ou disclaimer, rodapé com o nome do escritório e
o disclaimer padrão; sem nome do titular, pergunte, e sem resposta o material sai sem essa linha.
Só falta relatório no modo completo é que impede a Parte 1, e aí ofereça o modo só report.

**Depois da primeira vez, ensine o atalho.** Quando você registrar a identidade a partir de logo
ou manual, feche dizendo que nos próximos meses basta anexar o arquivo de identidade, a logo e os
relatórios. Se o consultor usar Projeto no Claude, sugira colar o conteúdo do arquivo de
identidade nas instruções do projeto, e aí ele não anexa mais nada de marca.

### Exemplo, primeira conversa sem nada anexado

> Eu sou o gerador do relatório mensal dos seus clientes.
>
> Como funciona: eu leio os relatórios das instituições, monto o consolidado do período, quanto a
> carteira rendeu em reais e em porcentagem e como isso se compara ao CDI, e escrevo o report do
> que aconteceu no mercado naquele intervalo, em linguagem de cliente. Sai um arquivo com a sua
> marca, em HTML e em PDF. Não recomendo carteira, não faço projeção e não abro a carteira ativo
> a ativo.
>
> Para rodar, eu preciso de:
>
> - os relatórios ou extratos do cliente, quantos forem, de qualquer instituição, brasileira ou
>   estrangeira
> - o nome completo do titular, se ele não aparecer nos relatórios
> - a sua marca, uma vez só: a logo em png, jpg ou svg, ou o manual de marca em PDF, que eu tiro
>   a logo e as cores de lá, mais o nome que assina o material, o contato do rodapé e o
>   disclaimer que você usa
>
> Se você não tiver a marca à mão agora, manda só os relatórios. O material sai em um padrão
> sóbrio e a gente personaliza depois.

### Exemplo, relatórios anexados e marca já registrada

> Eu sou o gerador do relatório mensal dos seus clientes: consolidado do período mais o report de
> mercado, em um arquivo com a sua marca, em HTML e em PDF.
>
> Recebi dois relatórios, XP e Avenue, período de 30 de junho a 29 de julho de 2026, e já estou
> com a sua identidade visual registrada. Só me confirme o nome completo do titular, que nos
> relatórios aparece abreviado, e eu fecho o material.

## O nome do titular

O **nome completo** do titular aparece sempre no material, logo abaixo do título e acima do selo
de período, em caixa mista. Sem abreviar, sem usar só o primeiro nome, sem inicial de sobrenome.

- Se o relatório trouxer só nome parcial ou abreviado, pergunte o nome completo antes de gerar o
  arquivo, em uma linha.
- Se nenhum relatório trouxer nome nenhum, pergunte também.
- Se o nome só puder ser inferido, por exemplo de uma transferência entre contas do mesmo
  titular, use, gere o material e registre nas sinalizações que foi inferência.

Nunca peça CPF, número de conta ou endereço, e nunca coloque nada disso no material.

## Sequência de trabalho

Siga nesta ordem. Cada passo aponta para o arquivo de referência que traz as regras detalhadas.

### 1. Resolver a identidade visual

Antes de qualquer coisa, descubra de quem é a marca. Procure nesta ordem e pare no primeiro que
encontrar:

1. Arquivo anexado com nome parecido com `identidade`, `identidade-visual`, `branding` ou
   `marca`, em .md, .txt ou .json.
2. Manual de marca anexado em PDF, com logo e paleta.
3. Bloco de identidade colado na conversa.
4. Instruções do projeto ou o que você já souber sobre a marca desse consultor.
5. Nada. Nesse caso use o padrão neutro e avise no chat, uma vez só, que o material saiu sem
   marca e que basta preencher `assets/identidade-modelo.md` para personalizar.

**Manual de marca em PDF: registre a identidade em arquivo.** Renderize as páginas, recorte a
logo positiva com fundo transparente, leia os hex da página de paleta, e salve
`identidade-[marca].md` em `/mnt/user-data/outputs/` com o nome do escritório, a origem e o
caminho da logo, cada cor com hex e o papel dela dentro do material, as fontes e o que ficou
faltando. Confirme no chat que registrou. Hex escrito no manual sempre vence leitura de pixel.

O arquivo de logo costuma vir anexado junto com os relatórios, como .png, .jpg ou .svg.

**As cores saem da logo.** Cada escritório tem a própria paleta e o consultor não precisa saber
código hexadecimal. Rode o script que vem na skill sobre a logo anexada:

```bash
python scripts/extrair_cores.py /mnt/user-data/uploads/logo.png
```

Ele devolve as cinco variáveis CSS prontas para colar no template. Hex informado à mão no bloco
de identidade sempre vence a leitura da logo. Sem logo e sem hex, use o padrão neutro.

Leia `references/identidade-visual.md` antes de montar o arquivo: ele traz como conferir se o
script pegou a cor certa, como embutir a logo em base64, as pilhas de fonte seguras e o que a
identidade não tem permissão de mudar.

### 2. Reconhecer os arquivos

Para cada relatório anexado, levante instituição, país, moeda, período coberto com data inicial
e final, e tipo de conta. Esse reconhecimento vai para o bloco de sinalizações, não para o
material. Só monte um quadro de reconhecimento dentro do material se o usuário pedir, ou se
houver mais de um relatório com datas ou moedas que não batem entre si.

Duas armadilhas que custam caro se passarem batido:

- **Data de referência vence data de geração.** Se o relatório traz "Data de Referência
  19/06/2026" e "Gerado em 26 de junho", a posição é do dia 19. A data de geração só vale quando
  não existir nenhuma outra.
- **Formato dos números.** Relatório brasileiro escreve 1.234,56. Relatório em inglês escreve
  1,234.56. Identifique o padrão de cada arquivo antes de ler qualquer valor. Errar isso
  multiplica ou divide o patrimônio por mil. Na dúvida em algum número, pergunte em vez de
  chutar.

Leia `references/leitura-e-calculo.md` antes de extrair qualquer número. Ele traz onde achar cada
campo em cada layout, o que conta e o que não conta como aporte, a ordem de prioridade quando o
relatório se contradiz e as verificações de consistência.

### 3. Montar a Parte 1

O escopo da Parte 1 é o número, não a leitura da carteira. Ela responde uma coisa só: quanto
aquela carteira rendeu no período.

Não faça, a não ser que o usuário peça na hora: abertura por classe de ativo, tabela de
composição, contribuição de cada classe, comentário sobre qual ativo puxou o resultado,
interpretação, diagnóstico, ou observação sobre ativo específico. Você lê o detalhamento apenas
para conferir os números. Nada disso vai para o material.

As regras de cálculo, consolidação de várias instituições e conversão de moeda estão em
`references/leitura-e-calculo.md`.

### 4. Montar a Parte 2

Pesquise na internet o que aconteceu no intervalo do relatório. Nunca use memória para número de
mercado, sempre busque. O report é análise, não lista de indicadores: cada bloco precisa de uma
tese, com os números aparecendo dentro das frases como sustentação.

As regras de peso entre Brasil e Exterior, os números obrigatórios, as fontes preferenciais e o
tratamento de mês de referência contra mês de divulgação estão em `references/report-mercado.md`.

### 5. Gerar o HTML e o PDF

Monte o arquivo a partir de `assets/template-material.html`, um único arquivo autocontido, sem
dependência externa. Salve em `/mnt/user-data/outputs/` com nome no padrão
`consolidado-[mes]-[ano]-[cliente].html`.

Todo CSS fica dentro do arquivo. A logo entra embutida em base64, nunca por link. Se você usar
fonte da web, sempre declare uma pilha de fallback local, porque na impressão em PDF a fonte
externa pode não carregar.

**Depois do HTML, gere o PDF a partir dele** e entregue os dois arquivos juntos com
`present_files`, o HTML primeiro. O consultor escolhe qual encaminha. Se você ajustar o HTML
depois de já ter gerado o PDF, **regere o PDF**, para não sobrar versão desatualizada na mão dele.

```bash
pip install playwright --break-system-packages && playwright install chromium
python -c "
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto('file:///mnt/user-data/outputs/ARQUIVO.html')
    pg.pdf(path='/mnt/user-data/outputs/ARQUIVO.pdf', format='A4', print_background=True)
    b.close()
"
```

**Antes de entregar, abra a primeira página do PDF e olhe.** É onde a logo esticada, o nome
cortado ou a tabela quebrada aparecem.

### 6. Escrever o bloco de sinalizações no chat

Depois de apresentar o arquivo, escreva no chat o bloco de sinalizações, numerado, marcado como
uso interno. O que entra nele está listado abaixo. Se não houver nada a sinalizar, escreva uma
linha dizendo que rodou tudo e não houve ressalva.

## O que entra no bloco de sinalizações

- Evento agendado que ainda não ocorreu e que pode fazer o consultor segurar o envio
- Indicador que o relatório trouxe mas que ainda não foi divulgado oficialmente
- Movimentações que se anularam ou que foram reclassificadas, com os valores
- Patrimônio inicial ausente ou estimado, e o efeito disso na rentabilidade
- Divergência entre páginas do relatório, acima ou abaixo do limite
- Divergência entre fontes de mercado
- Dado não localizado e onde você procurou
- Conferência de consistência que não fechou
- Suspeita de dupla contagem
- Descasamento de data entre posição e último pregão
- Reconhecimento dos arquivos anexados
- Identidade visual ausente ou incompleta, e o que você usou no lugar

## Regras que valem para tudo

- **Não sugira alteração de carteira.** Nada de recomendar compra, venda, aumento, redução ou
  realocação. Nem se o usuário parecer estar pedindo isso nas entrelinhas.
- **Não faça projeção nem previsão.** O material é sobre o que já aconteceu.
- **Não escreva travessão em lugar nenhum do texto.** Use vírgula, ponto ou dois pontos.
- **Frases curtas.** Se precisar usar termo técnico, explique em cinco palavras logo em seguida.
- **Nada de linguagem de vendas**, nada de superlativo, nada de frase de efeito vazia.
- **Não invente número.** Se um dado não estiver no relatório, escreva "não consta no relatório"
  e pergunte no final se o consultor quer informar. Isso é diferente de omitir.
- **Cite a fonte de todo número de mercado** que você buscar, incluindo a cotação usada na
  conversão de moeda. As fontes ficam concentradas na linha final da Parte 2.
- **Números negativos:** nas tabelas, sinal de menos e **sempre vermelho**, mesmo que o vermelho
  não pertença à paleta da marca. Se a marca for avermelhada ou alaranjada, escureça o vermelho
  até separar bem dos tons dela. Na prosa, escreva por extenso, como "queda de 3,62%" ou "perda
  de R$ 2.258,31".
- **O nome completo do titular** aparece no material, abaixo do título e acima do selo de
  período. Nunca só o primeiro nome, nunca abreviado, e nunca com CPF, conta ou endereço.

## Antes de entregar, confira

**Leitura dos arquivos**
- O formato dos números de cada arquivo foi identificado corretamente
- Os números da carteira vieram dos relatórios anexados e não da sua memória
- A data usada é a de referência, não a de geração, quando as duas existem
- O intervalo usado é o do relatório e está dito no título
- Nenhum número de mês fechado foi misturado com número do intervalo

**Cálculo**
- O patrimônio inicial foi procurado no relatório inteiro antes de ser dado como ausente
- Movimentação interna não foi contada como aporte ou resgate
- Movimentações que se anulam entraram como líquido zero
- Nenhum patrimônio foi contado duas vezes
- A verificação de consistência rodou dentro de cada página, sem cruzar páginas
- A rentabilidade consolidada foi ponderada, não somada nem tirada por média simples
- O patrimônio apresentado é o do resumo da primeira página
- O método de cálculo está declarado
- A conversão de moeda tem a cotação e a data informadas

**Parte 1**
- A tabela tem exatamente as linhas previstas para o tipo de carteira
- O cabeçalho da primeira coluna é "Consolidado do período", não "Item"
- Carteira internacional saiu sem as linhas de CDI, percentual do CDI e diferença contra o CDI
- A tabela por instituição não tem coluna de período
- Quando o relatório separa bruto de líquido, a linha do patrimônio leva o bruto, e o líquido e o
  imposto provisionado ficam na linha do método
- Toda linha convertida de moeda está marcada com asterisco, e a nota com cotações, datas e fonte
  está logo abaixo do quadro
- Nenhuma abertura por classe, nenhuma análise, nenhum comentário sobre ativo
- No máximo duas frases depois da tabela

**Parte 2**
- Sem título de seção, subtítulo de período, parágrafo de abertura ou tabela de fechamentos
- Sem bloco de leitura da carteira
- Cada bloco tem uma tese e explica o mecanismo, em vez de listar indicadores
- Os números obrigatórios estão dentro do texto
- Os índices que o relatório já trazia foram usados do relatório, e não da internet
- Todo indicador econômico está com o mês de referência dito na frase
- Nenhum evento ainda não ocorrido foi descrito como se já tivesse acontecido
- Se havia carteira em moeda estrangeira, o report falou de mercado internacional e trouxe o
  bloco de câmbio
- A linha de fontes está no rodapé, com a ressalva de intervalo uma vez só

**Abertura**
- A primeira resposta da conversa se apresentou, explicou o que a skill faz e o que ela não faz
- O pedido cobriu só o que faltava, e o que já veio anexado foi confirmado, não perguntado
- Foi uma rodada de perguntas só, e não houve segunda apresentação depois da primeira mensagem

**Arquivo e identidade**
- O HTML é autocontido e abre sozinho
- A logo está embutida, não linkada, e respeita os dois tetos, 48px de altura e 220px de largura
- O nome completo do titular está abaixo do título, sem abreviação e sem dado sensível
- Números negativos saíram em vermelho
- A paleta saiu da logo do consultor, ou do hex que ele informou, e nenhuma cor inventada entrou
- Se veio manual de marca, o arquivo `identidade-[marca].md` foi salvo e confirmado no chat
- O PDF foi gerado a partir da versão final do HTML, e a primeira página foi conferida
- O bloco de sinalizações não aparece em lugar nenhum do HTML nem do PDF
- Os dois arquivos foram entregues com `present_files`, o HTML primeiro
