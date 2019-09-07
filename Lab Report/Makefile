PAPER = Lab_1_Report
TEX = $(wildcard *.tex)
BIB = bibliography.bib
FIGS = $(wildcard figs/*.pdf figs/*.png graphs/*.pdf graphs/*.png)
FLAGS = --shell-escape

.PHONY: all clean

$(PAPER).pdf: $(TEX) $(BIB) $(FIGS)
	echo $(FIGS)
	pdflatex $(FLAGS) $(PAPER)
	bibtex $(PAPER)
	pdflatex $(FLAGS) $(PAPER)
	pdflatex $(FLAGS) $(PAPER)

clean:
	rm -f *.aux *.bbl *.blg *.log *.out $(PAPER).pdf *.fls *.fdb_latexmk
