import pandas as pd


def printInfo(data, reduced_cols=False):
    df = pd.DataFrame(data["response"]["routes"])
    #  df columns = "id", "name", "description"

    lines = []
    separator = "-" * 50  # Separator line between records

    if reduced_cols:
        for _, row in df.iterrows():
            lines.append(separator)
            lines.append(f"ID: {row['id']}")
            lines.append(f"NAME: {row['name']}")
    else:
        for _, row in df.iterrows():
            lines.append(separator)
            lines.append(f"ID: {row['id']}")
            lines.append(f"NAME: {row['name']}")
            lines.append(f"DESCRIPTION: {row['description']}")
    lines.append(separator)  # Add a final separator

    table = "\n".join(lines)
    print(table)
