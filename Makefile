MAIN=main

pdf:
	latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error $(MAIN).tex

clean:
	latexmk -C $(MAIN).tex
