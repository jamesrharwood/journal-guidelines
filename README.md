# Medical journal policies regarding reporting guidelines

## Automated cross sectional survey of medical journals author guidelines pages
## To determine how many make reference to key reporting guidelines or the EQUATOR-Network

1. We downloaded a list of all journals indexed in Medline. We only included those labelled as [currently active](https://www.ncbi.nlm.nih.gov/nlmcatalog?term=currentlyindexed%5BAll%20Fields%5D%20AND%20currentlyindexedelectronic%5BAll%20Fields%5D&cmd=DetailsSearch) on Jan 28th 2021. Raw data available in data/medline_journals.xml
2. Extracted the journal IDs, titles, URLs, and subject areas - data/data.csv
3. We used a semi-automated, iterative process to find and scrape author guideline pages. Generally publishers use similar URL patterns across their journals so we automate as far as possible and then fill in the blanks when necessary.
4. We attempt to comfirm that we have scraped the correct page successfully by looking for the presence of phrases common to author guideline pages: table, figure, abstract etc.
5. We use regular expressions to check for mentions of, or links to, the EQUATOR Network or common reporting guidelines.
