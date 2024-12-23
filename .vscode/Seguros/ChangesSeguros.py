import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyodbc

def fetch_data():
    connection_string = (
        "DRIVER={SQL Server};"
        "SERVER=SRV003;"
        "DATABASE=JVW;"
        "Trusted_Connection=yes;"
    )

    query = """
    SELECT  
        Aud.Dtt, 
        Aud.Fld,
        Aud.Old,
        Aud.New,
        Dos.Dos,
        Dos.Exe,
        Dos.Cor,
        clb1.Eml AS UsrEmail, 
        clb2.Eml AS NewExecutantEmail
    FROM JVW.dbo._aud AS Aud
    JOIN JVW.dbo.jvdclb AS clb1
        ON Aud.Usr = clb1.Ide
    JOIN JVW.dbo.jvddos AS Dos 
        ON Aud.Rid = Dos.Drn
    JOIN JVW.dbo.jvdclb AS clb2
        ON Aud.New = clb2.Mnm
    WHERE Aud.tbl = 'jvddos' 
      AND CAST(Aud.Dtt AS DATE) = CAST(DATEADD(DAY, -1, SYSDATETIME()) AS DATE)
      AND Dos.Dep = 'SEGURO' 
      AND Aud.Fld IN ('Cor', 'Exe') 
    ORDER BY Aud.Dtt DESC;
    """

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        connection.close()
        return results
    except pyodbc.Error as e:
        raise ConnectionError(f"Failed to fetch data from the database: {e}")

def send_email(recipient, subject, body):
    sender_email = "No-Reply@adcecija.pt"
    sender_password = "XYkVSZp#Vwl4gslhRKa%FGIE"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

def process_changes(data):
    for record in data:
        dtt, fld, old, new, dos, exe, cor, usr_email, new_email = record

        if fld == 'Exe' and old == '':
            body = f"Carissimo {new},\n\nO dossier nº {dos}, acabou de lhe ser designado\n\nMuito obrigado\nAP Seguros"
        elif fld == 'Cor' and old == '':
            body = f"Carissimo {new},\n\nAcabou de lhe ser designado, como Coordenador, o dossier nº {dos}, cujo Executante é {exe}\n\nMuito obrigado\nAP Seguros"
        elif fld == 'Exe' and old != '':
            body = f"Carissimo {new},\n\nO dossier nº {dos}, acabou de lhe ser designado pelo seu colega {old}\n\nMuito obrigado\nAP Seguros"
        elif fld == 'Cor' and old != '':
            body = f"Carissimo {new},\n\nAcabou de lhe ser designado, como Coordenador, o dossier nº {dos}, cujo Executante é {exe} pelo seu colega {old}\n\nMuito obrigado\nAP Seguros"
        else:
            continue

        send_email(new_email, "Notificação de Designação de Processo", body)

def main():
    try:
        data = fetch_data()
        process_changes(data)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()