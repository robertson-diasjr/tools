# Finance Tools
Geralmente obter informações consolidadas para análises financeiras nem sempre é uma tarefa fácil e só percebemos isso quando precisamos.

Dias desses me peguei nessa situação e visando facilitar a vida de muitos como Eu (profissionais de outras áreas que não financeira), compartilho esses códigos escritos em Python que tem por objetivo extrair em planilhas informações de FII - Fundos de Investimentos Imobiliários a partir das 2 principais plataformas no Brasil: Clube FII e FundsExplorer.

## Pré-Requisitos
1. Pyhton e bibliotecas instaladas
- `pip install pandas`
- `pip install requests`
- `pip install selenium`
- `pip install openpyxl`
- `pip install html5lib`
- 1`pip install <qualquer biblioteca que por ventura venha a faltar quando você rodar :-)>`

## Idéias
- Uma vez os dados estando no Pandas, você pode "brincar" com qualquer tipo de análise (sum, mean, etc) e extrair dados para sua análise
- Outra opção (no meu caso), vou transferir esses dados numa base SQLite e montar queries SQL (por estar mais familiarizado nesse momento) e extrair dados para análise
- Qualquer outra que te atenda :-)

Enjoy ;-)

## License
- GNU Public License
