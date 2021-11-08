all: test

target.bc: target.c
	clang -emit-llvm -c target.c

test cfg.dot: target.bc analysis.py
	./analysis.py target.bc

cfg.pdf: cfg.dot
	dot -Tpdf cfg.dot > cfg.pdf

.PHONY: test all clean

clean:
	rm -f *.bc *~ *.o *.dot *.pdf


