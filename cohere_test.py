import cohere

# Paste your API key here
co = cohere.Client("EVQzIdFzZWHbm9mjuaN6h0ed3Cq4iEOET3iyf1v6")

response = co.generate(
    model='command',
    prompt='Give me 3 simple AI project ideas for beginners.',
    max_tokens=100
)

print(response.generations[0].text)
