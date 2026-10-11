from celery import shared_task
import pandas as pd
from model import Campaign, Influencers
from mail_service import send_message_daily, send_message_monthly


@shared_task(ignore_result=False)
def create_resource_csv(sponsorid):

    from app import app

    with app.app_context():

        campaigns = Campaign.query.filter(Campaign.Created_by == sponsorid).all()

        if not campaigns:
            return "No campaigns found for the given sponsor"

        campaigns_data = [
            {
                "Campaign_ID": campaign.Campaign_ID,
                "Name": campaign.Name,
                "Desc": campaign.Desc,
                "Start_Date": campaign.Start_Date.strftime("%Y-%m-%d %H:%M:%S"),
                "End_Date": campaign.End_Date.strftime("%Y-%m-%d %H:%M:%S"),
                "Budget": campaign.Budget,
                "Goals": campaign.Goals,
                "Created_by": campaign.Created_by,
                "Influencer": (
                    Influencers.query.get(campaign.Influencer).Name
                    if campaign.Influencer
                    else ""
                ),
                "Status": campaign.Status,
                "Flag": campaign.Flag,
                "Views": campaign.Views,
                "Preferred_Category": campaign.Preferred_Category,
                "Visibility": campaign.Visibility,
            }
            for campaign in campaigns
        ]

        df = pd.DataFrame(campaigns_data)

        filename = f"campaigns_{sponsorid}.csv"

        df.to_csv(filename, index=False)

        return filename


@shared_task(ignore_result=True)
def daily_reminder():
    send_message_daily()
    return "OK"


@shared_task(ignore_result=True)
def monthly_reminder():
    send_message_monthly()
    return "OK"
