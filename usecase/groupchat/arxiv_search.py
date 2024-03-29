# filename: arxiv_search.py

import requests
from bs4 import BeautifulSoup

def search_papers(query, max_results=5):
    # Send a GET request to Arxiv's API with the search query
    url = f'http://export.arxiv.org/api/query?search_query=all:{query}&sortBy=lastUpdatedDate&sortOrder=descending&start=0&max_results={max_results}'
    response = requests.get(url)
    response.raise_for_status() 

    # Parse the response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Fetch entries
    entries = soup.find_all('entry')
    
    # Store title, authors, abstract and link of each entry
    papers = []
    for entry in entries:
        title = entry.title.text
        authors = [author.get_text() for author in entry.find_all('name')]
        abstract = entry.summary.text
        link = entry.link['href']
        papers.append({
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'link': link
        })
    return papers

# Search for latest 'GPT-4' papers
papers = search_papers('GPT-4')

# Print the title, author list, abstract and link of each paper
for i, paper in enumerate(papers, start=1):
    print(f'Paper {i}:')
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'])}")
    print('Abstract:')
    print(paper['abstract'])
    print(f"PAPER URL: {paper['link']}")
    print('-'*80)