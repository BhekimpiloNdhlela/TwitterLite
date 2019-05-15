
def get_email_template(link):
	email_content = """
	<html>
		<head>
			<title>HTML email confirmation</title>
		</head>
	"""
	email_content += """
		<style type="text/css">
			@media only screen and (max-width: 480px) {
				table[class=email], table[class=email-content] { clear: both; width: 320px !important; }
			}
		</style>
	"""
	email_content += '''
		<body>
		<table width="99%" border="0" cellpadding="0" cellspacing="0">
			<tr>
				<td align="center" valign="top" bgcolor="#c9c9c9">
					<!-- Second HTML table is the email itself -->
					<table class="email" width="500" border="0" cellpadding="0" cellspacing="0">
						<tr>
							<td align="center" valign="top">
		<p style="font-family: Helvetica, Arial, sans-serif; font-size: 10px; line-height: 12px; margin-top: 20px; margin-right: 0; margin-bottom: 20px; margin-left: 0; padding-top: 0; padding-right: 0; padding-bottom: 0; padding-right: 0;">

		</p>
							</td>
						</tr>
						<tr>
							<td align="center" valign="top" bgcolor="#00aced">
		<h1 style="font-family: Georgia, Times, serif; font-size: 48px; font-weight: normal; line-height: 48px; margin-top: 20px; margin-right: 20px; margin-bottom: 20px; margin-left: 20px; padding-top: 0; padding-right: 0; padding-bottom: 0; padding-right: 0;">
		<img src="https://github.com/BhekimpiloNdhlela/405-Found/blob/master/app/static/img/logo.png" height="55px" width="55px"> Bootleg Twitter
		</h1>

							</td>
						</tr>
						<tr>
							<td valign="top" bgcolor="#999999">
								<table class="email-content" align="left" width="650" border="0" cellpadding="0" cellspacing="0">
									<tr>
										<td valign="top" bgcolor="#f5f7f8">
		<h2 align="center" style="color: #000000; font-family: Helvetica, Arial, sans-serif; font-size: 24px; font-weight: normal; line-height: 24px; margin-top: 20px; margin-right: 0; margin-bottom: 20px; margin-left: 20px; padding-top: 0; padding-right: 0; padding-bottom: 0; padding-right: 0;">
		We're glad you've joined the dark side!
		</h2>
		<form action="{0}">
		<div style="text-align: center;">
         	<button type="submit" align="center" style="margin:0 auto; display: block; background-color:#333333;border:1px solid #333333;border-color:#333333;border-radius:6px;border-width:1px;color:#ffffff;display:inline-block;font-family:arial,helvetica,sans-serif;font-size:16px;font-weight:normal;letter-spacing:0px;line-height:16px;padding:12px 18px 12px 18px;text-align:center;text-decoration:none">Confirm your email</button> </div>
      	</form>
		<p align="center" style="color: #000000; font-family: Georgia, Times, serif; font-size: 15px; line-height: 22px; margin-top: 0; margin-right: 10px; margin-bottom: 20px; margin-left: 20px; padding-top: 0; padding-right: 0; padding-bottom: 0; padding-right: 0;">
		We just want to confirm you're you.
		</p>
										</td>
									</tr>
								</table>
							</td>
						</tr>
						<tr>

						</tr>
						<tr>
							<td align="left" valign="top">

		<p style="font-family: Helvetica, Arial, sans-serif; font-size: 10px; line-height: 16px; margin-top: 15px; margin-right: 0; margin-bottom: 20px; margin-left: 20px; padding-top: 0; padding-right: 0; padding-bottom: 0; padding-right: 0;">
		You are receiving this email because you have signed up for an account on Bootleg Twitter. If you didn't create a Bootleg Twitter account, just delete this email and eveything will go back too the way it was. Probably.
		</p>
							</td>
						</tr>
					</table>
				
				</td>
			</tr>
		</table>
		</body>
	</html>
	'''.format(link )
	return email_content

