# This makefile:
# * Converts KiCad exported Gerber files to G-code files usable with LinuxCNC
# * Merges drill toolpaths to one 1mm drill toolpath

MILL_FEED=500
DRILL_FEED=500
SPINDLE_SPEED=6000
FINISH_HEIGHT=50
DRILL_DEPTH=5

all: export/sumochip_drill.ngc export/sumochip-panel_drill.ngc export/sumochip-panel-half_drill.ngc

%_drill.ngc: %-merged.drl %-F.Cu.gtl %-B.Cu.gbl
	pcb2gcode \
		--front $*-F.Cu.gtl \
		--back $*-B.Cu.gbl \
		--drill $*-merged.drl \
		--front-output $*_front.ngc \
		--back-output $*_back.ngc \
		--drill-output $*_drill.ngc \
		--metric \
		--zsafe 3 --zchange ${FINISH_HEIGHT} \
		--zwork 0 --offset 0.5 --mill-feed ${MILL_FEED} --mill-speed ${SPINDLE_SPEED} \
		--zdrill -${DRILL_DEPTH} --drill-feed ${DRILL_FEED} --drill-speed ${SPINDLE_SPEED}

%-merged.drl: %.drl
	sed -e 's/^T[2-9]C.*$$//g' -e 's/^T1C.*$$/T1C1.000/' -e 's/^T[1-9]$$//g' $< > $@  

clean:
	rm -fv export/*.ngc export/*-merged.drl
