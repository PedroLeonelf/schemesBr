class Modelo:

    def __init__(self):
            self.listaEntidades = []
            self.listaRelacionamentos = []

    def adicionaEntidade(self, entidade):
        self.listaEntidades.append(entidade)
    
    def getEntidades(self):
        return self.listaEntidades
    
    def getEntidadePorNome(self, nome):
        for entidade in self.listaEntidades:
            if entidade.getNome() == nome:
                return entidade
    
    def adicionaRelacionamento(self, relacionamento):
        self.listaRelacionamentos.append(relacionamento)
    
    def getRelacionamentos(self):
        return self.listaRelacionamentos
    
    def getNomes(self):
        print("\nEntities:",end='')
        for entidade in self.listaEntidades:
             print(entidade.getNome(), end=', ')if not entidade == self.listaEntidades[-1] else print(entidade.getNome())
        print("Relations:",end='')
        for relacionamento in self.listaRelacionamentos:
            print(relacionamento.getNome(), end=', ') if not relacionamento == self.listaRelacionamentos[-1] else print(relacionamento.getNome())
