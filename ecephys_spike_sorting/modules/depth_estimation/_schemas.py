from argschema import ArgSchema, ArgSchemaParser 
from argschema.schemas import DefaultSchema
from argschema.fields import Nested, InputDir, NumpyArray, String, Float, Dict, Int, Bool, OutputFile
from ...common.schemas import EphysParams, Directories, CommonFiles

class DepthEstimationParams(DefaultSchema):
    hi_noise_thresh = Float(required=True, default=50.0, help='Max RMS noise for including channels')
    lo_noise_thresh = Float(required=True, default=3.0, help='Min RMS noise for including channels')

    save_figure = Bool(required=True, default=True)
    figure_location = OutputFile(required=True, default=None)
    
    smoothing_amount = Int(required=True, default=5, help='Gaussian smoothing parameter to reduce channel-to-channel noise')
    power_thresh = Float(required=True, default=2.5, help='Ignore threshold crossings if power is above this level (indicates channels are in the brain)')
    diff_thresh = Float(required=True, default=-0.07, help='Threshold to detect large increases is power at brain surface')
    freq_range = NumpyArray(required=True, default=[0,10], help='Frequency band for detecting power increases')
    max_freq = Int(required=True, default=150, help='Maximum frequency to plot')
    channel_range = NumpyArray(required=True, default=[370,380], help='Channels assumed to be out of brain, but in saline')
    n_passes = Int(required=True, default=10, help='Number of times to compute offset and surface channel')
    skip_s_per_pass = Int(required=True, default=100, help='Number of seconds between data chunks used on each pass')
    start_time = Float(required=True, default=0, help='First time (in seconds) for computing median offset')
    time_interval = Float(required=True, default=5, help='Number of seconds for computing median offset')

    nfft = Int(required=True, default=4096, help='Length of FFT used for calculations')

    air_gap = Int(required=True, default=100, help='Approximate number of channels between brain surface and air')

class InputParameters(ArgSchema):
    
    depth_estimation_params = Nested(DepthEstimationParams)

    ephys_params = Nested(EphysParams)
    directories = Nested(Directories)
    common_files = Nested(CommonFiles)

class OutputSchema(DefaultSchema): 

    input_parameters = Nested(InputParameters, 
                              description=("Input parameters the module " 
                                           "was run with"), 
                              required=True) 
 
class OutputParameters(OutputSchema): 

    surface_channel = Int()
    air_channel = Int()
    probe_json = String()
    execution_time = Float()  