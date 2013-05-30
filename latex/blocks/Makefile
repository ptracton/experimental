
LATEX = pdflatex
DVIPDF = dvipdf
LATEX_OPTIONS = 

SRC_DIR = src
OUTPUT_DIR = outputs
DOCS_DIR = docs

DOC_NAME_ROOT = blocks
DOC_SRC = $(SRC_DIR)/$(DOC_NAME_ROOT).tex
DOC_PDF = $(DOCS_DIR)/$(DOC_NAME_ROOT).pdf

RM = /bin/rm
MV = /bin/mv

all: document

document:
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
	$(MV) $(OUTPUT_DIR)/$(DOC_NAME_ROOT).pdf $(DOC_PDF)


clean:
	$(RM) -rf $(SRC_DIR)/*~ *~ $(DOC_PDF)  $(OUTPUT_DIR)/*
	touch $(OUTPUT_DIR)read.me