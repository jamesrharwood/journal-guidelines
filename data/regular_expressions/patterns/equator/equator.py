from data.regular_expressions.patterns.common.dash import pattern as dash

pattern = fr"\bequator([\s{dash}]*network)?"
matches = [
    "Equator",
    "EQUATOR-Network",
    "EQUATOR Network",
    (" equator", "equator"),
    "EQUATOR — network",
]
non_matches = ["network", "Eequator"]
