import pandas as pd
from datetime import datetime
import os

def load_data(filepath):
    """Load and parse the CSV data file."""
    return pd.read_csv(filepath, parse_dates=['ChatStartTime', 'ChatEndTime'])

def calculate_chat_metrics(df):
    """Generate Chat Metrics summary as a dictionary."""
    total_chats = len(df)
    bot_closed = len(df[df['ClosedBy'].str.lower() == 'system'])
    agent_closed = total_chats - bot_closed
    bot_deflection = (bot_closed / total_chats) * 100 if total_chats > 0 else 0

    metrics = {
        "Total Chats": total_chats,
        "Closed by Bot": bot_closed,
        "Closed by Agent": agent_closed,
        "Bot Deflection %": round(bot_deflection, 2)
    }
    return pd.DataFrame(metrics.items(), columns=["Metric", "Value"])

def calculate_agent_metrics(df):
    """Create agent-wise performance DataFrame."""
    df = df[df['ClosedBy'].str.lower() != 'system'].copy()
    df['Response Time (mins)'] = df['AgentFirstResponseTime'] / 60
    df['Chat Duration (mins)'] = (df['ChatEndTime'] - df['ChatStartTime']).dt.total_seconds() / 60

    def get_shift(hour):
        if 9 <= hour < 15:
            return 'Morning'
        elif 15 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'

    df['Shift'] = df['ChatStartTime'].dt.hour.apply(get_shift)

    agent_summary = df.groupby('ClosedBy').agg({
        'Response Time (mins)': 'mean',
        'Chat Duration (mins)': 'mean',
        'CSATScore': 'mean'
    }).round(2).reset_index()

    shift_summary = df.groupby('Shift').agg({'CSATScore': 'mean'}).round(2).reset_index()
    return agent_summary, shift_summary

def export_report(chat_df, agent_df, shift_df):
    """Save all dataframes to an Excel report."""
    os.makedirs('reports', exist_ok=True)
    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    with pd.ExcelWriter(filename) as writer:
        chat_df.to_excel(writer, index=False, sheet_name="Chat Metrics")
        agent_df.to_excel(writer, index=False, sheet_name="Agent Metrics")
        shift_df.to_excel(writer, index=False, sheet_name="Shift CSAT Metrics")

    print(f"✅ Report generated and saved to: {filename}")

def main():
    df = load_data('data/data_dump.csv')
    chat_metrics = calculate_chat_metrics(df)
    agent_metrics, shift_metrics = calculate_agent_metrics(df)
    export_report(chat_metrics, agent_metrics, shift_metrics)

if __name__ == "__main__":
    main()
