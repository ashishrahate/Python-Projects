"""THE FOLLOWING SCRIPT IS FOR SYSTEM OPTIMISATION.
    WHICH COLLECTS THE DATA OF THE MACHINE SUCH AS CPU , MEMORY,
    SWAP MEMORY, BATTERY USAGE ETC.

    - It returns the data in the form of an ordered dictionary.
    - converts it into a csv file and it is saved in files.
    - if the threshold is crossed it sends the selected data in a table format as an alert email.
    - at the end of every day the csv files are deleted.

    THIS CAN BE RUN ON THE MACHINE PERIODICALLY USING DIFFERENT SOFTWARE.

    """




import psutil
from collections import OrderedDict
import logging
from prettytable import *
import csv
import os
#from db_connectivity import *
from datetime import datetime
from pytz import timezone
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from django.utils.encoding import force_text



#from admin_repo import *

error_logger = logging.getLogger('error_logger')




def system_info():
        cpu_info = OrderedDict()

        cpu_times = psutil.cpu_times()
        cpu_freq = psutil.cpu_freq()
        disk_use = psutil.disk_usage('/')
        mem_virt = psutil.virtual_memory()
        mem_swap = psutil.swap_memory()
        battery = psutil.sensors_battery()
        user = psutil.users()



        cpu_info['cpu_use_percent'] = psutil.cpu_percent(interval=1, percpu = False)
        cpu_info['disk_use_percent'] = disk_use.percent
        cpu_info['memory_used_percent'] = mem_virt.percent
        if ((cpu_info["cpu_use_percent"] >= 90.00) and (cpu_info['memory_percent_used'] >= 80.00)) or cpu_info['disk_use_percent'] >= 90.00:
            flag = True
        else:
            flag = False

        cpu_info['threshold_exceeded'] = flag
        cpu_info['disk_total'] = float(disk_use.total/(1024*1024))
        cpu_info['disk_used'] = float(disk_use.used/(1024*1024))

        cpu_info['disk_free'] = float(disk_use.free/(1024*1024))

        cpu_info['total_memory'] = float(mem_virt.total/(1024*1024))
        cpu_info['used_memory'] = float(mem_virt.used/(1024*1024))

        cpu_info['availabel_memory'] = float(mem_virt.available/(1024*1024))
        cpu_info['swaptotal'] = float(mem_swap.total/(1024*1024))
        cpu_info['swap_used'] = float(mem_swap.used/(1024*1024))
        cpu_info['swap_percent_used'] = mem_swap.percent
        cpu_info['swapfree'] = float(mem_swap.free/(1024*1024))

        cpu_info['cpu_user_time'] = cpu_times.user
        cpu_info['cpu_system_time'] = cpu_times.system
        cpu_info['cpu_idle_time'] = cpu_times.idle

        cpu_info['free_memory'] =  float(mem_virt.free/(1024*1024))
        cpu_info['active_mem'] =  float(mem_virt.active/(1024*1024))
        cpu_info['cached_mem']  =  float(mem_virt.cached/(1024*1024))


        cpu_info['battery percent'] = battery.percent
        cpu_info['battery time left(mins)'] = float(battery.secsleft/(60))
        cpu_info['user_name'] = user[0].name
        cpu_info['user_host'] = user[0].host
        #cpu_info['mac_id'] = get_mac()


        now_utc = datetime.now(timezone('UTC'))
        now_pacific = now_utc.astimezone(timezone('Asia/Kolkata'))
        utc_datetime = now_utc.strftime("%Y-%m-%d %H:%M:%S")
        cpu_info['system_IST_datetime'] = now_pacific.strftime("%Y-%m-%d %H:%M:%S")
        cpu_info['system_datetime'] = utc_datetime

        return cpu_info

t = system_info()
x = PrettyTable()
mylist=[]
def msg_body():
        x.field_names = ['section                                 ', '                            amount']
        for i, j  in t.items():

                l =str(i)
                m= str(j)

                lis = [l,m]
                x.add_row(lis)
                mylist.append(lis)
        print(mylist)
        x.border = True
        x.align['section']="l"
        string_table= str(x)
        print(string_table)

        return string_table




recipient = "--- RECIPIENTS EMAIL ID---"


def send_debug_alert_mail( msg, subject, emails):

    email_body = msg
    # print('aws email triggered ')
    # subject = 'Humidity value notification'
    subject = subject
    to_email = emails

    SENDER = '---SENDERS EMAIL ID---'
    SENDERNAME = 'SENDERS NAME'

    RECIPIENT = to_email


    PASSWORD_SMTP = "--PASSWORD--"
    HOST = "smtp.gmail.com"
    PORT = 587


    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = RECIPIENT


    msg.attach(MIMEText(email_body, 'plain'))


    # Try to send the message.
    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(SENDER, PASSWORD_SMTP)
        server.sendmail(SENDER, RECIPIENT.split(','), msg.as_string())
        server.close()

        # ---
    # Display an error message if something goes wrong.
    except Exception as e:
                error_logger.error(e)

    return



# emailfunction call with csv attachments
msg1 = msg_body()
print(msg1)

def csv_manager():
        now = datetime.today()
        if now.hour >= 23 and now.minute >= 55 and now.second >= 00.00:
                os.remove('--YOUR FILENAME .csv--')


def write_data_to_csv(dictionary1):
        save_to = "--YOUR FILENAME .csv--"

        fieldname = dictionary1.keys()

        with open(save_to, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldname)
                writer.writeheader()
                writer.writerow(dictionary1)

        return

def email_csv_manager():

    d = system_info()
    # FOR THE FOLLOWING SET THE PREFERABLE THRESHOLDS FOR CPU , MEMORY AND DISK.
    if ((d["cpu_use_percent"] >= 00.00) and (d['memory_used_percent'] >= 00.00)) or d['disk_use_percent'] >= 80.00 == True:
        send_debug_alert_mail(msg1, 'system_threshold_exceeded!!!', recipient)


    write_data_to_csv(system_info())
    csv_manager()

email_csv_manager()



