paper:
	pdflatex teaching_statement_jiang.tex
	bibtex teaching_statement_jiang
	pdflatex teaching_statement_jiang.tex
	pdflatex teaching_statement_jiang.tex
	make clean
	open teaching_statement_jiang.pdf

clean:
	\rm -f *.dvi *.ps *.bbl *.aux *.log *.blg *.toc all.tar* uu \
	*~ *.bak *.lbl *.brf *.out

spotless: clean
	\rm -f *.pdf
