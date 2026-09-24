# Data Functions

Biblioteca em Python orientada a objetos (POO) focada em Qualidade de Dados, projetada para sanitizar, normalizar e validar dados presentes em tabelas para tratamento efetivo e consistência de informação.

## Estrutura do Projeto

- `normalize_data.py`: Módulo contendo a classe `DataTransformer`, voltada para a higienização, aplicação de máscaras e padronização de campos.
- `check_data.py`: Módulo contendo a classe `DataValidator`, voltada para a verificação de integridade estrutural e regras de negócio, retornando valores booleanos (`True`/`False`).

## Descrição dos Módulos

### 1. Normalização (`normalize_data.py`)
- **`clean_text`**: Padroniza textos aplicando conversão para maiúsculas, remoção de espaços nas extremidades, eliminação de acentos e exclusão de caracteres especiais básicos.
- **`normalize_cep`**: Formata códigos postais para o padrão `XX.XXX-XXX`, incluindo o preenchimento automático de zeros à esquerda para entradas com 7 dígitos.
- **`normalize_cpf_cnpj`**: Identifica automaticamente a estrutura do documento e aplica a formatação correta para CPF ou CNPJ.
- **`normalize_phone`**: Ajusta números telefônicos para os padrões com ou sem DDD, contemplando linhas fixas e celulares.

### 2. Validação (`check_data.py`)
- **`validate_cep`**: Confere se a estrutura numérica do CEP possui exatamente 8 dígitos.
- **`validate_cpf`**: Executa o algoritmo matemático oficial de validação dos dígitos verificadores do CPF.
- **`validate_cnpj`**: Executa o algoritmo matemático oficial de validação dos dígitos verificadores do CNPJ.
- **`validate_chassi`**: Valida o padrão internacional de 17 caracteres alfanuméricos, incluindo a checagem restritiva do 10º dígito (ano-modelo) e a exclusão de caracteres inválidos.
- **`validate_uf`**: Verifica se a sigla informada corresponde a uma Unidade Federativa brasileira válida.

## Exemplo de Utilização

```python
from normalize_data import DataTransformer
from check_data import DataValidator

# Exemplo de tratamento e normalização
cep_formatado = DataTransformer.normalize_cep("1001000")  # Retorna: '01.001-000'
texto_tratado = DataTransformer.clean_text("  exemplo de dado  ")  # Retorna: 'EXEMPLO DE DADO'

# Exemplo de validação de qualidade
cpf_valido = DataValidator.validate_cpf("12345678901")  # Retorna: True ou False
uf_valida = DataValidator.validate_uf("ES")  # Retorna: True
