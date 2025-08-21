def Email_body(username, userlogin, temppassword):
    global body
    
    body=f'''
    <div class="rps_5b4f"><div><div style="padding:31px"><div style="text-align:center; padding:5px; color:#FFFFFF; font-weight:600; font-size:18px; background-color:#009FDB; margin-bottom:40px">
                    INSMA USER LOGIN </div><div style="padding-right:100px"><span style="font-size:15px; color:#000000">
                    <div style="padding-right:100px"><span style="font-size:15px; color:#000000">
        Hello {username},<br><br>
        Your login credentials are as follows:
        <br><br>
        Username: {userlogin} <br>
        Password: {temppassword} <br><br>
        Please keep this information secure.<br><br>
        Thanks.
        </span></div></div><div></div></div></div></div>
    '''

    return body

