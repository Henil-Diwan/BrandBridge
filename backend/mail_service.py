from datetime import datetime, timedelta
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from model import Campaign, Influencers, Sponsors, Users

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "Brandbridge@gmail.com"
SENDER_PASSWORD = "dummy_password"


def send_message_daily():

    influencers = Influencers.query.all()
    sponsors = Sponsors.query.all()

    for sponsor in sponsors:
        requested_campaigns = Campaign.query.filter(
            Campaign.Created_by == sponsor.Sponser_ID,
            Campaign.Status == "Requested_by",
            Campaign.Flag == "No",
        ).limit(5)

        campaign_list = ""
        for campaign in requested_campaigns:
            campaign_list += f"<li>{campaign.Name} : By {Influencers.query.get(campaign.Influencer).Name}</li>"
        print(campaign_list)

        if campaign_list != "":

            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 15px;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Daily Reminder</h1>
                    <h2>Hello {sponsor.Name}</h2>
                    <br>
                    <p>You Have Pending Requests, Log into your Brandbridge Account to resolve them</p>
                </div>
                <div class="bg">
                    <ul>
                       <h3>{campaign_list}</h3>
                    </ul>
                </div>
                <div class="bg">
                    <p>Our team is continually working to connect you with influencers and opportunities that align with your brand. In the meantime, feel free to explore new partnerships, update your profile, or check out recent campaign insights.</p>
                    <br>
                    <p>We're here to help you make the most out of your BrandBridge experience. Stay tuned for new collaborations coming soon!</p>
                    <br>
                    <p>If you have any questions or need assistance, don't hesitate to reach out.</p>
                </div>
            </body>
            </html>
            """
        else:
            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Daily Reminder</h1>
                    <h2>Hello {sponsor.Name}</h2>
                    <br>
                    <p>At the moment, there are no pending requests in your BrandBridge account.</p>
                    <p>But you can always check in to see the latest Influencers</p>
                    <br>
                    <p>Our team is continually working to connect you with influencers and opportunities that align with your brand. In the meantime, feel free to explore new partnerships, update your profile, or check out recent campaign insights.</p>
                    <br>
                    <p>We're here to help you make the most out of your BrandBridge experience. Stay tuned for new collaborations coming soon!</p>
                    <br>
                    <p>If you have any questions or need assistance, don't hesitate to reach out.</p>



                </div>
            </body>
            </html>
            """

        msg = MIMEMultipart()
        msg["To"] = Users.query.get(sponsor.Created_by).Email
        msg["Subject"] = "Brandbridge Reminders"
        msg["From"] = SENDER_EMAIL

        msg.attach(MIMEText(html_content, "html"))
        client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
        client.send_message(msg=msg)
        client.quit()

    for influencer in influencers:

        requested_campaigns = Campaign.query.filter(
            Campaign.Influencer == influencer.Infuencer_ID,
            Campaign.Status == "Requested_to",
            Campaign.Flag == "No",
        ).all()

        campaign_list = ""
        for campaign in requested_campaigns:
            campaign_list += f"<li>{campaign.Name} : By {Sponsors.query.get(campaign.Created_by).Name}</li>"

        if campaign_list != "":

            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 15px;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Daily Reminder</h1>
                    <h2>Hello {influencer.Name}</h2>
                    <br>
                    <p>You Have Pending Requests, Log into your Brandbridge Account to resolve them</p>
                </div>
                <div class="bg">
                    <ul>
                       <h3>{campaign_list}</h3>
                    </ul>
                </div>
                <div class="bg">
                    <p>We're always on the lookout for exciting opportunities that fit your unique style and audience. Be sure to keep your profile updated and check in often for new campaigns and brand partnerships.</p>
                    <br>
                    <p>As always, if you have any questions or need support, we're just a message away!</p>
                </div>
            </body>
            </html>
            """
        else:
            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Daily Reminder</h1>
                    <h2>Hello {influencer.Name}</h2>
                    <br>
                    <p>We hope you're doing great!</p>
                    <p>It looks like there are no pending collaboration requests in your BrandBridge account right now.</p>
                    <br>
                    <p>Don't worry, we're always on the lookout for exciting opportunities that fit your unique style and audience. Be sure to keep your profile updated and check in often for new campaigns and brand partnerships.</p>
                    <br>
                    <p>As always, if you have any questions or need support, were just a message away!</p>
                </div>
            </body>
            </html>
            """

        msg = MIMEMultipart()
        msg["To"] = Users.query.get(influencer.Created_by).Email
        msg["Subject"] = "Brandbridge Reminders"
        msg["From"] = SENDER_EMAIL

        msg.attach(MIMEText(html_content, "html"))
        client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
        client.send_message(msg=msg)
        client.quit()


def send_message_monthly():
    influencers = Influencers.query.all()
    sponsors = Sponsors.query.all()

    current_year = datetime.now().year
    current_month = datetime.now().month
    start_of_month = datetime(current_year, current_month, 1)
    end_of_month = datetime(current_year, current_month + 1, 1) - timedelta(days=1)

    for sponsor in sponsors:

        active_campaigns = Campaign.query.filter(
            Campaign.Created_by == sponsor.Sponser_ID,
            Campaign.End_Date >= end_of_month,
            Campaign.Flag == "No",
        ).all()

        total_budget = sum(campaign.Budget for campaign in active_campaigns)
        campaign_no = len(active_campaigns)
        requested_to_length = len(
            Campaign.query.filter(
                Campaign.Created_by == sponsor.Sponser_ID,
                Campaign.End_Date >= end_of_month,
                Campaign.Flag == "No",
                Campaign.Status == "Requested_to",
            ).all()
        )
        requested_by_length = len(
            Campaign.query.filter(
                Campaign.Created_by == sponsor.Sponser_ID,
                Campaign.End_Date >= end_of_month,
                Campaign.Flag == "No",
                Campaign.Status == "Requested_by",
            ).all()
        )

        campaign_list = ""
        for campaign in active_campaigns:
            campaign_list += f"<li>{campaign.Name} : Status -  {campaign.Status}, Budget - {campaign.Budget}</li>"
        print(campaign_list)

        if campaign_list != "":

            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 15px;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Monthly Reminder</h1>
                    <h2>Hello {sponsor.Name}</h2>
                    <br>
                    <p>Heres Your Monthly Recap</p>
                </div>
                <div class="bg">
                    <h3>Total Spent: {total_budget}</h3>
                    <h3>Total Campaigns: {campaign_no}</h3>
                    <h3>Campaigns requested by you: {requested_to_length}</h3>
                    <h3>Campaigns requested to you: {requested_by_length}</h3>
                </div>
                <div class="bg">
                    <p>Here are all your campaigns this month</p>
                    <ul>
                       <p>{campaign_list}</p>
                    </ul>
                </div>
                <div class="bg">
                    <p>Our team is continually working to connect you with influencers and opportunities that align with your brand. In the meantime, feel free to explore new partnerships, update your profile, or check out recent campaign insights.</p>
                    <br>
                    <p>We're here to help you make the most out of your BrandBridge experience. Stay tuned for new collaborations coming soon!</p>
                    <br>
                    <p>If you have any questions or need assistance, don't hesitate to reach out.</p>
                </div>
            </body>
            </html>
            """
        else:
            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Daily Reminder</h1>
                    <h2>Hello {sponsor.Name}</h2>
                    <br>
                    <p>You did not have any campaigns this month</p>
                    <p>You can always create campaigns for the latest Influencers to boost</p>
                    <br>
                    <p>Our team is continually working to connect you with influencers and opportunities that align with your brand. In the meantime, feel free to explore new partnerships, update your profile, or check out recent campaign insights.</p>
                    <br>
                    <p>We're here to help you make the most out of your BrandBridge experience. Stay tuned for new collaborations coming soon!</p>
                    <br>
                    <p>If you have any questions or need assistance, don't hesitate to reach out.</p>



                </div>
            </body>
            </html>
            """

        msg = MIMEMultipart()
        msg["To"] = Users.query.get(sponsor.Created_by).Email
        msg["Subject"] = "Brandbridge Reminders"
        msg["From"] = SENDER_EMAIL

        msg.attach(MIMEText(html_content, "html"))
        client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
        client.send_message(msg=msg)
        client.quit()

    for influencer in influencers:

        active_campaigns = Campaign.query.filter(
            Campaign.Influencer == influencer.Infuencer_ID,
            Campaign.Status == "Accepted",
            Campaign.Flag == "No",
            Campaign.End_Date >= end_of_month,
        ).all()

        total_earnings = sum(campaign.Budget for campaign in active_campaigns)
        campaign_no = len(active_campaigns)
        requested_to_length = len(
            Campaign.query.filter(
                Campaign.Influencer == influencer.Infuencer_ID,
                Campaign.Status == "Requested_to",
                Campaign.Flag == "No",
                Campaign.End_Date >= end_of_month,
            ).all()
        )
        requested_by_length = len(
            Campaign.query.filter(
                Campaign.Influencer == influencer.Infuencer_ID,
                Campaign.Status == "Requested_by",
                Campaign.Flag == "No",
                Campaign.End_Date >= end_of_month,
            ).all()
        )

        campaign_list = ""
        for campaign in active_campaigns:
            campaign_list += f"<li>{campaign.Name} : Budget - {campaign.Budget}</li>"

        if campaign_list != "":

            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 15px;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Daily Reminder</h1>
                    <h2>Hello {influencer.Name}</h2>
                    <br>
                    <p>Heres Your Monthly Recap</p>
                </div>
                <div class="bg">
                    <h3>Total Earned: {total_earnings}</h3>
                    <h3>Total Campaigns: {campaign_no}</h3>
                    <h3>Campaigns requested to you: {requested_to_length}</h3>
                    <h3>Campaigns requested by you: {requested_by_length}</h3>
                </div>
                <div class="bg">
                    <p>Here are all your campaigns this month</p>
                    <ul>
                       <p>{campaign_list}</p>
                    </ul>
                </div>
                <div class="bg">
                    <p>We're always on the lookout for exciting opportunities that fit your unique style and audience. Be sure to keep your profile updated and check in often for new campaigns and brand partnerships.</p>
                    <br>
                    <p>As always, if you have any questions or need support, we're just a message away!</p>
                </div>
            </body>
            </html>
            """
        else:
            html_content = f"""
            <html>
            <head>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");

                    * {{
                        font-family: "Poppins", sans-serif;
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}

                    body {{
                        background-color: #1f1f47;
                        height: 100%;
                        margin: 0;
                        color: white;
                        padding: 30px;
                    }}

                    .purple-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        left: -100px;
                        top: -200px;
                        z-index: -1;
                    }}
                    .purple-circle-2 {{
                        position: absolute;
                        height: 150px;
                        width: 150px;
                        border-radius: 100%;
                        background-color: #784ba8;
                        top: -50px;
                        left: 1000px;
                        z-index: -1;
                    }}
                    .blue-circle {{
                        position: absolute;
                        height: 400px;
                        width: 400px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        right: -100px;
                        top: 150px;
                        z-index: -1;
                    }}
                    .blue-circle-2 {{
                        position: absolute;
                        height: 200px;
                        width: 200px;
                        border-radius: 100%;
                        background-color: #5c9df1;
                        left: -100px;
                        bottom: -100px;
                        z-index: -1;
                    }}
                    .pink-circle {{
                        position: absolute;
                        height: 500px;
                        width: 500px;
                        border-radius: 100%;
                        background-color: #fa709a;
                        bottom: -150px;
                        right: 500px;
                        z-index: -1;
                    }}

                    h1 {{
                        color: white;
                        text-align: center;
                        margin-bottom: 20px;
                    }}

                    p {{
                        font-size: 16px;
                        text-align: center;
                    }}

                    .highlight {{
                        color: #ff6347;
                        font-weight: bold;
                    }}
                    .bg {{
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="purple-circle"></div>
                <div class="purple-circle-2"></div>
                <div class="blue-circle"></div>
                <div class="blue-circle-2"></div>
                <div class="pink-circle"></div>

                <div class="bg">
                    <h1>BrandBridge - Daily Reminder</h1>
                    <h2>Hello {influencer.Name}</h2>
                    <br>
                    <p>We hope you're doing great!</p>
                    <p>It looks like you had no campaigns with BrandBridge this month.</p>
                    <br>
                    <p>Don't worry, we're always on the lookout for exciting opportunities that fit your unique style and audience. Be sure to keep your profile updated and check in often for new campaigns and brand partnerships.</p>
                    <br>
                    <p>As always, if you have any questions or need support, were just a message away!</p>
                </div>
            </body>
            </html>
            """

        msg = MIMEMultipart()
        msg["To"] = Users.query.get(influencer.Created_by).Email
        msg["Subject"] = "Brandbridge Reminders"
        msg["From"] = SENDER_EMAIL

        msg.attach(MIMEText(html_content, "html"))
        client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
        client.send_message(msg=msg)
        client.quit()
