import pandas as pd

def get_code_values(code_id):
    df = pd.read_csv('language/codes_ptBR.tsv', sep='\t')
    return df[df.code_id == code_id].values.tolist()[0]

class CodeDescriptor:
    def __init__(self, code_id, code, examples, explanation, json_code, color):
        self.code_id = code_id
        self.code = code
        self.examples = examples
        self.explanation = explanation
        self.json_code = json_code
        self.color = color

class EntityCode:
    def __init__(self):
        code_ids = ["person", "source", "educational", "commercial", "gov", "city", "country", "police", "work", "movement", "text"]
        self.map = {}
        self.json_map = {}
        self.valid_search_filters = []
        self.code_map = {}
        for k in code_ids:
            code_id, code, examples, explanation, json_code, color = get_code_values(k)
            code_descriptor = CodeDescriptor(code_id, code, examples, explanation, json_code, color)
            self.map[code_id] = code_descriptor
            self.code_map[code] = code_descriptor
            self.json_map[json_code] = code_descriptor
            self.valid_search_filters.append(code)

entity_code = EntityCode()
