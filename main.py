#open google
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys

from tkinter import  ttk
from tkinter import *

import yagmail

root=Tk()
root.title('send bunch of inquiry emails')
#frame entry for search and button
frameUpper=Frame(master=root,borderwidth=3,relief='flat',padx=12,pady=12)
frameUpper.grid(row=0,column=0,sticky=(E,W))
#frame for text to send via email
frameBtm=Frame(master=root,borderwidth=3,relief='groove',padx=12,pady=12,width=200,height=100)
frameBtm.grid(row=1,column=0,sticky=(N,S,E,W))

frm_emails=ttk.Frame(master=root,padding=3,borderwidth=3,width=300,relief='sunken')

var_inp=StringVar()
lbl_search=Label(master=frameUpper,text='enter search keyword:')
entry_search=Entry(master=frameUpper,width=33,textvariable=var_inp,relief='groove')

#text editor
txt_greetings='Hi,'
search_variable='keyword'
txt_body=f'I would like to have price information for {search_variable} for our company located in Azerbaijan'
txt_regards='Kind regards,'
btn_radio=StringVar()
btn_radio_greeting=ttk.Radiobutton(master=frameBtm,text='Greetings',variable=btn_radio,value=txt_greetings)
btn_radio_body=ttk.Radiobutton(master=frameBtm,text='Body',variable=btn_radio,value=txt_body)
btn_radio_regards=ttk.Radiobutton(master=frameBtm,text='Regards',variable=btn_radio,value=txt_regards)
lbl_text_message=Label(master=frameBtm,text='text message for email')
entry_msg_txt=StringVar()
entry_text=Entry(master=frameBtm,textvariable=entry_msg_txt,borderwidth=1,width=20)

def start_scraping(event=None):
    global search_variable
    search_variable = var_inp.get()

    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument("start-maximized")
    # options.add_experimental_option("detach", True)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://www.google.com/')

    # search for image
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "q"))).send_keys(search_variable + Keys.RETURN)
    # find first 10 companies
    res_lst = []
    res = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'cite')))

    for r in res:
        res_lst.append(driver.execute_script("return arguments[0].firstChild.textContent;", r))



    # take email addresses from company
    import re
    emails_lst = []
    for i in range(len(res_lst)):
        driver.get(res_lst[i])
        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
        html = driver.page_source
        emails = re.findall(email_pattern, html)
        driver.implicitly_wait(5)
        print(emails)
        emails_lst.append(emails)

    driver.close()


    flattened_list = [item for sublist in emails_lst for item in sublist]

    global no_duplicates
    no_duplicates = [x for n, x in enumerate(flattened_list) if x not in flattened_list[:n]]

    func_x()
    send_mail()

def func_x():
    frm_emails.grid(row=2,sticky=(S,E,W))
    Label(master=frm_emails, text=no_duplicates,wraplength=200).pack()

lbl_search.grid(sticky=(E,W))
entry_search.grid(sticky=(E,W))
entry_search.bind('<Return>', start_scraping)
Button(master=frameUpper, width=13, command=start_scraping, text='run').grid(pady=5)

btn_radio_greeting.grid(row=1,column=0,sticky=(W,))
btn_radio_body.grid(row=2,column=0,sticky=(W,))
btn_radio_regards.grid(row=3,column=0,sticky=(W,))

def change_value_btn_greetings(event):
    entry_msg_txt.set(btn_radio.get())
    txt_greetings=entry_msg_txt.get()


def change_value_btn_body(event):
    entry_msg_txt.set(btn_radio.get())
    txt_body=entry_msg_txt.get()


def change_value_btn_regards(event):
    entry_msg_txt.set(btn_radio.get())
    txt_regards=entry_msg_txt.get()


btn_radio_greeting.bind('<Double-1>',change_value_btn_greetings)
btn_radio_body.bind('<Double-1>',change_value_btn_body)
btn_radio_regards.bind('<Double-1>',change_value_btn_regards)

lbl_text_message.grid(row=0,column=0,rowspan=1,columnspan=1,sticky=(W))
entry_text.grid(row=1,column=1,rowspan=3,columnspan=3,sticky=(N,S,E,W))

root.columnconfigure(0,weight=1)
root.rowconfigure(1,weight=1)

frameUpper.columnconfigure(0,weight=1)

frameBtm.columnconfigure(0,weight=1)
frameBtm.rowconfigure(0,weight=1)
frameBtm.columnconfigure(1,weight=5)
frameBtm.rowconfigure(1,weight=5)
lbl_text_message.rowconfigure(0,weight=1)
lbl_text_message.columnconfigure(0,weight=1)
entry_text.rowconfigure(1,weight=5)
entry_text.columnconfigure(1,weight=5)

frm_emails.rowconfigure(0,weight=1)
frm_emails.columnconfigure(0,weight=1)

def get_value_from_entry_txt_put_to_variable(event):
    global txt_greetings
    global txt_body
    global txt_regards
    global txt_message_to_send
    print(btn_radio.get())
    if btn_radio.get()==txt_regards:
        print('btn_radio_regards')
        txt_regards = entry_msg_txt.get()
    elif btn_radio.get()==txt_body:
        print('btn_radio_body')
        txt_body = entry_msg_txt.get()
    elif btn_radio.get()==txt_greetings:
        print('btn_radio_greeting')
        txt_greetings = entry_msg_txt.get()
    print(txt_message_to_send,'---')
    txt_message_to_send = txt_greetings + '\n' + txt_body + '\n' + txt_regards
    print(txt_message_to_send, '-+-')
    test_print()

entry_text.bind('<Return>',get_value_from_entry_txt_put_to_variable)
# send emails
txt_message_to_send=txt_greetings+'\n'+txt_body+'\n'+txt_regards
def test_print():
    print(txt_message_to_send,'+++')

def send_mail():
    print(search_variable)
    receivers = no_duplicates
    body = txt_message_to_send

    email = yagmail.SMTP("company.caucasus.aze@gmail.com","fzcgkmwqspxvbxlp")
    for receiver in receivers:
        email.send(
            to=receiver,
            subject=f"Inquiry about {search_variable}",
            contents=body,
        )


if __name__=='__main__':
    root.mainloop()

#pyinstaller -F  main.py --onefile --noconsole