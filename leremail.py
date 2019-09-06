import imaplib
import email
import json
import sys
import html


dados_email = {}
with open("dados_acesso_email.json") as json_file:
    dados_email = json.load(json_file)

# filtro = sys.argv[1]

FROM_EMAIL = dados_email["FROM_EMAIL"]
FROM_PWD = dados_email["FROM_PWD"]
SMTP_SERVER = dados_email["SMTP_SERVER"]
SMTP_PORT = dados_email["SMTP_PORT"]

try:
    # colocando os valores no campo de email
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox', readonly=False)
    # buscando tudo que o assunto seja 
    # type_mail, data = mail.search(None, '(SUBJECT "'+filtro+'")')
    type_mail, data = mail.search(None, 'unseen')
    mail_ids = data[0]

    id_list = mail_ids.split()
    print(id_list)
    first_email_id = int(id_list[0])-1
    latest_email_id = int(id_list[-1])
    print("Reading emails from {} to {}.\n\n".format(latest_email_id, first_email_id))

    for i in range(latest_email_id, first_email_id, -1):
        typ, data = mail.fetch(str.encode(str(i)), '(RFC822)')
        if str(i) in str(id_list):
            for response_part in data:
                if not isinstance(response_part, tuple):
                    continue
                msg = email.message_from_bytes(response_part[1])
                #mail_str = str(msg)

                # Se e-mail nao contem a estrutura que precisamos, nao processa
                # if mail_str.find('oi') <= 1:
                    # continue

                email_subject = msg['subject']
                email_from = msg['from']

                print('mail_str : ' + msg.get_payload(0).get_payload() + '\n')
                
                mail.store(str.encode(str(i)), '+X-GM-LABELS', 'Espana')

                print('----------------------------------------------------------')
                print('----------------------------------------------------------')

    mail.logout()

except Exception as e:
    print(e)