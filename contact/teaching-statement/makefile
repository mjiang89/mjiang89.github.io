paper:
	pdflatex meng.tex
	bibtex meng
	pdflatex meng.tex
	pdflatex meng.tex
	make clean
	open meng.pdf

clean:
	\rm -f *.dvi *.ps *.bbl *.aux *.log *.blg *.toc all.tar* uu \
	*~ *.bak *.lbl *.brf *.out

spotless: clean
	\rm -f *.pdf
