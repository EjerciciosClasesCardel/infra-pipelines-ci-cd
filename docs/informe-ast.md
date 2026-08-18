# Ejemplo de AST en expresiones

La gramática considerada es:

```bnf
<lc-exp> ::= <identifier>
           var-exp(id)
         ::= "lambda" "(" <identifier> ")" <lc-exp>
            lambda-exp(id, exp)
          ::= "(" <lc-exp> <lc-exp> ")"
            app-exp(rator, rand)
```

---

## Ejemplo 1: `x`

```mermaid
graph TD
  A[var-exp]
  A --> B[id: x]
```

---

## Ejemplo 2: `(lambda (x) x)`

```mermaid
graph TD
  A[lambda-exp]
  A --> B[id: x]
  A --> C[var-exp]
  C --> D[id: x]
```

---

## Ejemplo 3: `((lambda (x) x) y)`

```mermaid
graph TD
  A[app-exp]
  A --> B[lambda-exp]
  B --> C[id: x]
  B --> D[var-exp]
  D --> E[id: x]
  A --> F[var-exp]
  F --> G[id: y]
```

---

## Ejemplo 4: `(lambda (x) (lambda (y) x))`

```mermaid
graph TD
  A[lambda-exp]
  A --> B[id: x]
  A --> C[lambda-exp]
  C --> D[id: y]
  C --> E[var-exp]
  E --> F[id: x]
```

---

## Ejemplo 5: `((lambda (x) (x x)) (lambda (y) y))`

```mermaid
graph TD
  A[app-exp]

  A --> B[lambda-exp]
  B --> C[id: x]
  B --> D[app-exp]
  D --> E[var-exp]
  E --> F[id: x]
  D --> G[var-exp]
  G --> H[id: x]

  A --> I[lambda-exp]
  I --> J[id: y]
  I --> K[var-exp]
  K --> L[id: y]
```
