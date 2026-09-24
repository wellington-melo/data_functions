# ----------------------------------------------------------------------- #
#   BIBLIOTECAS
# ----------------------------------------------------------------------- #

import re
import unicodedata


# ----------------------------------------------------------------------- #
#   FUNCOES
# ----------------------------------------------------------------------- #

class DataTransformer:
    
    """
    Classe responsável por centralizar funções e métodos de normalização e tratamento de dados textuais e cadastrais.
    
    """
    
    @staticmethod
    def clean_text(text: str) -> str:
        
        """
        Realiza a limpeza completa de um texto:
        1. Converte para string (se necessário) e aplica TRIM (remove espaços nas pontas)
        2. Converte para UPPERCASE
        3. Remove acentos (normalização NFKD)
        4. Remove caracteres especiais (mantendo apenas letras, números e espaços)
        
        Obs: Como essa função unificada remove todos os caracteres especiais (como pontos, arrobas, hifens, etc.), evitar usá-la 
        em campos como E-mails, CPFs/CNPJs ou URLs.
        
        """
        if not isinstance(text, str):
            if text is None:
                return ""
            text = str(text)
        
        # Remove espaços nas pontas e joga para maiúsculo
        text = text.strip().upper()
        
        # Normaliza e remove acentos
        nfkd_form = unicodedata.normalize('NFKD', text)
        text_without_accents = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
        
        # Remove caracteres especiais (mantém apenas alfanuméricos e espaços)
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text_without_accents)
        
        return cleaned_text
    
    # ----------------------------------------------------------------------

    @staticmethod
    def normalize_cep(cep: str) -> str:
        
        """
        Normaliza e formata um valor de CEP para o padrão brasileiro oficial (xx.xxx-xxx).

        Esta função realiza a limpeza e padronização de códigos postais (CEP), garantindo que entradas com pontuações 
        extras, em formato numérico ou mal formatadas sigam rigorosamente a máscara padrão de endereçamento.

        Fluxo de Execução:
            1. Verifica o tipo do dado de entrada e converte para string de forma segura (tratando valores nulos/None).
            2. Remove todos os caracteres não numéricos através de expressão regular (\D).
            3. Se o CEP possuir 7 dígitos (perda do zero à esquerda comum em sistemas legados), preenche com '0' à esquerda.
            4. Valida se a quantidade de dígitos resultante é exatamente 8. Caso contrário, retorna o original.
            5. Aplica a formatação estrutural dividindo os dígitos nos blocos correspondentes (2, 3 e 3).

        Exemplo de Uso:
            >>> DataTransformer.normalize_cep("01001000")
            '01.001-000'
            >>> DataTransformer.normalize_cep("1001-000")
            '01.001-000'
            
        """
        if not isinstance(cep, str):
            cep = str(cep) if cep is not None else ""
        
        # Extrai apenas os dígitos numéricos da string
        digits = re.sub(r'\D', '', cep)
        
        # Se tiver 7 dígitos, corrige o zero à esquerda ausente
        if len(digits) == 7:
            digits = digits.zfill(8)
        
        # Valida se o CEP possui exatamente a quantidade correta de dígitos (8 dígitos)
        if len(digits) != 8:
            return cep  # Retorna original se inválido para evitar quebra silenciosa
        
        # Retorna formatado no padrão xx.xxx-xxx
        return f"{digits[:2]}.{digits[2:5]}-{digits[5:]}"
    
    # ----------------------------------------------------------------------

    @staticmethod
    def normalize_cpf_cnpj(documento: str) -> str:
        
        """
        Identifica e formata um documento numérico para o padrão de CPF (xxx.xxx.xxx-xx) 
        ou CNPJ (xx.xxx.xxx/xxxx-xx) com base na quantidade de dígitos válidos.
        
        Retorna o valor original caso o tamanho dos dígitos não corresponda a 11 ou 14.
        
        """
        if not isinstance(documento, str):
            documento = str(documento) if documento is not None else ""
            
        digits = re.sub(r'\D', '', documento)
        
        if len(digits) == 11:  # CPF
            return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
        
        elif len(digits) == 14:  # CNPJ
            return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
        
        return documento
    
    # ----------------------------------------------------------------------

    @staticmethod
    def normalize_telefone(telefone: str) -> str:
        
        """
        Trata telefones formatando para o padrão com DDD ((XX) XXXXX-XXXX / (XX) XXXX-XXXX) 
        ou sem DDD (XXXXX-XXXX / XXXX-XXXX) dependendo da quantidade de dígitos numéricos extraídos.
        
        Retorna o valor original caso a quantidade de dígitos seja diferente de 8, 9, 10 ou 11.
        
        """
        if not isinstance(telefone, str):
            telefone = str(telefone) if telefone is not None else ""
            
        digits = re.sub(r'\D', '', telefone)
        
        if len(digits) == 11:  # Celular com DDD
            return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
        
        elif len(digits) == 10:  # Fixo com DDD
            return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        
        elif len(digits) == 9:  # Apenas celular
            return f"{digits[:5]}-{digits[5:]}"
        
        elif len(digits) == 8:  # Apenas fixo
            return f"{digits[:4]}-{digits[4:]}"
            
        return telefone