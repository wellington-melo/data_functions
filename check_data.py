# ----------------------------------------------------------------------- #
#   BIBLIOTECAS
# ----------------------------------------------------------------------- #

import re


# ----------------------------------------------------------------------- #
#   FUNCOES
# ----------------------------------------------------------------------- #

class DataValidator:
    
    """
    Classe responsável por validar a integridade de dados (ex: CPF, CNPJ, CHASSI, UF, CEP)
    retornando True caso for uma variável correta dentro dos padrões passados ou False caso não.
    
    """

    @staticmethod
    def validate_cep(cep: str) -> bool:
        
        """
        Valida se o CEP possui o formato correto de 8 dígitos.
        
        """
        if not cep:
            return False
        digits = re.sub(r'\D', '', str(cep))
        return len(digits) == 8
    
    # ----------------------------------------------------------------------

    @staticmethod
    def validate_cpf(cpf: str) -> bool:
        
        """
        Valida um CPF verificando seus dois dígitos verificadores.

        O CPF possui 11 dígitos, sendo:
        - 9 dígitos que compõem o número base;
        - 2 dígitos verificadores, calculados a partir dos anteriores.

        A validação abaixo verifica se esses dois dígitos verificadores correspondem aos cálculos definidos para o CPF.

        Observação:
            Esta função verifica apenas se o CPF é matematicamente válido.
            Ela não confirma se o CPF existe ou está regular na Receita Federal.
            
        """
        
        if not cpf:
            return False
        digits = re.sub(r'\D', '', str(cpf))
        
        if len(digits) != 11 or digits == digits[0] * 11:
            return False
            
        # Cálculo do primeiro dígito verificador
        soma = sum(int(digits[i]) * (10 - i) for i in range(9))
        digito1 = (soma * 10) % 11
        if digito1 == 10:
            digito1 = 0
        if digito1 != int(digits[9]):
            return False
            
        # Cálculo do segundo dígito verificador
        soma = sum(int(digits[i]) * (11 - i) for i in range(10))
        digito2 = (soma * 10) % 11
        if digito2 == 10:
            digito2 = 0
        if digito2 != int(digits[10]):
            return False
            
        return True

    # ----------------------------------------------------------------------

    @staticmethod
    def validate_cnpj(cnpj: str) -> bool:
        
        """
        Valida um CNPJ verificando seus dois dígitos verificadores.

        O CNPJ possui 14 dígitos, sendo:
        - 12 dígitos que compõem o número base;
        - 2 dígitos verificadores, calculados a partir dos anteriores.

        A validação abaixo verifica se esses dois dígitos verificadores
        correspondem aos cálculos definidos para o CNPJ.

        Observação:
            Esta função verifica apenas se o CNPJ é matematicamente válido.
            Ela não confirma se o CNPJ existe ou está regular na Receita Federal.
            
        """
        
        if not cnpj:
            return False
        digits = re.sub(r'\D', '', str(cnpj))
        
        if len(digits) != 14 or digits == digits[0] * 14:
            return False

        # Validação CNPJ (pesos padrão)
        def calcula_digito(digs, pesos):
            soma = sum(int(d) * p for d, p in zip(digs, pesos))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto

        pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        pesos2 = [6] + pesos1

        d1 = calcula_digito(digits[:12], pesos1)
        d2 = calcula_digito(digits[:12] + str(d1), pesos2)

        return digits[-2:] == f"{d1}{d2}"
    
    # ----------------------------------------------------------------------

    @staticmethod
    def validate_chassi(chassi: str) -> bool:
        
        """
        Valida se o Chassi possui a estrutura padrão internacional (17 caracteres).
        Além disso, valida se o 10º caractere (responsável pelo ano-modelo) 
        pertence ao conjunto de caracteres oficiais permitidos (A-Z exceto I,O,Q,U e 1-9).
        
        """
        if not chassi:
            return False
            
        chassi = str(chassi).strip().upper()
        
        # 17 caracteres no total. 
        # O 10º caractere [9] restringe estritamente aos símbolos válidos de ano-modelo.
        # Caracteres válidos para o 10º dígito: A-H, J-N, P, R, S, T, V, W, X, Y, 1-9
        pattern = r"^[A-HJ-NPR-Z0-9]{9}[A-HJ-NPR-Z1-9][A-HJ-NPR-Z0-9]{7}$"
        
        return bool(re.match(pattern, chassi))
    
    # ----------------------------------------------------------------------

    @staticmethod
    def validate_uf(uf: str) -> bool:
        
        """
        Valida se a UF informada é uma sigla de estado brasileiro válida.
        
        """
        if not uf:
            return False
        
        ufs_validas = {
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA",
            "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        }
        return str(uf).strip().upper() in ufs_validas