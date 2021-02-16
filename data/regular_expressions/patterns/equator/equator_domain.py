pattern = r"equator-network\.org"
matches = [
    "equator-network.org",
    ("www.equator-network.org", 1),
    ("https://www.equator-network.org", 1),
    ("http://equator-network.org/reporting-guidelines/prisma", 1),
    ("equator-network.org something", "equator-network.org"),
]
non_matches = ["something else"]
