NAME = dsp

DOT = dot
DOT_FLAGS = -Tpng

DOT2TEX = dot2tex
DOT2TEX_FLAGS = -ftikz 
LATEX = latex

SOURCE = $(NAME).gv
TARGET = $(NAME).pdf
TARGET_DOT = $(NAME)_dot.png
TEX_FILE = $(NAME).tex
DVI_FILE = $(NAME).dvi
LATEX_OUTPUT = $(NAME)_latex.pdf
DVIPDF = dvipdf

all: PNG #PDF TEX

PNG:
	$(DOT) $(DOT_FLAGS) $(SOURCE) -o $(TARGET_DOT)

TEX:
	$(DOT2TEX) $(DOT2TEX_FLAGS) $(SOURCE) > $(TEX_FILE)
	$(LATEX) $(TEX_FILE)
	$(LATEX) $(TEX_FILE)
	$(DVIPDF) $(DVI_FILE) 

clean:
	rm -f $(TARGET) *~ $(TEX_FILE) $(DVI_FILE) *log *aux $(TARGET_DOT)
