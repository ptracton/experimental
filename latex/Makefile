
LATEX = latex
DVIPDF = dvipdf
LATEX_OPTIONS = 

SRC_DIR = src
OUTPUT_DIR = outputs
DOCS_DIR = docs

DOC_NAME_ROOT = document
DOC_SRC = $(SRC_DIR)/$(DOC_NAME_ROOT).tex
DOC_PDF = $(DOCS_DIR)/$(DOC_NAME_ROOT).pdf

RM = /bin/rm

all: document

document:
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
	$(DVIPDF) $(OUTPUT_DIR)/$(DOC_NAME_ROOT).dvi $(DOC_PDF)



clean:
	$(RM) -rf $(SRC_DIR)/*~ *~ $(DOC_PDF)  $(OUTPUT_DIR)/*
	touch $(OUTPUT_DIR)read.me