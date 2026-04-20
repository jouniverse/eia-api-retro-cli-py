"""
Quick Fetch Definitions – ported from notes/quick-fetch-options.txt and
the Google Sheets reference app (freezer/eia-gs/src/QuickAccess.gs).

Each definition is a dict with:
  route          – API route after /v2/ (without trailing /data)
  frequency      – hourly | daily | weekly | monthly | annual
  data           – list of data field names
  facets         – dict of facet key → list of values (optional)
  start          – fixed start period string (optional)
  start_dynamic  – dynamic start config (optional, see eia_fetch.compute_dynamic_start)
  end            – fixed end period string (optional)
  offset         – initial paging offset (default 0)
  sort_dir       – sort direction (default "asc")
  label          – human-readable menu label
  group_col      – column to group by for charting (optional)
"""

# ---------------------------------------------------------------------------
# Featured / Short Selection
# ---------------------------------------------------------------------------
FEATURED_OPTIONS = [
    (
        "f_elec_hourly",
        "Electricity – Hourly Demand, Forecast, Generation & Interchange (US48, last week)",
    ),
    (
        "f_elec_daily_gen",
        "Electricity – Daily Generation By Energy Source (US48, last month)",
    ),
    ("f_ng_prices", "Natural Gas Prices (monthly, US, past 5y)"),
    ("f_petro_spot", "Petroleum Spot Prices – WTI & Brent (weekly, past 5y)"),
    ("f_seds_total", "SEDS – Total Energy (annual, US, from 1960)"),
    ("f_seds_renew", "SEDS – Renewable Energy (annual, US, from 1960)"),
    ("f_steo_total", "STEO – Total Energy Outlook (monthly, current → end of outlook)"),
    ("f_aeo_total", "AEO – Total Energy Outlook (annual, 2025 → end of outlook)"),
]

# ---------------------------------------------------------------------------
# Category option lists  (key, label)
# ---------------------------------------------------------------------------
COAL_OPTIONS = [
    ("coal_agg_prod", "Aggregate Production (annual, US, past 10y)"),
    ("coal_cons_quality", "Price and Consumption (annual, US)"),
    ("coal_exp_imp", "Exports / Imports / Quantity / Price (annual, past 10y)"),
    ("coal_market_sales", "Market Sales and Price (annual, US, from 2001)"),
    ("coal_mine_prod", "Mine Production (annual, active mines, past 2y)"),
    ("coal_price_rank", "Price by Rank (annual, US, from 2001)"),
    ("coal_reserves", "Reserves and Capacity (annual, US, from 2001)"),
]

CRUDE_OIL_IMPORTS_OPTIONS = [
    ("crude_imports", "Crude Oil Imports (monthly, world → US, past 5y)"),
]

ELECTRICITY_OPTIONS = [
    (
        "elec_hourly",
        "Hourly Demand, Forecast, Generation & Interchange (US48, last week)",
    ),
    (
        "elec_daily_region",
        "Daily Demand, Forecast, Generation & Interchange (US48, last month)",
    ),
    (
        "elec_daily_interchange",
        "Daily Interchange By Neighboring BA (US48, last month)",
    ),
    ("elec_net_gen", "Utility Scale Net Generation (monthly, US, past 10y)"),
    ("elec_retail_price", "Average Retail Price (monthly, US, past 10y)"),
    (
        "elec_emissions",
        "Emissions at Conventional Power Plants (annual, US, from 1990)",
    ),
    ("elec_capacity", "Generating Capacity (annual, US, from 1990)"),
]

INTERNATIONAL_OPTIONS = [
    (
        "intl_oil_ng",
        "World/US Oil & NG Production/Consumption/Stocks (monthly, past 10y)",
    ),
    ("intl_us_oil_prod", "US Oil Production (monthly, OECD, past 20y)"),
    (
        "intl_us_petro_cons",
        "US Refined Petroleum Consumption (monthly, OECD, past 10y)",
    ),
]

NATURAL_GAS_OPTIONS = [
    ("ng_prices", "Natural Gas Prices (monthly, US, past 5y)"),
    ("ng_futures", "Spot & Futures Prices NYMEX (weekly, past 5y)"),
    ("ng_res_comm", "Avg Price Residential & Commercial (monthly, past 5y)"),
    ("ng_consumption", "Consumption By End Use (monthly, US, past 10y)"),
    ("ng_consumers", "Number Of Consumers (annual, US, past 20y)"),
    ("ng_heat", "Heat Content Consumed (monthly, US, past 10y)"),
    ("ng_reserves", "Reserves Summary (annual, US, past 30y)"),
    ("ng_imports_country", "Imports By Country (monthly, US, past 10y)"),
    ("ng_imports_entry", "Imports By Point Of Entry (monthly, US, past 10y)"),
    ("ng_exports_country", "Exports By Country (monthly, US, past 10y)"),
    ("ng_exports_exit", "Exports By Point Of Exit (monthly, US, past 10y)"),
    ("ng_storage", "Underground Storage Capacity (monthly, US, past 10y)"),
    ("ng_summary", "Natural Gas Summary (monthly, US, past 2y)"),
]

NUCLEAR_OUTAGES_OPTIONS = [
    ("nuclear_outages", "US Nuclear Outages (daily, past 1y)"),
]

PETROLEUM_OPTIONS = [
    (
        "petro_reserves",
        "Crude Oil Proved Reserves & Production (annual, US, from 1976)",
    ),
    ("petro_crude_prod", "Crude Oil Production (monthly, US, past 20y)"),
    (
        "petro_retail_gas",
        "Weekly Retail Gasoline & Diesel Prices (weekly, US, past 2y)",
    ),
    ("petro_spot", "Spot Prices – WTI & Brent (weekly, past 5y)"),
    ("petro_heating", "Heating Oil & Propane Prices (weekly, US, past 5y)"),
    ("petro_product_supply", "Weekly Product Supplied (weekly, US, past 5y)"),
    ("petro_refiner_prod", "Weekly Refiner Net Production (weekly, US, past 5y)"),
    ("petro_imports", "Imports By Area Of Entry (monthly, US, past 10y)"),
    ("petro_exports", "Exports (monthly, US, past 10y)"),
    ("petro_weekly_stocks", "Weekly Stocks (weekly, US, past 1y)"),
    ("petro_stocks_type", "Stocks By Type (monthly, US, past 10y)"),
    ("petro_supply_est", "Weekly Supply Estimates (weekly, US, past 1y)"),
    ("petro_supply_disp", "Crude Oil Supply & Disposition (monthly, US, past 10y)"),
]

SEDS_OPTIONS = [
    ("seds_total", "Total Energy (annual, US, from 1960)"),
    ("seds_renew", "Renewable Energy (annual, US, from 1960)"),
    ("seds_solar", "Solar Energy (annual, US, from 1960)"),
]

DENSIFIED_BIOMASS_OPTIONS = [
    ("biomass_capacity", "Capacity By Region (monthly, US Total, past 10y)"),
    ("biomass_chars", "Characteristics By Region (monthly, past 10y)"),
    ("biomass_export", "Export Sales and Price (monthly, past 10y)"),
    ("biomass_feedstock", "Feedstocks and Costs (monthly, past 10y)"),
    ("biomass_inventory", "Inventories By Region (monthly, US Total, past 10y)"),
    ("biomass_production", "Production By Region (monthly, US Total, past 10y)"),
    ("biomass_sales", "Sales and Price By Region (monthly, US Total, past 10y)"),
]

TOTAL_ENERGY_OPTIONS = [
    ("te_monthly", "Total Energy (monthly, US, past 10y)"),
    ("te_annual", "Total Energy (annual, US, from 1949)"),
    ("te_crude", "Crude Oil (annual, US, from 1949)"),
    ("te_fossil", "Fossil Fuels (annual, US, from 1949)"),
    ("te_solar", "Solar Energy (annual, US, from 1949)"),
]

STEO_OPTIONS = [
    ("steo_total", "Total Energy Outlook (monthly, current → end of outlook)"),
    ("steo_crude", "Crude Oil Outlook (monthly, current → end of outlook)"),
    ("steo_ng", "Natural Gas Outlook (monthly, current → end of outlook)"),
    ("steo_renew", "Renewable Energy Outlook (monthly, current → end of outlook)"),
]

AEO_OPTIONS = [
    ("aeo_macro", "Macroeconomic Indicators (annual, 2025 → end of outlook)"),
    ("aeo_total", "Total Energy Outlook (annual, 2025 → end of outlook)"),
    ("aeo_crude", "Crude Oil Price Outlook (annual, 2025 → end of outlook)"),
    ("aeo_oilgas", "Oil and Gas Supply Outlook (annual, 2025 → end of outlook)"),
    ("aeo_renew", "Renewable Energy Capacity Outlook (annual, 2025 → end of outlook)"),
]

IEO_OPTIONS = [
    ("ieo_energy", "World Energy Consumption (annual, outlook)"),
    ("ieo_co2", "World CO2 Emissions (annual, outlook)"),
    ("ieo_crude", "World Crude Oil (annual, outlook)"),
    ("ieo_coal", "World Coal (annual, outlook)"),
    ("ieo_ng", "World Natural Gas (annual, outlook)"),
    ("ieo_renew", "World Renewable Energy (annual, outlook)"),
    ("ieo_elec", "World Electricity Generation (annual, outlook)"),
    ("ieo_gdp", "World GDP (annual, outlook)"),
    ("ieo_pop", "World Population (annual, outlook)"),
]

CO2_OPTIONS = [
    ("co2_total", "Total CO2 Emissions By Sector & Fuel (annual, US, from 1970)"),
]


# ---------------------------------------------------------------------------
# Full definitions dict
# ---------------------------------------------------------------------------
QUICK_FETCH_DEFS = {
    # ── Featured (aliases that point to same defs as category versions) ──
    "f_elec_hourly": {
        "route": "electricity/rto/region-data",
        "frequency": "hourly",
        "data": ["value"],
        "facets": {"respondent": ["US48"]},
        "start_dynamic": {"unit": "days", "amount": 7, "hourly": True},
        "label": "Electricity Hourly Demand (US48, last week)",
        "group_col": "type-name",
    },
    "f_elec_daily_gen": {
        "route": "electricity/rto/daily-fuel-type-data",
        "frequency": "daily",
        "data": ["value"],
        "facets": {"respondent": ["US48"]},
        "start_dynamic": {"unit": "days", "amount": 30},
        "label": "Electricity Daily Generation By Source (US48, last month)",
        "group_col": "fueltype",
    },
    "f_ng_prices": {
        "route": "natural-gas/pri/sum",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "duoarea": ["NUS"],
            "process": ["FWA", "PCS", "PEU", "PG1", "PIN", "PRS"],
        },
        "start_dynamic": {"unit": "years", "amount": 5, "monthly": True},
        "label": "Natural Gas Prices (US, past 5y)",
        "group_col": "process-name",
    },
    "f_petro_spot": {
        "route": "petroleum/pri/spt",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {"product": ["EPCBRENT", "EPCWTI"]},
        "start_dynamic": {"unit": "years", "amount": 5},
        "label": "Petroleum Spot Prices WTI & Brent (past 5y)",
        "group_col": "product-name",
    },
    "f_seds_total": {
        "route": "seds",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "seriesId": [
                "TENEB",
                "TEPRB",
                "TETCB",
                "TETCD",
                "TETCE",
                "TETCV",
                "TETGR",
                "TETPB",
                "TETPV",
            ],
            "stateId": ["US"],
        },
        "start": "1960",
        "label": "SEDS Total Energy (US, from 1960)",
        "group_col": "seriesDescription",
    },
    "f_seds_renew": {
        "route": "seds",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "stateId": ["US"],
            "seriesId": ["REPRB", "RETCB", "RETES"],
        },
        "start": "1960",
        "label": "SEDS Renewable Energy (US, from 1960)",
        "group_col": "seriesDescription",
    },
    "f_steo_total": {
        "route": "steo",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "seriesId": ["RETCBUS", "TETCCO2", "TETCFUEL", "TOEPGEN_US", "TOTOGEN_US"],
        },
        "start_dynamic": {"unit": "months", "amount": 0, "monthly": True},
        "offset": 100,
        "label": "STEO Total Energy Outlook",
        "group_col": "seriesId",
    },
    "f_aeo_total": {
        "route": "aeo/2025",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["1"],
            "seriesId": [
                "cnsm_use_ten_NA_tot_NA_usa_qbtu",
                "sup_prd_ten_NA_tot_NA_usa_qbtu",
                "trad_exp_ten_NA_tot_NA_usa_qbtu",
                "trad_imp_ten_NA_tot_NA_usa_qbtu",
                "unc_NA_ten_NA_descr_NA_usa_qbtu",
            ],
        },
        "start": "2025",
        "label": "AEO Total Energy Outlook (2025)",
        "group_col": "seriesName",
    },
    # ── Coal ──────────────────────────────────────────────────────────────
    "coal_agg_prod": {
        "route": "coal/aggregate-production",
        "frequency": "annual",
        "data": ["production"],
        "facets": {"stateRegionId": ["US"], "mineTypeId": ["ALL"]},
        "start": "2016",
        "label": "Coal Aggregate Production",
    },
    "coal_cons_quality": {
        "route": "coal/consumption-and-quality",
        "frequency": "annual",
        "data": ["consumption", "price"],
        "facets": {"location": ["US"]},
        "label": "Coal Consumption & Quality",
    },
    "coal_exp_imp": {
        "route": "coal/exports-imports-quantity-price",
        "frequency": "annual",
        "data": ["price", "quantity"],
        "facets": {
            "countryId": ["TOT"],
            "customsDistrictId": ["TOT"],
            "coalRankId": ["TOT"],
        },
        "start": "2016",
        "label": "Coal Exports/Imports",
    },
    "coal_market_sales": {
        "route": "coal/market-sales-price",
        "frequency": "annual",
        "data": ["price", "sales"],
        "facets": {"stateRegionId": ["US"], "marketTypeId": ["TOT"]},
        "start": "2001",
        "label": "Coal Market Sales & Price",
    },
    "coal_mine_prod": {
        "route": "coal/mine-production",
        "frequency": "annual",
        "data": ["latitude", "longitude", "production"],
        "facets": {"mineStatusId": ["ACT"]},
        "start": "2023",
        "label": "Coal Mine Production",
    },
    "coal_price_rank": {
        "route": "coal/price-by-rank",
        "frequency": "annual",
        "data": ["price"],
        "facets": {"stateRegionId": ["US"]},
        "start": "2001",
        "label": "Coal Price by Rank",
    },
    "coal_reserves": {
        "route": "coal/reserves-capacity",
        "frequency": "annual",
        "data": ["recoverable-reserves"],
        "facets": {"stateId": ["US"], "mineTypeId": ["TOT"]},
        "start": "2001",
        "label": "Coal Reserves & Capacity",
    },
    # ── Crude Oil Imports ─────────────────────────────────────────────────
    "crude_imports": {
        "route": "crude-oil-imports",
        "frequency": "monthly",
        "data": ["quantity"],
        "facets": {"originId": ["WORLD"], "destinationType": ["US"]},
        "start_dynamic": {"unit": "years", "amount": 5, "monthly": True},
        "label": "Crude Oil Imports (world → US)",
    },
    # ── Electricity ───────────────────────────────────────────────────────
    "elec_hourly": {
        "route": "electricity/rto/region-data",
        "frequency": "hourly",
        "data": ["value"],
        "facets": {"respondent": ["US48"]},
        "start_dynamic": {"unit": "days", "amount": 7, "hourly": True},
        "label": "Electricity Hourly Demand (US48)",
        "group_col": "type-name",
    },
    "elec_daily_region": {
        "route": "electricity/rto/daily-region-data",
        "frequency": "daily",
        "data": ["value"],
        "facets": {"respondent": ["US48"]},
        "start_dynamic": {"unit": "days", "amount": 30},
        "label": "Electricity Daily Region Data (US48)",
        "group_col": "type-name",
    },
    "elec_daily_interchange": {
        "route": "electricity/rto/daily-interchange-data",
        "frequency": "daily",
        "data": ["value"],
        "facets": {"fromba": ["US48"]},
        "start_dynamic": {"unit": "days", "amount": 30},
        "label": "Electricity Daily Interchange (US48)",
        "group_col": "toba",
    },
    "elec_net_gen": {
        "route": "electricity/electric-power-operational-data",
        "frequency": "monthly",
        "data": ["generation"],
        "facets": {"location": ["US"], "sectorid": ["99"], "fueltypeid": ["ALL"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Utility Scale Net Generation (US)",
    },
    "elec_retail_price": {
        "route": "electricity/retail-sales",
        "frequency": "monthly",
        "data": ["price"],
        "facets": {"stateid": ["US"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Average Retail Electricity Price (US)",
        "group_col": "sectorName",
    },
    "elec_emissions": {
        "route": "electricity/state-electricity-profiles/emissions-by-state-by-fuel",
        "frequency": "annual",
        "data": [
            "co2-rate-lbs-mwh",
            "co2-thousand-metric-tons",
            "nox-rate-lbs-mwh",
            "nox-short-tons",
            "so2-rate-lbs-mwh",
            "so2-short-tons",
        ],
        "facets": {"stateid": ["US"], "fuelid": ["ALL"]},
        "start": "1990",
        "label": "Power Plant Emissions (US)",
    },
    "elec_capacity": {
        "route": "electricity/state-electricity-profiles/capability",
        "frequency": "annual",
        "data": ["capability"],
        "facets": {"stateId": ["US"], "producertypeid": ["TOT"]},
        "start": "1990",
        "label": "Generating Capacity (US)",
    },
    # ── International ─────────────────────────────────────────────────────
    "intl_oil_ng": {
        "route": "international",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"countryRegionId": ["USA", "WORL"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "World/US Oil & NG (monthly)",
        "group_col": "countryRegionName",
    },
    "intl_us_oil_prod": {
        "route": "international",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"countryRegionId": ["USA"], "productId": ["53", "55"]},
        "start_dynamic": {"unit": "years", "amount": 20, "monthly": True},
        "label": "US Oil Production (OECD, past 20y)",
        "group_col": "productName",
    },
    "intl_us_petro_cons": {
        "route": "international",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "countryRegionId": ["USA"],
            "activityId": ["2"],
            "productId": ["54"],
        },
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "US Refined Petroleum Consumption (OECD)",
    },
    # ── Natural Gas ───────────────────────────────────────────────────────
    "ng_prices": {
        "route": "natural-gas/pri/sum",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "duoarea": ["NUS"],
            "process": ["FWA", "PCS", "PEU", "PG1", "PIN", "PRS"],
        },
        "start_dynamic": {"unit": "years", "amount": 5, "monthly": True},
        "label": "Natural Gas Prices (US)",
        "group_col": "process-name",
    },
    "ng_futures": {
        "route": "natural-gas/pri/fut",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {"duoarea": ["RGC", "Y35NY"]},
        "start_dynamic": {"unit": "years", "amount": 5},
        "label": "NG Spot & Futures (NYMEX)",
        "group_col": "process-name",
    },
    "ng_res_comm": {
        "route": "natural-gas/pri/rescom",
        "frequency": "monthly",
        "data": ["value"],
        "start_dynamic": {"unit": "years", "amount": 5, "monthly": True},
        "label": "NG Avg Price Residential & Commercial",
        "group_col": "process-name",
    },
    "ng_consumption": {
        "route": "natural-gas/cons/sum",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "NG Consumption By End Use (US)",
        "group_col": "process-name",
    },
    "ng_consumers": {
        "route": "natural-gas/cons/num",
        "frequency": "annual",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start_dynamic": {"unit": "years", "amount": 20, "annual": True},
        "label": "Number Of NG Consumers (US)",
        "group_col": "process-name",
    },
    "ng_heat": {
        "route": "natural-gas/cons/heat",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "NG Heat Content Consumed (US)",
        "group_col": "process-name",
    },
    "ng_reserves": {
        "route": "natural-gas/enr/sum",
        "frequency": "annual",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start": "1996",
        "label": "NG Reserves Summary (US)",
        "group_col": "process-name",
    },
    "ng_imports_country": {
        "route": "natural-gas/move/impc",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS-Z00"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "NG Imports By Country (US)",
        "group_col": "process-name",
    },
    "ng_imports_entry": {
        "route": "natural-gas/move/poe1",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS-Z00"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "NG Imports By Point Of Entry (US)",
        "group_col": "process-name",
    },
    "ng_exports_country": {
        "route": "natural-gas/move/expc",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS-Z00"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "NG Exports By Country (US)",
        "group_col": "process-name",
    },
    "ng_exports_exit": {
        "route": "natural-gas/move/poe2",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS-Z00"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "NG Exports By Point Of Exit (US)",
        "group_col": "process-name",
    },
    "ng_storage": {
        "route": "natural-gas/stor/cap",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"], "process": ["SAC"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Underground NG Storage Capacity (US)",
    },
    "ng_summary": {
        "route": "natural-gas/sum/lsum",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS", "NUS-Z00"]},
        "start_dynamic": {"unit": "years", "amount": 2, "monthly": True},
        "sort_dir": "desc",
        "label": "Natural Gas Summary (US)",
        "group_col": "process-name",
    },
    # ── Nuclear Outages ───────────────────────────────────────────────────
    "nuclear_outages": {
        "route": "nuclear-outages/us-nuclear-outages",
        "frequency": "daily",
        "data": ["capacity", "outage", "percentOutage"],
        "start_dynamic": {"unit": "years", "amount": 1},
        "label": "US Nuclear Outages (daily)",
    },
    # ── Petroleum ─────────────────────────────────────────────────────────
    "petro_reserves": {
        "route": "petroleum/crd/pres",
        "frequency": "annual",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"], "process": ["R01", "R10"]},
        "start": "1976",
        "label": "Crude Oil Reserves & Production (US)",
        "group_col": "process-name",
    },
    "petro_crude_prod": {
        "route": "petroleum/crd/crpdn",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start_dynamic": {"unit": "years", "amount": 20, "monthly": True},
        "label": "Crude Oil Production (US)",
        "group_col": "product-name",
    },
    "petro_retail_gas": {
        "route": "petroleum/pri/gnd",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start_dynamic": {"unit": "years", "amount": 2},
        "label": "Retail Gasoline & Diesel Prices (US)",
        "group_col": "product-name",
    },
    "petro_spot": {
        "route": "petroleum/pri/spt",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {"product": ["EPCBRENT", "EPCWTI"]},
        "start_dynamic": {"unit": "years", "amount": 5},
        "label": "Spot Prices WTI & Brent",
        "group_col": "product-name",
    },
    "petro_heating": {
        "route": "petroleum/pri/wfr",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start_dynamic": {"unit": "years", "amount": 5},
        "label": "Heating Oil & Propane Prices (US)",
        "group_col": "product-name",
    },
    "petro_product_supply": {
        "route": "petroleum/cons/wpsup",
        "frequency": "weekly",
        "data": ["value"],
        "start_dynamic": {"unit": "years", "amount": 5},
        "label": "Weekly Product Supplied (US)",
        "group_col": "product-name",
    },
    "petro_refiner_prod": {
        "route": "petroleum/pnp/wprodr",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS"]},
        "start_dynamic": {"unit": "years", "amount": 5},
        "label": "Refiner Net Production (US)",
        "group_col": "product-name",
    },
    "petro_imports": {
        "route": "petroleum/move/imp",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "duoarea": ["NUS-Z00"],
            "product": ["EP00", "EPC0"],
        },
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Petroleum Imports (US)",
        "group_col": "product-name",
    },
    "petro_exports": {
        "route": "petroleum/move/exp",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "duoarea": ["NUS-Z00"],
            "product": ["EP00", "EPC0"],
        },
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Petroleum Exports (US)",
        "group_col": "product-name",
    },
    "petro_weekly_stocks": {
        "route": "petroleum/stoc/wstk",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {
            "duoarea": ["NUS"],
            "product": ["EP00", "EPC0"],
        },
        "start_dynamic": {"unit": "years", "amount": 1},
        "label": "Weekly Stocks (US)",
        "group_col": "product-name",
    },
    "petro_stocks_type": {
        "route": "petroleum/stoc/typ",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "duoarea": ["NUS"],
            "product": ["EP00", "EPC0"],
        },
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Stocks By Type (US)",
        "group_col": "product-name",
    },
    "petro_supply_est": {
        "route": "petroleum/sum/sndw",
        "frequency": "weekly",
        "data": ["value"],
        "facets": {
            "duoarea": ["NUS", "NUS-Z00"],
            "product": ["EP00", "EPC0"],
        },
        "start_dynamic": {"unit": "years", "amount": 1},
        "label": "Weekly Supply Estimates (US)",
        "group_col": "product-name",
    },
    "petro_supply_disp": {
        "route": "petroleum/sum/crdsnd",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {"duoarea": ["NUS", "NUS-Z00"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Crude Oil Supply & Disposition (US)",
        "group_col": "process-name",
    },
    # ── SEDS ──────────────────────────────────────────────────────────────
    "seds_total": {
        "route": "seds",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "seriesId": [
                "TENEB",
                "TEPRB",
                "TETCB",
                "TETCD",
                "TETCE",
                "TETCV",
                "TETGR",
                "TETPB",
                "TETPV",
            ],
            "stateId": ["US"],
        },
        "start": "1960",
        "label": "SEDS Total Energy (US)",
        "group_col": "seriesDescription",
    },
    "seds_renew": {
        "route": "seds",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "stateId": ["US"],
            "seriesId": ["REPRB", "RETCB", "RETES"],
        },
        "start": "1960",
        "label": "SEDS Renewable Energy (US)",
        "group_col": "seriesDescription",
    },
    "seds_solar": {
        "route": "seds",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "seriesId": [
                "SOCCB",
                "SOCCP",
                "SOEGB",
                "SOEGP",
                "SOICB",
                "SOICP",
                "SOPRB",
                "SOR7P",
                "SORCB",
                "SOTCB",
                "SOTGP",
                "SOTXB",
            ],
            "stateId": ["US"],
        },
        "start": "1960",
        "label": "SEDS Solar Energy (US)",
        "group_col": "seriesDescription",
    },
    # ── Densified Biomass ─────────────────────────────────────────────────
    "biomass_capacity": {
        "route": "densified-biomass/capacity-by-region",
        "frequency": "monthly",
        "data": ["capacity", "number-of-facilities", "number-of-fte-employees"],
        "facets": {"region": ["US-TOTAL"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Biomass Capacity (US)",
    },
    "biomass_chars": {
        "route": "densified-biomass/characteristics-by-region",
        "frequency": "monthly",
        "data": ["average-ash", "average-heat", "average-moisture"],
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Biomass Characteristics By Region",
        "group_col": "region",
    },
    "biomass_export": {
        "route": "densified-biomass/export-sales-and-price",
        "frequency": "monthly",
        "data": ["average-price", "quantity"],
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Biomass Export Sales & Price",
    },
    "biomass_feedstock": {
        "route": "densified-biomass/feedstocks-and-cost",
        "frequency": "monthly",
        "data": ["cost", "quantity"],
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Biomass Feedstocks & Costs",
    },
    "biomass_inventory": {
        "route": "densified-biomass/inventories-by-region",
        "frequency": "monthly",
        "data": ["inventory"],
        "facets": {"region": ["US-TOTAL"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Biomass Inventories (US)",
    },
    "biomass_production": {
        "route": "densified-biomass/production-by-region",
        "frequency": "monthly",
        "data": ["production"],
        "facets": {"region": ["US-TOTAL"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Biomass Production (US)",
    },
    "biomass_sales": {
        "route": "densified-biomass/sales-and-price-by-region",
        "frequency": "monthly",
        "data": ["average-price", "quantity"],
        "facets": {"region": ["US-TOTAL"]},
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Biomass Sales & Price (US)",
    },
    # ── Total Energy ──────────────────────────────────────────────────────
    "te_monthly": {
        "route": "total-energy",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "msn": [
                "BMPRBUS",
                "BMTCBUS",
                "REPRBUS",
                "RETCBUS",
                "TEEXBUS",
                "TEIMBUS",
                "TENFSUS",
                "TENIBUS",
                "TEPRBUS",
                "TETCBUS",
                "TETCEUS",
                "TFPRBUS",
                "TFTCBUS",
                "TXEIBUS",
            ],
        },
        "start_dynamic": {"unit": "years", "amount": 10, "monthly": True},
        "label": "Total Energy Monthly (US)",
        "group_col": "seriesDescription",
    },
    "te_annual": {
        "route": "total-energy",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "msn": [
                "BMPRBUS",
                "BMTCBUS",
                "REPRBUS",
                "RETCBUS",
                "TEEXBUS",
                "TEIMBUS",
                "TENFSUS",
                "TENIBUS",
                "TEPRBUS",
                "TETCBUS",
                "TETCEUS",
                "TFPRBUS",
                "TFTCBUS",
                "TXEIBUS",
            ],
        },
        "start": "1949",
        "label": "Total Energy Annual (US)",
        "group_col": "seriesDescription",
    },
    "te_crude": {
        "route": "total-energy",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "msn": [
                "CODPUUS",
                "COEXBUS",
                "COEXPUS",
                "COIMBUS",
                "COIMPUS",
                "CONIBUS",
                "COPSPUS",
                "COSQPUS",
                "OGTWPUS",
            ],
        },
        "start": "1949",
        "label": "Total Energy – Crude Oil (US)",
        "group_col": "seriesDescription",
    },
    "te_fossil": {
        "route": "total-energy",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "msn": ["FFPRBUS", "FFTCBUS", "TFPRBUS", "TFTCBUS"],
        },
        "start": "1949",
        "label": "Total Energy – Fossil Fuels (US)",
        "group_col": "seriesDescription",
    },
    "te_solar": {
        "route": "total-energy",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "msn": ["SOETPUS", "SOFFBUS", "SOGBPUS", "SOTCBUS", "SOTEPUS"],
        },
        "start": "1949",
        "offset": 340,
        "label": "Total Energy – Solar (US)",
        "group_col": "seriesDescription",
    },
    # ── STEO ──────────────────────────────────────────────────────────────
    "steo_total": {
        "route": "steo",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "seriesId": ["RETCBUS", "TETCCO2", "TETCFUEL", "TOEPGEN_US", "TOTOGEN_US"],
        },
        "start_dynamic": {"unit": "months", "amount": 0, "monthly": True},
        "offset": 100,
        "label": "STEO Total Energy Outlook",
        "group_col": "seriesId",
    },
    "steo_crude": {
        "route": "steo",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "seriesId": [
                "BREPUUS",
                "CONIPUS",
                "COPRPUS",
                "COPR_WORLD",
                "WORLD_NC",
                "WTIPUUS",
            ],
        },
        "start_dynamic": {"unit": "months", "amount": 0, "monthly": True},
        "label": "STEO Crude Oil Outlook",
        "group_col": "seriesId",
    },
    "steo_ng": {
        "route": "steo",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "seriesId": [
                "NGEPSHR_US",
                "NGEPTOT",
                "NGEXPUS",
                "NGHHMCF",
                "NGHHUUS",
                "NGIMPUS",
            ],
        },
        "start_dynamic": {"unit": "months", "amount": 0, "monthly": True},
        "label": "STEO Natural Gas Outlook",
        "group_col": "seriesId",
    },
    "steo_renew": {
        "route": "steo",
        "frequency": "monthly",
        "data": ["value"],
        "facets": {
            "seriesId": [
                "RETCBUS",
                "RTEPGEN_US",
                "RTEPSHR_US",
                "SODTC_US",
                "SOTCBUS",
                "SOTOGEN_US",
                "SOTOPUS",
                "WNTCBUS",
                "WNTOGEN_US",
            ],
        },
        "start_dynamic": {"unit": "months", "amount": 0, "monthly": True},
        "label": "STEO Renewable Energy Outlook",
        "group_col": "seriesId",
    },
    # ── AEO ───────────────────────────────────────────────────────────────
    "aeo_macro": {
        "route": "aeo/2025",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["18"],
            "seriesId": [
                "dmg_empm_nofm_NA_NA_NA_NA_mill",
                "eci_NA_NA_NA_gdp_real_NA_blny09dlr",
                "eci_ffr_NA_NA_NA_NA_NA_pcntn",
                "eci_tnr10_NA_NA_NA_NA_NA_pcntn",
                "eci_vos_NA_NA_NA_NA_NA_blny09dlr",
            ],
        },
        "start": "2025",
        "label": "AEO Macroeconomic Indicators",
        "group_col": "seriesName",
    },
    "aeo_total": {
        "route": "aeo/2025",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["1"],
            "seriesId": [
                "cnsm_use_ten_NA_tot_NA_usa_qbtu",
                "sup_prd_ten_NA_tot_NA_usa_qbtu",
                "trad_exp_ten_NA_tot_NA_usa_qbtu",
                "trad_imp_ten_NA_tot_NA_usa_qbtu",
                "unc_NA_ten_NA_descr_NA_usa_qbtu",
            ],
        },
        "start": "2025",
        "label": "AEO Total Energy Outlook",
        "group_col": "seriesName",
    },
    "aeo_crude": {
        "route": "aeo/2025",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["12"],
            "seriesId": [
                "prce_NA_NA_NA_cr_brntsppr_usa_y13dlrpbbl",
                "prce_NA_NA_NA_cr_wti_usa_y13dlrpbbl",
                "prce_mark_NA_NA_cr_NA_usa_y13dlrpbbl",
            ],
        },
        "start": "2025",
        "label": "AEO Crude Oil Price Outlook",
        "group_col": "seriesName",
    },
    "aeo_oilgas": {
        "route": "aeo/2025",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["14"],
            "seriesId": [
                "prce_hhp_NA_NA_ng_hhp_usa_y13dlrpmmbtu",
                "sup_dpr_NA_NA_ng_tot_usa_trlcf",
                "sup_prd_NA_NA_cr_NA_usa_millbrlpdy",
                "sup_prd_NA_NA_ngp_NA_usa_millbrlpdy",
            ],
        },
        "start": "2025",
        "label": "AEO Oil & Gas Supply Outlook",
        "group_col": "seriesName",
    },
    "aeo_renew": {
        "route": "aeo/2025",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["16"],
            "seriesId": [
                "cap_NA_alls_NA_tot_NA_NA_gw",
                "cap_NA_enus_NA_tot_NA_NA_gw",
                "cap_nts_elep_NA_tot_NA_NA_gw",
                "gen_NA_alls_NA_tot_NA_NA_blnkwh",
                "gen_NA_elep_NA_tot_NA_NA_blnkwh",
                "gen_NA_enus_NA_tot_NA_NA_blnkwh",
            ],
        },
        "start": "2025",
        "label": "AEO Renewable Capacity Outlook",
        "group_col": "seriesName",
    },
    # ── IEO ───────────────────────────────────────────────────────────────
    "ieo_energy": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["1"],
            "seriesId": ["cnsm_pe_usa_qbtu", "cnsm_pe_wor_qbtu"],
        },
        "label": "IEO World Energy Consumption",
        "group_col": "seriesName",
    },
    "ieo_co2": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["10"],
            "seriesId": ["emi_co2_fossil_usa_mtonne", "emi_co2_fossil_wor_mtonne"],
        },
        "label": "IEO World CO2 Emissions",
        "group_col": "seriesName",
    },
    "ieo_crude": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["24", "30"],
            "seriesId": [
                "prce_cdp_wptpprc_dolperbarrel",
                "sup_liqp_cd_usa_mbpd",
                "sup_liqp_cd_wor_mbpd",
            ],
        },
        "label": "IEO World Crude Oil",
        "group_col": "seriesName",
    },
    "ieo_coal": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["7", "86", "89"],
            "seriesId": [
                "cnsm_clp_wor_mst",
                "sup_clp_exp_wor_mst",
                "sup_clp_imp_wor_mst",
            ],
        },
        "label": "IEO World Coal",
        "group_col": "seriesName",
    },
    "ieo_ng": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["41", "42", "6"],
            "seriesId": [
                "cnsm_ngp_wor_tcf",
                "ngprod_tot_wor_tcf",
                "trade_gas_usa_tcf",
                "trade_gas_wor_tcf",
            ],
        },
        "offset": 300,
        "label": "IEO World Natural Gas",
        "group_col": "seriesName",
    },
    "ieo_renew": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["9"],
            "seriesId": ["cnsm_rn_usa_qbtu", "cnsm_rn_wor_qbtu"],
        },
        "label": "IEO World Renewable Energy",
        "group_col": "seriesName",
    },
    "ieo_elec": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["20"],
            "seriesId": ["pgdis_gen_tot_bkwh"],
            "regionId": ["6-0", "6-2"],
        },
        "label": "IEO World Electricity Generation",
        "group_col": "regionName",
    },
    "ieo_gdp": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["3", "4", "47"],
            "seriesId": [
                "gdpmer_wor_b2015dol",
                "gdpppp_wor_b2015dol",
                "gdpppppercap_wor_2015dolpercap",
            ],
        },
        "label": "IEO World GDP",
        "group_col": "seriesName",
    },
    "ieo_pop": {
        "route": "ieo/2023",
        "frequency": "annual",
        "data": ["value"],
        "facets": {
            "tableId": ["15"],
            "seriesId": ["pop_usa_m", "pop_wor_m"],
        },
        "label": "IEO World Population",
        "group_col": "seriesName",
    },
    # ── CO2 Emissions ─────────────────────────────────────────────────────
    "co2_total": {
        "route": "co2-emissions/co2-emissions-aggregates",
        "frequency": "annual",
        "data": ["value"],
        "facets": {"stateId": ["US"]},
        "start": "1970",
        "label": "Total CO2 Emissions (US)",
        "group_col": "fuel-name",
    },
}
