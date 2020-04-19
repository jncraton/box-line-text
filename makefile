all: dist/index.html

dist/index.html: src/index.html
	cp $< $@
	# Remove leading whitespace
	sed -i -e "s/^\s*//g" $@
	# Remove comments
	sed -i -e "s/\/\/.*//g" $@
	# Remove blank lines
	sed -i -e "/^\s*$$/d" $@		

clean:
	rm -f dist/index.html
