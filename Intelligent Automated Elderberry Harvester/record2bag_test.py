import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
serial_num_2 = '213522252513'
config.enable_device(serial_num_2)
#config.enable_record_to_file('test.bag')

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

my_device = pipeline_profile.get_device(serial_num_2)


recorder = rs.recorder('test2.bag', my_device)
print(type(recorder))
recorder.as_recorder()
print(type(recorder))
recorder.pause()


pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        recorder.resume()

except KeyboardInterrupt: #^c
    pipeline.stop()
    pass
