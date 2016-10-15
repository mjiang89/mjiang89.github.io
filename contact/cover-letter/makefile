paper:
	pdflatex cover_letter_jiang.tex
	pdflatex cover_letter_jiang.tex
	make clean
	open cover_letter_jiang.pdf

clean:
	\rm -f *.dvi *.ps *.bbl *.aux *.log *.blg *.toc all.tar* uu \
	*~ *.bak *.lbl *.brf *.out

spotless: clean
	\rm -f *.pdf
