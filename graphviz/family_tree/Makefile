NAME = family_tree

DOT = dot
DOT_FLAGS = -Tpdf

DOT2TEX = dot2tex
DOT2TEX_FLAGS = -ftikz 
LATEX = latex

SOURCE = $(NAME).gv
TARGET = $(NAME).pdf
TARGET_DOT = $(NAME)_dot.pdf
TEX_FILE = $(NAME).tex
DVI_FILE = $(NAME).dvi
LATEX_OUTPUT = $(NAME)_latex.pdf
DVIPDF = dvipdf

all: PDF #TEX

PDF:
	$(DOT) $(DOT_FLAGS) $(SOURCE) -o $(TARGET_DOT)

TEX:
	$(DOT2TEX) $(DOT2TEX_FLAGS) $(SOURCE) > $(TEX_FILE)
	$(LATEX) $(TEX_FILE)
	$(LATEX) $(TEX_FILE)
	$(DVIPDF) $(DVI_FILE) 

clean:
	rm -f $(TARGET) *~ $(TEX_FILE) $(DVI_FILE) *log *aux $(TARGET_DOT)
