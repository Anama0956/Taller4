"""Punto 5. Inferencia mediante encadenamiento hacia adelante."""
from models.logic import match_premises, substitute


def forward_chain(kb):
    """Retorna una tupla con los hechos originales y derivados, sin duplicados.

    Cada ronda usa los hechos disponibles al comenzarla. La base de entrada
    debe conservarse.
    kb.facts contiene objetos Atom; kb.rules contiene objetos Rule con los
    atributos premises y conclusion. Los hechos se comparan directamente.

    Tips:
    - match_premises(regla.premises, hechos) genera (sustitución, hechos usados).
      Si no hay coincidencias, no genera resultados. La sustitución es un
      diccionario, por ejemplo {'?p': 'ana'}.
    - substitute(regla.conclusion, sustitución) retorna un nuevo objeto Atom
      con las variables reemplazadas por los valores de la sustitución.
    """
    # TODO: Add your code here
    facts = list(kb.facts)
    
    while True:
      available = tuple(facts)
      new = []
      
      for rule in kb.rules:
        for substitution, used_fact in match_premises(rule.premises, available):
          conclusion = substitute(rule.conclusion, substitution)
          if conclusion not in facts and conclusion not in new:
            new.append(conclusion)
          
      if not new:
        return tuple(facts)
      
      facts.extend(new)
          

    # FIN DEL BLOQUE DEL ESTUDIANTE
