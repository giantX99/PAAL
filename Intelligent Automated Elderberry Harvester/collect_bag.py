import shutil, time, pyrealsense2 as rs

'''
class Pipeline:
    
    def __init__(self, filepath='test.bag'):
        self.filepath = filepath
        context       = rs2.context()
        self.device   = device = context.devices[0]
        serial_number = device.get_info(rs2.camera_info.serial_number)
        get_sensor    = lambda s: s.get_info(rs2.camera_info.name)
        self.sensors  = {get_sensor(s): s for s in device.sensors}        
        self.config   = config = rs2.config()
        self.pipeline = rs2.pipeline(context)
        config.enable_device(serial_number)
        config.enable_record_to_file('tmp.bag')
        
    def start(self): self.pipeline.start(self.config)
        
    def stop(self):
        self.pipeline.stop()
        
        # When the lines below are un-commented, the bag seems to write
        # properly. When they are commented, the bag produces an index error.
        
        #del self.pipeline
        #del self.config
        #del self.sensors
        #del self.device
        #self.pipeline = None
        #self.config = None
        #self.sensors = None
        #self.device = None
        
        shutil.move('tmp.bag', self.filepath)
        

if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.start()
    time.sleep(1)
    pipeline.stop()
'''

#serial_num_1 = '203522252121' # Old camera d455 (Yellow)
serial_num_2 = '213522252513' # New camera d455 (Green)

# camera 1:
#pipe_cam1 = rs.pipeline()
#config_cam1 = rs.config()
#config_cam1.enable_device(serial_num_1)
#config_cam1.enable_record_to_file('tmp.bag')

# camera 2 (green):
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_record_to_file('tmp.bag')

try:
    while True:
        pipe_cam2.start(config_cam2)

except KeyboardInterrupt:
    pipe_cam2.stop()
    pass

