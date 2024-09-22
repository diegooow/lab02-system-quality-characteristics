# Relatório Final

## Introdução

Este relatório apresenta uma análise das principais características de qualidade dos repositórios open-source mais populares escritos em Java no GitHub. As questões de pesquisa abordam a relação entre a popularidade, maturidade, atividade e tamanho dos repositórios e suas características de qualidade interna, medidas através da ferramenta CK.

## Hipóteses iniciais 

#### RQ 01. Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
  _Repositórios mais populares possuem melhores características de qualidade._

#### RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade?    
  _Repositórios mais maduros possuem melhores características de qualidade._

#### RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
  _Repositórios mais ativos possuem melhores características de qualidade._

#### RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?
  _Repositórios maiores possuem melhores características de qualidade._

## Metodologia

Para responder às questões de pesquisa, coletamos dados dos 1.000 repositórios Java com maior número de estrelas no GitHub utilizando as APIs GraphQL do GitHub. Em seguida, utilizamos a ferramenta de análise estática de código CK para calcular as métricas de qualidade.

#### As métricas de processo incluem:
Popularidade: número de estrelas
Tamanho: linhas de código (LOC) e linhas de comentários
Atividade: número de releases
Maturidade: idade (em anos) de cada repositório coletado

#### As métricas de qualidade incluem:
CBO: Coupling between objects
DIT: Depth Inheritance Tree
LCOM: Lack of Cohesion of Methods

Os dados coletados foram armazenados em um arquivo CSV para análise.

## Resultados Obtidos

#### RQ 01. Qual a relação entre a popularidade dos repositórios e as suas características de qualidade?
Correlação entre número de estrelas e quality_score: -0.12 (p-valor: 0.0003)

A correlação negativa sugere que repositórios mais populares tendem a ter uma pontuação de qualidade menor. Isso pode ser contra-intuitivo, mas pode ser explicado pelo fato de que repositórios mais populares podem atrair contribuições de uma gama mais ampla de desenvolvedores, o que pode levar a uma menor consistência na qualidade do código.

![image](https://github.com/user-attachments/assets/8179c443-a5e3-4459-be11-ed31bd19015c)


#### RQ 02. Qual a relação entre a maturidade do repositórios e as suas características de qualidade?
Correlação entre idade(em anos) e quality_score: 0.07 (p-valor: 0.0232)

A correlação positiva sugere que repositórios mais antigos tendem a ter uma pontuação de qualidade ligeiramente maior. Isso pode ser devido ao fato de que repositórios mais antigos tiveram mais tempo para refinar e melhorar seu código.

![image](https://github.com/user-attachments/assets/36311e37-cf38-4867-83ae-9218b979713b)


#### RQ 03. Qual a relação entre a atividade dos repositórios e as suas características de qualidade?
Correlação entre releases e quality_score: 0.26 (p-valor: 0.0000)

A correlação positiva sugere que repositórios com mais releases tendem a ter uma pontuação de qualidade maior. Isso pode ser explicado pelo fato de que repositórios com mais releases provavelmente passaram por mais iterações de desenvolvimento e, portanto, tiveram mais oportunidades para melhorar a qualidade do código.

![image](https://github.com/user-attachments/assets/3e151235-ca02-41ce-a0fa-81a2ae73af08)


#### RQ 04. Qual a relação entre o tamanho dos repositórios e as suas características de qualidade?
Correlação entre LOC(linhas de código) e quality_score: 0.32 (p-valor: 0.0000)

A correlação positiva sugere que repositórios maiores tendem a ter uma pontuação de qualidade maior. Isso pode ser devido ao fato de que repositórios maiores podem ter mais complexidade e, portanto, exigir um nível mais alto de qualidade para manter o código gerenciável.

![image](https://github.com/user-attachments/assets/3cc1560a-10f0-41e3-be77-d73236cc69fe)


## Conclusão

Os resultados obtidos nesta análise fornecem insights significativos sobre as características de qualidade dos repositórios open-source mais populares escritos em Java no GitHub. Os dados sugerem que a popularidade, maturidade, atividade e tamanho dos repositórios estão todos relacionados à qualidade do código de maneiras interessantes e às vezes inesperadas.

A hipótese inicial de que repositórios mais populares possuem melhores características de qualidade foi contrariada pelos dados. Observou-se uma correlação negativa entre a popularidade (medida pelo número de estrelas) e a pontuação de qualidade. Isso sugere que projetos com maior visibilidade podem atrair uma gama diversificada de contribuições, resultando em inconsistências na qualidade do código. Portanto, é crucial implementar estratégias eficazes de revisão de código e controle de qualidade em projetos de grande visibilidade para manter a qualidade do código.

Em contraste, os repositórios mais antigos, mais ativos e maiores mostraram uma tendência de terem melhores características de qualidade. Isso indica que o tempo, o nível de atividade e a complexidade do projeto podem contribuir positivamente para a qualidade do código. Repositórios mais antigos e ativos provavelmente passaram por várias iterações de desenvolvimento e refinamento, levando a um código de melhor qualidade. Da mesma forma, projetos maiores, apesar de sua complexidade, podem adotar práticas rigorosas de controle de qualidade para garantir a manutenção do código

No entanto, é importante ressaltar que esses resultados são correlações e não implicam necessariamente causalidade. Além disso, a qualidade do código é complexa e pode ser influenciada por uma variedade de fatores não considerados nesta análise.
