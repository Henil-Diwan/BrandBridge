from celery import shared_task
import pandas as pd
from model import Campaign, Influencers


@shared_task
def create_resource_csv(sponsorid):
    # Create Flask app context
    from app import create_app
    app = create_app()
    with app.app_context():
        # Query for campaigns for the given sponsor
        campaigns = Campaign.query.filter(Campaign.Created_by == sponsorid).all()

        if not campaigns:
            return "No campaigns found for the given sponsor"

        # Convert campaigns to a list of dictionaries
        campaigns_data = [{
            'Campaign_ID': campaign.Campaign_ID,
            'Name': campaign.Name,
            'Desc': campaign.Desc,
            'Start_Date': campaign.Start_Date.strftime('%Y-%m-%d %H:%M:%S'),  # Format DateTime
            'End_Date': campaign.End_Date.strftime('%Y-%m-%d %H:%M:%S'),
            'Budget': campaign.Budget,
            'Goals': campaign.Goals,
            'Created_by': campaign.Created_by,
            'Influencer': Influencers.query.get(campaign.Influencer).Name if campaign.Influencer else "",
            'Status': campaign.Status,
            'Flag': campaign.Flag,
            'Views': campaign.Views,
            'Preferred_Category': campaign.Preferred_Category,
            'Visibility': campaign.Visibility
        } for campaign in campaigns]

        # Use pandas to create a DataFrame and generate CSV
        df = pd.DataFrame(campaigns_data)

        # Save the CSV to a file
        filename = f"campaigns_{sponsorid}.csv"

        df.to_csv(filename, index=False)

        # Return the file path or filename for later retrieval
        return filename