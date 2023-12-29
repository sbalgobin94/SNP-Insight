import requests

def parse_23andme_file(file_path):
    """
    Parses the 23andMe file and extracts SNP data.
    """
    snps = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#') and line.strip():
                parts = line.split('\t')
                snps.append({'rsid': parts[0], 'chromosome': parts[1], 'position': parts[2], 'genotype': parts[3].strip()})
    return snps

def query_dbsnp_for_annotation(rsid):
    """
    Queries dbSNP (or a similar service) for annotations of a given rsid.
    Returns the annotation data.
    """
    # Construct the E-Search URL
    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=snp&term={rsid}[rsid]+AND+human[Organism]&retmode=json"
    
    # Make the search request
    search_response = requests.get(search_url)
    if search_response.status_code == 200:
        search_data = search_response.json()
        id_list = search_data["esearchresult"]["idlist"]
        if id_list:
            # Use the first ID for E-Summary (or iterate through all IDs as needed)
            id = id_list[0]
            summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=snp&id={id}&retmode=json"
            summary_response = requests.get(summary_url)
            if summary_response.status_code == 200:
                return summary_response.json()
    print("nothing found")
    return None

def process_23andme_file(file_path):
    """
    Process the 23andMe file and annotate SNPs using dbSNP.
    """
    snps = parse_23andme_file(file_path)
    annotated_snps = []

    for snp in snps:
        annotation = query_dbsnp_for_annotation(snp['rsid'])
        if annotation:
            snp['annotation'] = annotation
            annotated_snps.append(snp)

    return annotated_snps