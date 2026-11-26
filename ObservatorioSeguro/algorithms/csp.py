"""Puntos 1–3. Retroceso, consistencia de arcos y heurísticas."""
from collections import deque
from models.csp import SearchTrace, copy_domains


def backtracking_search(csp, domains=None, select_variable=None,
                        order_values=None, trace=None):
    """Punto 1: retorna {tarea: franja} o None si no hay solución.

    Entradas: csp representa el problema; domains contiene los dominios vigentes,
    reducidos por AC-3 cuando corresponde.
    csp.variables contiene los identificadores de las tareas, en orden.
    domains es {tarea: [franjas enteras]}; assignment es {tarea: franja}.
    El bloque por completar define expand(assignment).

    Tips:
    - choose(csp, assignment, domains) retorna una tarea pendiente;
      ordered(csp, x, assignment, domains) retorna sus valores en orden.
    - consistent(x, valor, assignment) retorna si el candidato es compatible
      con la asignación parcial; es el comprobador suministrado para este bloque.
    - search(nueva_asignacion) es la llamada recursiva suministrada. Recibe
      una asignación independiente y retorna una solución completa o None.
    """
    trace = trace if trace is not None else SearchTrace(False)
    domains = copy_domains(csp.domains if domains is None else domains)
    choose = select_variable or (lambda p, a, d: next(x for x in p.variables if x not in a))
    ordering = order_values or (lambda p, x, a, d: list(d[x]))

    # Registra las decisiones y los cambios de la búsqueda.
    def snapshot(assignment):
        return {x: [assignment[x]] if x in assignment else list(domains[x])
                for x in csp.variables}

    def ordered(problem, variable, assignment, current_domains):
        values = ordering(problem, variable, assignment, current_domains)
        trace.record('select', f'Elegir {variable}. Orden de valores: {values}.',
                     assignment, snapshot(assignment) if trace.enabled else domains, variable)
        return values

    def consistent(variable, value, assignment):
        current = snapshot(assignment) if trace.enabled else domains
        trace.attempt(assignment, current, variable, value)
        valid = csp.consistent(variable, value, assignment)
        if valid and trace.enabled:
            child = {**assignment, variable: value}
            trace.record('assign', f'Asignar {variable} a la franja {value}.',
                         child, snapshot(child), variable, value)
        elif not valid:
            trace.record('reject', 'El valor entra en conflicto con una tarea asignada.',
                         assignment, current, variable, value)
        return valid

    def search(assignment):
        result = expand(assignment)
        if result is None and len(assignment) < len(csp.variables):
            trace.fail(assignment, snapshot(assignment) if trace.enabled else domains)
            if assignment and trace.enabled:
                variable = next(reversed(assignment))
                parent = {x: v for x, v in assignment.items() if x != variable}
                trace.restore(parent, snapshot(parent), variable)
        return result

    # TODO: Add your code here
    def expand(assignment):
        if len(assignment) == len(csp.variables):
            return assignment

        x = choose(csp, assignment, domains)

        for value in ordered(csp, x, assignment, domains):
            if consistent(x, value, assignment):
                child = {**assignment, x: value}
                result = search(child)
                if result is not None:
                    return result
        return None
    # # FIN DEL BLOQUE DEL ESTUDIANTE

    return search({})


def revise(csp, x, y, domains):
    """Punto 2: revisa X→Y modificando domains[x].

    Retorna True únicamente si cambia ese dominio; False en caso contrario.

    Tips:
    - x e y son identificadores de tareas; domains[x] y domains[y] son listas.
    - csp.compatible(x, valor_x, y, valor_y) comprueba las restricciones
      entre ese par de tareas, respetando la dirección de las precedencias.
    - Si elimina elementos mientras recorre una lista, itere sobre una copia.
    """
    
    cambio = False
    copia_x =list(domains[x])
    
    for valor_x in copia_x:
      if not any(csp.compatible(x, valor_x, y, valor_y) for valor_y in domains[y]):
        dx = domains[x]
        dx.remove(valor_x)
        cambio = True
    return cambio
    
    raise NotImplementedError
    # FIN DEL BLOQUE DEL ESTUDIANTE


def ac3(csp, domains):
    """Punto 2: reduce domains; retorna False si detecta un dominio vacío.

    Un retorno True indica consistencia de arcos, no garantiza una solución.

    Tips:
    - Cada arco es un par (x, y) de identificadores de tareas.
      csp.neighbors[x] contiene los vecinos de x.
    - revise(csp, x, y, domains) retorna si modificó domains[x].
    """
    # TODO: Add your code here
      
    cola = deque()
    for x in csp.variables:
      for y in csp.neighbors[x]:
        cola.append((x,y))
        
    while cola:
      x,y = cola.popleft()
      if revise(csp, x, y, domains):
        if not domains[x]:
          return False
        for z in csp.neighbors[x]:
          if z != y:
            cola.append((z,x))
    return True
      
    raise NotImplementedError
    # FIN DEL BLOQUE DEL ESTUDIANTE


def select_unassigned_variable(csp, assignment, domains):
    """...(deja el docstring como está)..."""
    # TODO: Add your code here
    pendientes = [x for x in csp.variables if x not in assignment]

    def valores_restantes(x):
        return sum(1 for v in domains[x] if csp.consistent(x, v, assignment))

    def vecinos_pendientes(x):
        return sum(1 for y in csp.neighbors[x] if y not in assignment)

    return min(pendientes, key=lambda x: (valores_restantes(x),
                                          -vecinos_pendientes(x),
                                          csp.variables.index(x)))
    # FIN DEL BLOQUE DEL ESTUDIANTE


def order_domain_values(csp, variable, assignment, domains):
    """...(deja el docstring como está)..."""
    # TODO: Add your code here
    candidatos = [v for v in domains[variable]
                  if csp.consistent(variable, v, assignment)]
    vecinos = [y for y in csp.neighbors[variable] if y not in assignment]
    compatibles = {y: [w for w in domains[y] if csp.consistent(y, w, assignment)]
                   for y in vecinos}

    def descartados(v):
        return sum(1 for y in vecinos for w in compatibles[y]
                   if not csp.compatible(variable, v, y, w))

    return sorted(candidatos, key=descartados)
    # FIN DEL BLOQUE DEL ESTUDIANTE
