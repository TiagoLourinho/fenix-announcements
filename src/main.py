from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from json import JSONDecodeError
from lib2to3.pgen2.parse import ParseError
import weakref
import requests
import smtplib
from time import sleep
import traceback
import xml.etree.ElementTree as ET


from classes.announcement import Announcement
from input import students


def log(message, end="\n"):
    print(f'[{str(datetime.now()).split(".")[0]}]: {message}', end=end)


def get_seconds_since_epoch(ann):
    return ann.date.timestamp()


def send_email(type, student, course=None, ann=None, err=None):
    sender_address = "fenix.announcements@gmail.com"
    sender_pass = "ajvirxcjxhwpvife"
    receiver_address = student.email

    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_address

    if type == "WELCOME":

        message["Subject"] = f"Hello {student.name}!"
        body = """ <h1>Welcome!</h1>
            <p>You are now subscribed and will receive new announcements from the following courses:</p>
            <ul> """

        for c in student.courses:
            body += f"<li>{c.name}</li>"

        body += "</ul>"
        message.attach(MIMEText(body, "html"))

    elif type == "NEW":
        message["Subject"] = f"{course} - {ann.title}"
        body = ann.description + f"<br><br> Published at {ann.date} by {ann.author}."
        message.attach(MIMEText(body, "html"))

    elif type == "ERROR":
        message["Subject"] = "Error occured"
        body = err
        message.attach(MIMEText(body, "plain"))

    while True:
        try:
            session = smtplib.SMTP("smtp.gmail.com", 587)
            session.starttls()
            session.login(sender_address, sender_pass)
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()
            break
        except:
            e = traceback.format_exc()
            log(f"Error occured:\n {e}")

            sleep(60)
            continue


def main():
    log("Fennix announcements bot started")
    api = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/courses/"

    # Send welcome email
    for student in students:
        send_email("WELCOME", student)
        log(f"Welcome email sent to {student.email}")

    # Main loop
    while True:
        try:
            for student in students:
                for course in student.courses:

                    anns = []

                    # Get the XML that has the announcements list(using the FenixEdu API)
                    r = requests.get(api + str(course.id))
                    while r.status_code != 200:

                        log(
                            f"Couldn't get response from {api + str(course.id)} ({course.name})"
                        )
                        sleep(60)
                        r = requests.get(api + str(course.id))

                    ann_link = r.json()["announcementLink"]

                    r = requests.get(ann_link)
                    while r.status_code != 200:

                        log(f"Couldn't get response from {ann_link} ({course.name})")
                        sleep(60)
                        r = requests.get(ann_link)

                    xml = r.text

                    # Extract the announcements
                    root = ET.fromstring(xml)
                    for ann in root.findall("./channel/item"):
                        anns.append(
                            Announcement(
                                ann[0].text, ann[1].text, ann[-1].text, ann[3].text
                            )
                        )

                    # Sort chronologically
                    anns.sort(key=get_seconds_since_epoch)

                    # New announcement was made
                    if course.anns is not None and len(anns) > len(course.anns):
                        send_email("NEW", student, course.name, anns[-1])
                        log(
                            f"New announcement from {course.name}, emailed {student.email}"
                        )

                    course.anns = anns

            log("Sleeping...", end="\r")
            sleep(60)

        except JSONDecodeError:
            log("JSONDecodeError")

            sleep(60)
            continue

        except ParseError:
            log("ParseError")

            with open("latest_error.xml", "w") as f:
                f.write(xml)

            sleep(60)
            continue

        except Exception as e:
            # e = traceback.format_exc()
            log(f"Error occured:\n {e}")

            # send_email("ERROR", students[0], err=e)

            sleep(60)
            continue


if __name__ == "__main__":
    main()
