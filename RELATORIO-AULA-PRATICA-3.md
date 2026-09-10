# Relatório — Aula Prática 3

## Identificação

- **Equipe:** _[nome da equipe]_
- **Integrantes:** _[nomes dos integrantes]_
- **Repositório Git:** https://github.com/iadigitall/tdd-project
- **Data:** _[dd/mm/aaaa]_

## Ambiente

- **Sistema operacional:** Windows (terminal Git Bash)
- **Editor/IDE:** _[VS Code — confirmar]_
- **Versão do Python:** _[rodar `python --version` e colar aqui]_
- **Versão do Django:** _[rodar `python -m django --version` e colar aqui]_
- **Navegador usado no Selenium:** _[Chrome / Firefox — confirmar]_

## Checkpoints

| Checkpoint | Teste executado | Resultado | Evidência | Commit |
|---|---|---|---|---|
| 1 - Isolamento dos testes funcionais | `python manage.py test functional_tests` | OK — passou | _[print do terminal]_ | _[hash]_ |
| 2 - Remoção de sleeps | `python manage.py test functional_tests` | OK — passou | _[print do terminal]_ | _[hash]_ |
| 3 - Múltiplos usuários | `python manage.py test functional_tests` | OK — passou | _[print do terminal]_ | _[hash]_ |
| 4 - URLs, views e templates | `python manage.py test lists` | OK — passou | _[print do terminal]_ | _[hash]_ |
| 5 - Modelo List e Item | `python manage.py test lists` | OK — passou | _[print do terminal]_ | _[hash]_ |
| 6 - URL única e add item | `python manage.py test lists` | OK — passou | _[print do terminal]_ | _[hash]_ |
| 7 - Template final | `python manage.py test` | OK — passou | _[print do terminal]_ | _[hash]_ |

> Dica: para o commit de cada checkpoint, rode `git log --oneline` e pegue o hash curto correspondente. Para a evidência, um print do terminal com a linha `OK` (ou `Ran N tests ... OK`) já resolve.

## Falhas Esperadas

| Falha | O que indicava | Como foi corrigida |
|---|---|---|
| `selenium.common.exceptions.WebDriverException` / `AssertionError: 'To-Do' not found in title` ao rodar o primeiro teste funcional | O teste funcional foi escrito **antes** da aplicação existir — não havia página nem servidor respondendo (ciclo TDD: começa no vermelho) | Criando o projeto/app Django, a view da home e o template `home.html`, fazendo o servidor responder e o título aparecer |
| `django.db.utils.OperationalError: no such table: lists_item` | O modelo `Item`/`List` foi definido no código, mas a migração ainda não tinha sido criada/aplicada — o banco de teste não tinha a tabela | Rodando `python manage.py makemigrations` e `python manage.py migrate` para gerar e aplicar a migração |

> Se durante o roteiro apareceram outras (ex.: `TemplateDoesNotExist: home.html`, `NoReverseMatch` por URL sem nome, ou o teste `assertIn` falhando porque o item não persistia), pode trocar por uma dessas — o importante é descrever pelo menos duas que você realmente viu.

## Pontos Técnicos Aprendidos

**O que é isolamento em testes funcionais?**
É garantir que cada teste rode contra um banco de dados de teste próprio e temporário, criado e destruído a cada execução. Assim os testes não dependem dos dados de desenvolvimento nem "sujam" o banco real, e o que um teste cria não vaza para o outro. No Django, isso vem de rodar os FTs sob `LiveServerTestCase`/`StaticLiveServerTestCase`, que sobem um servidor de teste isolado.

**Por que `sleep` pode gerar testes frágeis?**
`time.sleep()` espera um tempo fixo. Se a aplicação responder mais rápido, você desperdiça segundos à toa; se responder mais devagar (máquina lenta, CI carregado), o teste falha mesmo com a aplicação funcionando — vira um teste "flaky" (instável). Trocar por uma espera explícita (um `wait_for` que tenta de novo em loop até um timeout) faz o teste se adaptar ao tempo real de resposta.

**Qual a diferença entre teste funcional e teste de unidade nesta aula?**
O teste funcional (Selenium) exercita o sistema inteiro pela ótica do usuário: abre o navegador, digita, clica e verifica o resultado na tela — é ponta a ponta, "caixa preta", e mais lento. O teste de unidade valida uma peça pequena e isolada (uma view, um modelo, a resolução de uma URL) pela ótica do desenvolvedor — é rápido e aponta exatamente onde quebrou.

**Por que a aplicação precisou de uma classe `List`?**
Porque um `Item` sozinho não sabe a que lista pertence. A classe `List` dá identidade a cada lista de tarefas, permitindo agrupar itens (via chave estrangeira do `Item` para a `List`) e dar a cada lista uma URL própria. Sem ela, não dava para separar "a lista do usuário A" da "lista do usuário B".

**Como as URLs passaram a representar recursos?**
Saímos de uma única página genérica para URLs no estilo REST, em que cada endereço identifica um recurso específico — por exemplo `/lists/<id>/` aponta para uma lista concreta, e um `POST` nessa URL adiciona um item àquela lista. As URLs deixaram de ser "telas" e passaram a ser endereços das entidades do domínio.

## Conclusão da Equipe

Ao longo da atividade a equipe praticou o ciclo do TDD — escrever o teste primeiro (vermelho), fazer passar com o mínimo de código (verde) e então refatorar. Ficou claro na prática a diferença entre teste funcional (visão do usuário, ponta a ponta) e teste de unidade (visão do desenvolvedor, peça isolada), e como os dois se complementam. O ganho mais concreto foi o **controle de regressão**: com a suíte de testes rodando, qualquer mudança que quebrava um comportamento já existente era apontada na hora, o que deu segurança para evoluir o código (criar os modelos `List`/`Item`, dar URL única a cada lista) sem medo de derrubar o que já funcionava. Também aprendemos que detalhes como isolar o banco de teste e trocar `sleep` por espera explícita são o que separa uma suíte confiável de uma suíte instável.
