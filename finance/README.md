# Finance Tools
Geralmente obter informações consolidadas para análises financeiras nem sempre é uma tarefa fácil e só percebemos isso quando precisamos.

Dias desses me peguei nessa situação ao avaliar Fundos de Investimentos Imobiliários (FIIs) e visando facilitar a vida de muitos como Eu (profissionais de outras áreas que não financeira), criei e compartilho esses códigos escritos em Python que tem por objetivo extrair em planilhas as principais informações dos FII - Fundos de Investimentos Imobiliários a partir das 2 principais plataformas no Brasil: Clube FII e FundsExplorer.

## Pré-Requisitos
1. Pyhton e bibliotecas instaladas
- `pip install pandas`
- `pip install requests`
- `pip install selenium`
- `pip install openpyxl`
- `pip install html5lib`
- `pip install <qualquer biblioteca que por ventura venha a faltar quando você rodar :-)>`

2. **Selenium**: aqui você precisará fazer download do driver em https://chromedriver.storage.googleapis.com/index.html?path=114.0.5735.90/, extraí-lo e ajustar o respectivo diretório dentro do código
   - Caso não queira mexer no código, crie o diretório "C:\terraform" e coloque o driver dentro.
   - No código, o diretório é referenciado da seguinte forma: 'C:\terraform\chromedriver.exe'

## Idéias
- Uma vez os dados estando no Python Pandas, você pode "brincar" com qualquer tipo de análise (sum, mean, etc) e extrair dados para sua análise
- Na planilha Excel, você pode criar uma nova coluna e: (dividir o valor do dividendo mensal esperado) pelo (valor do dividendo médio) e multiplicar (*) pelo preço atual da quota (ação). Com isso obterá o montante necessário a ser investido naquele FII para obter a renda mensal desejada.
- Outra opção (no meu caso), vou transferir esses dados numa base SQLite e montar queries SQL (por estar mais familiarizado nesse momento) e extrair dados para análise
- Qualquer outra que te atenda :-)

Enjoy ;-)

## License
- GNU Public License
