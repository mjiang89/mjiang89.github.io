paper:
	pdflatex research_statement_jiang.tex
	bibtex research_statement_jiang
	pdflatex research_statement_jiang.tex
	pdflatex research_statement_jiang.tex
	make clean
	open research_statement_jiang.pdf

clean:
	\rm -f *.dvi *.ps *.bbl *.aux *.log *.blg *.toc all.tar* uu \
	*~ *.bak *.lbl *.brf *.out

spotless: clean
	\rm -f *.pdf
