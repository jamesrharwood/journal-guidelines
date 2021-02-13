pattern = r"equator-network.org"
matches = [
    ("equator-network.org", pattern),
    ("www.equator-network.org", pattern),
    ("https://www.equator-network.org", pattern),
    ("http://equator-network.org/reporting-guidelines/prisma", pattern),
    ("equator-network.org something", "equator-network.org"),
]
non_matches = ["something else"]
