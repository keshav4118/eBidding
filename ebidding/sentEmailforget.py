
def mymail(username, password):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    me = "kesh8085@gmail.com"
    you = username

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Verification Mail eAuction"
    msg['From'] = me
    msg['To'] = you

    html = """<html>
  					<head></head>
  					<body>
    					<h1> This is your eBidding Account Id & Password </h1>
    					<h2>Username : """+username+"""</h2>
    					<h2>Password : """+str(password)+"""</h2>
    					<br>
    					<a href='http://localhost:8000/login/' >Click here to Log In </a>		
  					</body>
				</html> 
    """

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("kesh8085@gmail.com", "8085761835")

    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    s.sendmail(me, you, str(msg))
    s.quit()
    print("mail send successfully....")
