# Consolidado e report mensal, como usar

Uma página. Leia uma vez e não precisa voltar aqui.

## O que isso faz

Você anexa os relatórios do seu cliente e recebe de volta o material que você envia para ele,
com a sua marca, em HTML e em PDF. O material tem duas partes:

1. **O consolidado.** Quanto a carteira rendeu no período, em reais e em porcentagem, e como isso
   se compara ao CDI.
2. **O report.** A leitura do que aconteceu no mercado naquele intervalo, escrita para quem não é
   do mercado financeiro.

Depois do arquivo, no chat, vem um **bloco de sinalizações**, que é só para você. Ele lista as
ressalvas que eu encontrei, como um dado que ainda não foi divulgado ou uma divergência entre
páginas do relatório. Esse bloco nunca entra no arquivo do cliente.

## O que você precisa mandar

**Uma vez só, a sua marca:**

- A sua logo, em png, jpg ou svg. Se você tiver o manual de marca em PDF, mande o manual. Eu tiro
  a logo e as cores de lá e te devolvo um arquivo de identidade pronto
- O nome que assina o material, o contato do rodapé e o disclaimer que você usa

**Todo mês, do cliente:**

- Os relatórios ou extratos, quantos forem, de qualquer instituição, brasileira ou estrangeira
- O nome completo do titular, só se ele não aparecer inteiro nos relatórios. Ele sai no material,
  abaixo do título. Nunca peço nem uso CPF, número de conta ou endereço

Não precisa saber código de cor, não precisa preencher planilha e não precisa padronizar nada
antes de mandar. Eu leio o layout de cada instituição do jeito que ele vem.

## Como chamar

Anexe os arquivos e escreva uma destas frases:

- **Consolidado e report de [mês]**, para o material completo
- **Só report de [mês]**, quando você quer apenas a leitura de mercado, sem carteira

Se você não disser o mês, eu uso o período do próprio relatório e confirmo com você na primeira
linha da resposta.

## O que sai

Dois arquivos com o mesmo conteúdo, o HTML e o PDF gerado a partir dele. O HTML funciona offline,
com a logo embutida, então pode encaminhar por e-mail sem quebrar. O PDF é para quem prefere
baixar direto.

## O que ela não faz, de propósito

- **Não recomenda carteira.** Nada de sugerir compra, venda, aumento, redução ou realocação
- **Não faz projeção.** O material é sobre o que já aconteceu, não sobre o que vem pela frente
- **Não abre a carteira ativo a ativo.** O consolidado responde quanto rendeu, não o que rendeu.
  Se você quiser abertura por classe em algum mês, peça na hora

## Dúvidas que aparecem sempre

**O relatório não fecha no último dia do mês.** Tudo bem. A data final do período é a data do
relatório. Se ele vai até o dia 26, o período é até o dia 26, e a busca de notícias e de números
do report cobre exatamente esse intervalo.

**Anexei duas corretoras com datas de corte diferentes.** Eu consolido mesmo assim. A linha do
total sai marcada como períodos diferentes e você recebe o aviso nas sinalizações.

**Tenho relatório em dólar.** O consolidado aparece nas duas moedas e ganha um quadro pequeno
separando o que foi rendimento do ativo e o que foi câmbio. A conversão usa a PTAX do Banco
Central, com a cotação e a data declaradas no material.

**Não tenho logo.** O material sai com um monograma das suas iniciais, ou em um padrão neutro e
sóbrio. Não fica com cara de rascunho.

**Um dado não apareceu em lugar nenhum.** Eu não estimo e não deixo em branco. Escrevo "não
consta no relatório" e registro nas sinalizações onde procurei.

## Para não anexar a marca todo mês

Depois da primeira vez, eu te devolvo um arquivo `identidade-[sua marca].md`. A partir daí, você
tem duas opções:

1. Anexar esse arquivo mais a logo junto com os relatórios, todo mês
2. Melhor: criar um **Projeto no Claude** e colar o conteúdo desse arquivo nas instruções do
   projeto. Aí você não anexa mais nada de marca, só os relatórios

Se você criar o projeto, cole também esta linha no fim das instruções, para eu abrir a conversa
já pedindo o que falta:

> Ao iniciar qualquer conversa neste projeto, use a skill consolidado-mensal e faça a abertura
> dela: diga em uma linha o que precisa ser anexado neste mês. Não repita o pedido de material de
> marca, que já está registrado acima.
