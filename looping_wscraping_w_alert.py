import urllib.request
import smtplib
import time
from datetime import datetime
import winsound
from bs4 import BeautifulSoup

# Setting up email settings for sending account
# Password can be set as ENV variable for improved security
GMAIL_USER = r"..."
GMAIL_PASSWORD = r"..."

SERVER = smtplib.SMTP_SSL("smtp.gmail.com", 465)


# listin all relevant urls
URLS = ["... .html"]

while True:
    for url in URLS:

        # Avoiding 403-error using User-Agent
        req = urllib.request.Request(url, headers={"User-Agent": "Magic Browser"})
        response = urllib.request.urlopen(req)
        html = response.read()

        soup = BeautifulSoup(html, "lxml")

        # Getting item name & availability status
        span_title = soup.find_all(
            "span", {"class": "productHeaderTitle__Name-gtvrqo-1 iJLJgg"}
        )
        span_data = soup.find_all("span", {"class": "availabilityText ZZa4"})

        for span_tag in span_data:

            if (
                span_tag.text
                == "Pas disponible pour le moment – date de livraison inconnue."
            ):
                print(
                    f"{span_title[0].text} => Item unavailable, moving to next entry..."
                )
            else:
                print(f"{span_title[0].text} IS AVAILABLE!")

                # Creating email
                sent_from = GMAIL_USER
                to = ["...@gmail.com"]
                subject = "..."
                body = span_title[0].text + r" is available."

                email_text = """From: %s
                To: %s
                Subject: %s

                %s
                """ % (
                    sent_from,
                    ", ".join(to),
                    subject,
                    body,
                )

                # Sending email
                SERVER.ehlo()
                SERVER.login(GMAIL_USER, GMAIL_PASSWORD)
                SERVER.sendmail(sent_from, to, email_text)
                SERVER.close()

                print("Email sent - Running looping alert sound...")

                # Looping system sound
                while True:
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                    time.sleep(2)

    # current date and time
    DT_OBJECT = datetime.now()

    print(
        f"\n[{DT_OBJECT}]: No available items found - Pausing for 10 seconds before next iteration...\n\n"
    )
    time.sleep(10)
