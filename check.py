import pandas as pd
import sys
from rdflib import Graph

df = pd.read_pickle("root_table.pkl")

# Get list of recommended properties per class

classes = ['p', 'tc', 'c', 'r', 'm', 'pub', 'pl', 'o', 'pe']

recommended = {key: set() for key in classes}

for index, row in df.iterrows():
    property_name = row["Property"]
    property_rec = row["Recommended Class"].split(",")
    for item in classes:
        if item in property_rec:
            recommended[item].add(property_name)

print(recommended)

# Get metadata for resource

if __name__ == "__main__":
    id = sys.argv[1]

id = "533800"

url = f"https://arche-curation.acdh-dev.oeaw.ac.at/api/{id}/metadata"
subject = f"https://arche-curation.acdh-dev.oeaw.ac.at/api/{id}"

g = Graph()
g.parse(url)
g.bind("acdh", "https://vocabs.acdh.oeaw.ac.at/schema#")

# Get type of resource

query = f"""
SELECT ?o WHERE {{ <{subject}> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?o }}
"""

results = g.query(query)
if len(results) > 1:
    print("More than one class found.")
else:
    for result in results:
        res_type = result.o.split("#")[1]
        print(res_type)

# Check which recommended properties are present

mapping = {
    'TopCollection': 'tc',
    'Collection': 'c',
    'Resource': 'r',
    'Metadata': 'm',
    'Project': 'p',
    'Publication': 'pub',
    'Place': 'pl',
    'Organisation': 'o',
    'Person': 'pe'
}

query = f"""
SELECT DISTINCT ?p WHERE {{ <{subject}> ?p ?o }}
"""

results = [result.p.split("#")[1] for result in g.query(query)]
print("================================")
print("Recommended properties PRESENT")
for property in recommended[mapping[res_type]]:
    if property in results:
        print(property)
print("================================")
print("Recommended properties MISSING")
for property in recommended[mapping[res_type]]:
    if property not in results:
        print(property)

# Check which optional properties are present

# Check which language tags are present (even when they are not needed)