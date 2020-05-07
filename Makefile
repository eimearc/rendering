RENDER=prman
SLCOMPILER=oslc
VIEWER=sho
SLEXT=oso

SHADERNAME=mug

SHADERS = mug.oso smudge.oso

.SUFFIXES: .osl .oso
.osl.oso:
	${SLCOMPILER} $<

all: ${SHADERS}

clean :
	rm -f ${SHADERNAME}.oso