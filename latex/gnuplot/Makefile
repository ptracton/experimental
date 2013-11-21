
LATEX = pdflatex
DVIPDF = dvipdf
LATEX_OPTIONS = 

SRC_DIR = src
OUTPUT_DIR = outputs
DOCS_DIR = docs

DOC_NAME_ROOT = gnuplot
DOC_SRC = $(SRC_DIR)/$(DOC_NAME_ROOT).tex
DOC_PDF = $(DOCS_DIR)/$(DOC_NAME_ROOT).pdf

RM = /bin/rm
MV = /bin/mv

all: document

document:
	mkdir -p $(OUTPUT_DIR) $(DOCS_DIR)
	gnuplot $(SRC_DIR)/gnuplot.gp
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
	$(LATEX) $(LATEX_OPTIONS) -output-directory=$(OUTPUT_DIR) $(DOC_SRC)
	$(MV) $(OUTPUT_DIR)/$(DOC_NAME_ROOT).pdf $(DOC_PDF)


clean:
	$(RM) -rf $(SRC_DIR)/*~ *~ $(DOC_PDF)  $(OUTPUT_DIR) $(DOCS_DIR) $(SRC_DIR)/eg2.tex

