# Medical journal policies regarding reporting guidelines

**Automated cross sectional survey of medical journals author guidelines pages**
**To determine how many make reference to key reporting guidelines or the EQUATOR-Network**

1. We downloaded a list of all journals indexed in Medline. We only included those labelled as [currently active](https://www.ncbi.nlm.nih.gov/nlmcatalog?term=currentlyindexed%5BAll%20Fields%5D%20AND%20currentlyindexedelectronic%5BAll%20Fields%5D&cmd=DetailsSearch) on Jan 28th 2021. We used the xml export over txt because the URL field in the txt format was harder to clean.
2. Extracted the journal IDs, titles, language, publisher, publication_type, URLs, and subject areas - data/journals.csv
3. Filtered out entries where Periodical wasn't listed as a publication type, or where no (non ovid) url was abailable.
4. We used an automated, iterative process to find and scrape author guideline pages. Generally publishers use similar URL patterns across their journals so we automate as far as possible and then fill in the blanks when necessary.
5. We attempt to comfirm that we have scraped the correct page successfully by looking for the presence of phrases common to author guideline pages: table, figure, abstract etc.
6. We use regular expressions to check for mentions of, or links to, the EQUATOR Network or common reporting guidelines.
