from todloop.routines import Logger, DataLoader
from todloop.tod import TODLoader, TODInfoLoader
from todloop.base import TODLoop
from routines import CRCorrelationFilter, FRBCorrelationFilter, SlowCorrelationFilter, DurationFilter, PixelFilter,ScatterPlot,EdgeFilter
from deconv_routine import Deconvolution
from calibration.routines import FixOpticalSign, CalibrateTOD
from plotter import PlotGlitches
from histogram import PlotHistogram, CreateHistogram

"""
LOAD CUTS DATA
"""

loop = TODLoop()
tod_id = 10000
loop.add_tod_list("../data/s16_pa3_list.txt")
loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/cosig/", output_key="cuts"))


"""
LOAD FILTERED DATA (UPTO TRACK 5000) AND PLOT A HISTOGRAM OF # OF PIXELS AFFECTED
"""
#loop.add_routine(DataLoader(input_dir="../outputs/s16_pa3_list/events/",output_key ="events"))
#loop.add_routine(Logger(input_key="events"))
#loop.add_routine(PlotHistogram(events_key="events"))
#loop.add_routine(CreateHistogram(cosig_key="cuts"))

"""
LOAD TOD DATA 
"""

loop.add_routine(TODLoader(output_key="tod_data"))
#loop.add_routine(Deconvolution(output_key="tod_data")) #load deconv data
loop.add_routine(FixOpticalSign(input_key="tod_data", output_key="tod_data"))
loop.add_routine(CalibrateTOD(input_key="tod_data",output_key="tod_data"))


"""
FILTER ROUTINES 
"""

loop.add_routine(PixelFilter(input_key="cuts",output_key="frb_cuts"))
loop.add_routine(DurationFilter(max_duration=5,input_key="frb_cuts",output_key="frb_cuts"))
loop.add_routine(FRBCorrelationFilter(tod_key="tod_data", cosig_key="frb_cuts", output_key ="frb_events",all_coeff_output_key="frb_coeff"))
loop.add_routine(EdgeFilter(input_key="frb_events",output_key="frb_events"))

#loop.add_routine(PixelFilter(min_pixels=4,max_pixels=10, input_key="cuts", output_key="cr_cuts"))
#loop.add_routine(CRCorrelationFilter(tod_key="tod_data", cosig_key="cr_cuts", output_key= "cr_events",all_coeff_output_key="cr_coeff"))

#loop.add_routine(DurationFilter(min_duration=50,input_key ="cuts",output_key="slow_cuts"))
#loop.add_routine(SlowCorrelationFilter(tod_key="tod_data", cosig_key="slow_cuts", output_key= "slow_events",all_coeff_output_key="slow_coeff"))

"""
SCATTER PLOT
Uncomment to see scatter plots of coefficients
!!! AND change all cosig keys to "cuts" and comment out all additional filters
"""
#loop.add_routine(ScatterPlot(frb_input_key="frb_coeff",cr_input_key="cr_coeff",slow_input_key="slow_coeff"))

"""
PLOT A GLITCH
"""
loop.add_routine(PlotGlitches(tag=tod_id,tod_key="tod_data", cosig_key="cuts"))
loop.run(tod_id, tod_id + 1)









