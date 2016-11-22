paper:
	pdflatex research_statement_jiang_2page.tex
	bibtex research_statement_jiang_2page
	pdflatex research_statement_jiang_2page.tex
	pdflatex research_statement_jiang_2page.tex
	make clean
	open research_statement_jiang_2page.pdf

clean:
	\rm -f *.dvi *.ps *.bbl *.aux *.log *.blg *.toc all.tar* uu \
	*~ *.bak *.lbl *.brf *.out

spotless: clean
	\rm -f *.pdf
