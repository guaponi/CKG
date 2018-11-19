import os.path
from graphdb_builder.databases.config import hgncConfig as iconfig
from graphdb_builder import builder_utils

#########################################
#          HUGO Gene Nomenclature       # 
#########################################
def parser(databases_directory, download = True):
    url = iconfig.hgnc_url
    entities = set()
    relationships = set()
    directory = os.path.join(databases_directory,"HGNC")
    builder_utils.checkDirectory(directory)
    fileName = os.path.join(directory, url.split('/')[-1])
    taxid = 9606
    entities_header = iconfig.header
    
    if download:
        builder_utils.downloadDB(url, directory)
    
    with open(fileName, 'r') as df:
        first = True
        for line in df:
            if first:
                first = False
                continue
            data = line.rstrip("\r\n").split("\t")
            geneSymbol = data[1]
            geneName = data[2]
            status = data[5]
            geneFamily = data[12]
            synonyms = data[18:23]
            transcript = data[23]
            if status != "Approved":
                continue

            entities.add((geneSymbol, "Gene", geneName, geneFamily, ",".join(synonyms), taxid))
            #relationships.add((geneSymbol, transcript, "TRANSCRIBED_INTO"))

    return entities, entities_header

