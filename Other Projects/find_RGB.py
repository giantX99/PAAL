import glob
import os
import shutil

ir_base_root = ''
rgb_root = ''
save_root = ''

ids3 = ['947','842','33016','950','814','782','158','33073','33040','33049','951','790','33015','33014','157']
ids4 = ['40054','40086','40051','40040','40319','40115','40987','40141','40114','40883','40026','40867','40060',
        '40069','44107','44212','44219']
ids5 = ['50805','50089','50221', '50151', '50974','50919','50094','50222','50981','50043','50078','50079',
        '50031','50152']

id_list = [ids3, ids4, ids5]

batch_counter = 3
current_pid = 'No PID processed'
try:
    for ids in id_list:
        for pid in ids:
            current_pid = pid
            ir_names = glob.glob(ir_base_root + str(batch_counter) + '/ID_' + pid + '/5/1/*.png')
            rgb_path = rgb_root + str(batch_counter) + '/ID_' + pid + 'RGB/'

            saving_path = save_root + pid + '/'
            if not os.path.exists(saving_path):
                os.makedirs(saving_path)
            
            for file in ir_names:
                rgb = os.path.basename(file)
                if rgb in os.listdir(rgb_path):
                    shutil.copy(rgb_path + rgb, saving_path + rgb)
            
            print("Batch: ", batch_counter, " ID: ", pid, " COMPLETED.")
        batch_counter+=1
except RuntimeError:
    print("Script ERROR.\nLast Batch Processed: ", batch_counter, "\nLast ID Processed: ", current_pid)