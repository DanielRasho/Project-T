def porcentajes_de_valores(lista: list):
    suma_valores = sum(lista);
    porcentajes = list(map(lambda x: (x/suma_valores) * 100, lista));
    
    return porcentajes;

def obtener_explode(lista: list):
    valores_len =len(lista);
    max_index = lista.index(max(lista));
    explode = tuple([0.1 if i == max_index else 0 for i in range(valores_len)]);
    
    return explode;

def agregar_label_lista(lista: list, label: str):
    lista = list(map(lambda item: '{} {}'.format(str(item), label), lista)); 

    return lista;