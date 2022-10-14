import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
pipeline_profile = pipeline.start(config)
device = pipeline_profile.get_device()
depth_sensor = device.query_sensors()[0]
emitter = depth_sensor.set_option(rs.option.emitter_on_off, 1)

'''
set_emitter = 0
depth_sensor.set_option(rs.option.emitter_enabled, set_emitter)
emitter1 = depth_sensor.get_option(rs.option.emitter_enabled)
print("new emitter = ", emitter1)'''