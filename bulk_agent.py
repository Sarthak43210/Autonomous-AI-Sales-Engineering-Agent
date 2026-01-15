import pandas as pd
import time
import os
from agent import search_company_news, write_email_logic

def run_bulk_outreach(input_file, output_file):
    # 1. Safety Check: Does the file even exist and have content?
    if not os.path.exists(input_file) or os.stat(input_file).st_size == 0:
        print(f"❌ Error: The file '{input_file}' is empty or missing!")
        print("Please add 'company_name' on the first line and then your companies below it.")
        return

    try:
        # 2. Load the leads
        df = pd.read_csv(input_file)
        
        # Check if 'company_name' column exists
        if 'company_name' not in df.columns:
            print("❌ Error: Could not find 'company_name' column in your CSV.")
            return

        results = []
        print(f"🚀 Starting bulk process for {len(df)} companies...")

        for index, row in df.iterrows():
            company = row['company_name']
            print(f"\nProcessing {index+1}/{len(df)}: {company}")

            # Research and Generate
            research = search_company_news(company)
            email_draft = write_email_logic(company, research)
            
            results.append({
                "Company": company,
                "Email_Draft": email_draft
            })

            # Respect the 2026 Free Tier Limits (wait between requests)
            if index < len(df) - 1:
                print("💤 Sleeping 35s to stay under quota...")
                time.sleep(35)

        # 3. Save results
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_file, index=False)
        print(f"\n✅ Success! Check '{output_file}' for your emails.")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_bulk_outreach("leads.csv", "outreach_results.csv")