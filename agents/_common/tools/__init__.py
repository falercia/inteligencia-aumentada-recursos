"""Tools educacionais seguras para rodar local, sem internet nem efeito externo.

Cada tool exporta duas coisas: o SCHEMA (formato da Anthropic) e a função
execute_*, que recebe o input e devolve string.

A tabela canônica para usar nos agentes:

    from agents._common.tools.calculator import CALCULATOR_TOOL, execute_calculator
    from agents._common.tools.file_reader import FILE_READER_TOOL, execute_file_reader
    from agents._common.tools.fake_web_search import WEB_SEARCH_TOOL, execute_web_search

    TOOLS = [CALCULATOR_TOOL, FILE_READER_TOOL, WEB_SEARCH_TOOL]
    TOOL_REGISTRY = {
        "calculator": execute_calculator,
        "file_reader": execute_file_reader,
        "fake_web_search": execute_web_search,
    }

    def execute(name, input):
        return TOOL_REGISTRY[name](input)
"""
