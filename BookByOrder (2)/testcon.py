import smtplib

def test_smtp_connection():
    try:
        # Remplacez les valeurs ci-dessous par vos informations SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('moisekapend80@gmail.com', '129012345K@ps')
        print("Connexion réussie")
        server.quit()
    except smtplib.SMTPAuthenticationError as e:
        print(f"Erreur d'authentification: {e}")
    except Exception as e:
        print(f"Erreur de connexion SMTP: {e}")

if __name__ == "__main__":
    test_smtp_connection()
