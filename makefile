all: dist/index.html

dist/index.html: src/index.html
	cp $< $@
	# Remove leading whitespace
	sed -i -e "s/^\s*//g" $@
	# Remove comments
	sed -i -e "s/\/\/.*//g" $@
	# Remove blank lines
	sed -i -e "/^\s*$$/d" $@		

test: dist/index.html
	@echo Tests disabled temporarily on this branch
	@#python3 src/test.py

clean:
	rm -f dist/index.html
	rm -f geckodriver*
