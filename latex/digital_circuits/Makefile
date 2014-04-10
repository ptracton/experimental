
LATEX = pdflatex
DVIPDF = dvipdf
LATEX_OPTIONS = 

SRC_DIR = src
OUTPUT_DIR = outputs
DOCS_DIR = docs

DOC_NAME_ROOT = digital_circuits
DOC_SRC = $(SRC_DIR)/$(DOC_NAME_ROOT).tex
DOC_PDF = $(DOCS_DIR)/$(DOC_NAME_ROOT).pdf

RM = /bin/rm

all: dirs document

dirs:
	mkdir -p $(OUTPUT_DIR)
	mkdir -p $(DOCS_DIR)

document:
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
#	$(DVIPDF) $(OUTPUT_DIR)/$(DOC_NAME_ROOT).dvi $(DOC_PDF)



clean:
	find . -name "*~" | xargs rm -f 
	$(RM) -rf $(DOCS_DIR) $(OUTPUT_DIR)
