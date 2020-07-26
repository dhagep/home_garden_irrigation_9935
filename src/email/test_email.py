import smtplib
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("homeirrigation9935@gmail.com", "vivieva9935")
msg="hello"
server.sendmail("homeirrigation9935@gmail.com","pratikpdhage@gmail.com", msg)
server.quit()

