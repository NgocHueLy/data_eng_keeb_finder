if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    scrape_dates = ['2024-03-28','2024-03-29','2024-03-30']
    urls = []

    dfs = []
    # get download link
    for scrape_date in scrape_dates:
        url = f"https://raw.githubusercontent.com/NgocHueLy/data_eng_keeb_finder/main/csv/purchase_{scrape_date}.csv"
        urls.append(url)
    
    # dataframe
    for url in urls:
        df = pd.read_csv(url)

        df = df.drop('Link*',axis=1)

        df = df.rename(columns={"Price (USD)":"price", "Link*":"purchase_link"})

        dfs.append(df)


    return pd.concat(dfs, ignore_index=True)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
