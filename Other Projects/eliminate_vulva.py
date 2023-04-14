import random
import glob
import os

rgb_root = ''

#ids3 = ['947','842','33016','950','814','782','158','33073','33040','33049','951','790','33015','33014','157']
ids4 = ['40054','40086','40051','40040','40319','40115','40987','40141','40114','40883','40026','40867','40060',
        '40069','44107','44212','44219']
ids5 = ['50805','50089','50221', '50151', '50974','50919','50094','50222','50981','50043','50078','50079',
        '50031','50152']

id_list = [ids4, ids5]

batch_counter = 4
current_pid = 'No PID processed'
try:
    for ids in id_list:
        for pid in ids:
            current_pid = pid
            rgb_path = glob.glob(rgb_root + str(batch_counter) + '/ID_' + pid + '/*.png')
            random.shuffle(rgb_path)

            if len(rgb_path) <= 50:
                continue
            remove_num = len(rgb_path) - 50
            remove_counter = 1
            for file in rgb_path:
                os.remove(file)
                if remove_counter == remove_num:
                    break
                remove_counter += 1

            print("Batch ", batch_counter, ", ID_", pid, ": ", remove_num, " Files removed.")
        
        batch_counter+=1
except RuntimeError:
    print("Script ERROR.\nLast Batch Processed: ", batch_counter, "\nLast ID Processed: ", current_pid)