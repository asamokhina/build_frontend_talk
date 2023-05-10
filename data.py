import pandas as pd
import matplotlib.pyplot as plt

def get_data():
    df = pd.read_csv("Steps.csv")

    # transform 'date' column to date object
    df['Date'] = pd.to_datetime(df['Date'] + " " + ["2023"], format="%b %d %Y")
    df = df.set_index("Date")
    

    return df

def create_basic_plot(df):
    fig, ax = plt.subplots()
    ax.plot(df.index, df["Actual"], marker="o", label="Actual")
    ax.plot(df.index, df['Goal'], label="Goal")
    ax.set_title("Steps Per Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Steps")
    
    plt.legend(loc="upper left")
    ax.grid(True)
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    return fig